"""KeyBang: offline Windows keyboard sound toy. Run with python app.py."""
import ctypes
from ctypes import wintypes
import math
from pathlib import Path
import queue
import random
import struct
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox
import wave
import winsound


def make_sound(path, style, volume):
    """Synthesize original effects, so there are no downloaded audio assets."""
    rng = random.Random(42)
    rate = 22050
    frames = bytearray()
    for i in range(int(rate * 0.22)):
        t = i / rate
        noise = rng.uniform(-1, 1)
        if style == 'Arcade laser':
            sample = math.sin(2 * math.pi * (1200 * t - 2200 * t * t)) * math.exp(-22 * t)
        elif style == 'Soft pop':
            sample = (0.7 * math.sin(2 * math.pi * 170 * t) + 0.3 * noise) * math.exp(-45 * t)
        else:
            sample = (0.75 * noise + 0.25 * math.sin(2 * math.pi * 75 * t)) * math.exp(-27 * t)
        frames.extend(struct.pack('<h', int(sample * 26000 * volume / 100)))
    with wave.open(str(path), 'wb') as audio:
        audio.setparams((1, 2, rate, 0, 'NONE', 'not compressed'))
        audio.writeframes(frames)


class KeyboardHook:
    """Pass every event onward; keep only transient held-key state."""
    def __init__(self, events):
        self.events = events
        self.held = set()
        self.user = ctypes.WinDLL('user32', use_last_error=True)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.callback_type = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        self.user.SetWindowsHookExW.argtypes = [ctypes.c_int, self.callback_type, wintypes.HINSTANCE, wintypes.DWORD]
        self.user.SetWindowsHookExW.restype = wintypes.HANDLE
        self.user.CallNextHookEx.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
        self.user.CallNextHookEx.restype = ctypes.c_ssize_t
        self.user.UnhookWindowsHookEx.argtypes = [wintypes.HANDLE]
        kernel.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        kernel.GetModuleHandleW.restype = wintypes.HMODULE
        self.callback = self.callback_type(self.handle)
        self.hook = self.user.SetWindowsHookExW(13, self.callback, kernel.GetModuleHandleW(None), 0)
        if not self.hook:
            raise ctypes.WinError(ctypes.get_last_error())

    def handle(self, code, message, address):
        if code == 0:
            key = ctypes.cast(address, ctypes.POINTER(wintypes.DWORD))[0]
            if message in (0x100, 0x104):
                if key not in self.held:
                    self.held.add(key)
                    self.events.put('toggle' if key == 0x77 else 'play')
            elif message in (0x101, 0x105):
                self.held.discard(key)
        return self.user.CallNextHookEx(None, code, message, address)

    def close(self):
        if self.hook:
            self.user.UnhookWindowsHookEx(self.hook)
            self.hook = None


class App:
    def __init__(self, root):
        self.root = root
        self.enabled = False
        self.events = queue.SimpleQueue()
        self.temp = tempfile.TemporaryDirectory(prefix='keybang-')
        self.cache = {}
        self.hook = None
        root.title('KeyBang • Keyboard sound effects')
        root.geometry('500x520')
        root.minsize(460, 500)
        root.configure(bg='#111827')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#111827')
        style.configure('TLabel', background='#111827', foreground='#e5e7eb', font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 11), padding=10)
        panel = ttk.Frame(root, padding=30)
        panel.pack(fill='both', expand=True)
        ttk.Label(panel, text='KEYBANG', font=('Segoe UI', 28, 'bold'), foreground='#a3e635').pack(anchor='w')
        ttk.Label(panel, text='Give your keyboard a soundtrack.').pack(anchor='w', pady=(0, 24))
        self.status = ttk.Label(panel, text='●  Muted', font=('Segoe UI', 16, 'bold'))
        self.status.pack(anchor='w')
        self.toggle_button = ttk.Button(panel, text='Enable sounds', command=self.toggle)
        self.toggle_button.pack(fill='x', pady=12)
        ttk.Label(panel, text='Sound effect').pack(anchor='w', pady=(10, 5))
        self.sound = tk.StringVar(value='Gunshot')
        ttk.Combobox(panel, textvariable=self.sound, values=['Gunshot', 'Arcade laser', 'Soft pop'], state='readonly').pack(fill='x')
        self.volume = tk.DoubleVar(value=20)
        self.volume_label = ttk.Label(panel, text='Volume · 20%')
        self.volume_label.pack(anchor='w', pady=(20, 0))
        ttk.Scale(panel, from_=0, to=100, variable=self.volume, command=self.volume_changed).pack(fill='x', pady=8)
        ttk.Button(panel, text='Preview sound', command=self.play).pack(fill='x')
        ttk.Label(panel, text='F8 toggles mute from any app.\nWorks while minimized. Close the window to quit.\nOffline • No typing history • No account', font=('Segoe UI', 10), foreground='#9ca3af').pack(anchor='w', pady=22)
        root.protocol('WM_DELETE_WINDOW', self.close)
        try:
            self.hook = KeyboardHook(self.events)
        except OSError as exc:
            messagebox.showerror('Keyboard listener unavailable', str(exc))
            self.close()
            return
        root.after(10, self.poll)

    def volume_changed(self, _):
        self.volume_label.configure(text=f'Volume · {int(self.volume.get())}%')

    def toggle(self):
        self.enabled = not self.enabled
        self.status.configure(text='●  Listening' if self.enabled else '●  Muted')
        self.toggle_button.configure(text='Mute sounds' if self.enabled else 'Enable sounds')
        if not self.enabled:
            winsound.PlaySound(None, 0)

    def play(self):
        key = (self.sound.get(), int(self.volume.get()))
        if key[1] == 0:
            return
        try:
            if key not in self.cache:
                path = Path(self.temp.name) / f'{len(self.cache)}.wav'
                make_sound(path, *key)
                self.cache[key] = str(path)
            winsound.PlaySound(self.cache[key], winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
        except (OSError, RuntimeError) as exc:
            self.enabled = False
            self.status.configure(text='Audio unavailable — try Preview')
            self.toggle_button.configure(text='Enable sounds')

    def poll(self):
        # Coalesce bursts so a busy UI never plays a backlog of old keystrokes.
        play = False
        while not self.events.empty():
            event = self.events.get()
            if event == 'toggle':
                self.toggle()
                play = False
            elif self.enabled:
                play = True
        if play and self.enabled:
            self.play()
        self.root.after(10, self.poll)

    def close(self):
        if self.hook:
            self.hook.close()
        winsound.PlaySound(None, 0)
        self.temp.cleanup()
        self.root.destroy()


if __name__ == '__main__':
    window = tk.Tk()
    App(window)
    window.mainloop()
