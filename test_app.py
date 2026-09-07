import ctypes
from pathlib import Path
import queue
import tempfile
import unittest
import wave
from unittest.mock import Mock
from app import KeyboardHook, make_sound


class Tests(unittest.TestCase):
    def test_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sound.wav'
            for style in ('Gunshot', 'Arcade laser', 'Soft pop'):
                for volume in (0, 20, 100):
                    make_sound(path, style, volume)
                    with wave.open(str(path)) as audio:
                        self.assertEqual(audio.getnchannels(), 1)
                        self.assertEqual(audio.getsampwidth(), 2)
                        self.assertEqual(audio.getframerate(), 22050)
                        frames = audio.readframes(audio.getnframes())
                        self.assertEqual(len(frames), 9702)
                        self.assertEqual(any(frames), volume != 0)

    def test_repeat_release_hotkey_and_forwarding(self):
        hook = KeyboardHook.__new__(KeyboardHook)
        hook.events = queue.SimpleQueue()
        hook.held = set()
        hook.user = Mock()
        hook.user.CallNextHookEx.return_value = 123
        key = ctypes.c_ulong(65)
        for message in (0x100, 0x100, 0x101, 0x100):
            self.assertEqual(hook.handle(0, message, ctypes.addressof(key)), 123)
        self.assertEqual([hook.events.get(), hook.events.get()], ['play', 'play'])
        self.assertTrue(hook.events.empty())
        key.value = 0x77
        hook.handle(0, 0x104, ctypes.addressof(key))
        self.assertEqual(hook.events.get(), 'toggle')
        self.assertEqual(hook.user.CallNextHookEx.call_count, 5)
