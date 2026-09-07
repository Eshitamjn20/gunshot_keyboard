"""Preloaded sound bank and event-driven playback; no file I/O per key."""
import math
import os
import queue
import random
import struct
import threading

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
from pygame import mixer

RATE = 48000
STYLES = ('Gunshot', 'Deep shot', 'Arcade laser', 'Soft pop')


def synthesize(style, variant=0):
    rng = random.Random(42 + variant)
    samples = []
    low = 0.0
    pitch = 1 + (variant - 1) * 0.025
    for i in range(int(RATE * 0.28)):
        t = i / RATE
        noise = rng.uniform(-1, 1)
        low += 0.12 * (noise - low)
        if style == 'Arcade laser':
            value = math.sin(2 * math.pi * pitch * (1200 * t - 1800 * t * t)) * math.exp(-24 * t)
        elif style == 'Soft pop':
            value = (0.8 * math.sin(2 * math.pi * 170 * t) + 0.2 * low) * math.exp(-55 * t)
        else:
            deep = style == 'Deep shot'
            # Dry muzzle crack, pitched low body, filtered air, and short reflections.
            crack = (noise - low) * math.exp(-t * 260) * 0.95
            body = math.sin(2 * math.pi * pitch * ((75 if deep else 115) * t + 1.3 * (1 - math.exp(-65 * t))))
            body *= math.exp(-t * (28 if deep else 42)) * 0.85
            air = low * math.exp(-t * 32) * 1.3
            metal = math.sin(2 * math.pi * 2200 * pitch * t) * math.exp(-t * 180) * 0.12
            value = crack + body + air + metal
            for delay, gain in ((0.019, 0.16), (0.037, 0.08)):
                if i >= int(delay * RATE):
                    value += samples[i - int(delay * RATE)] * gain
        # Sub-millisecond attack and terminal fade avoid artificial edge clicks.
        value *= min(1, i / 12) * min(1, (int(RATE * 0.28) - 1 - i) / 240)
        samples.append(value)
    peak = max(abs(value) for value in samples) or 1
    # Headroom for overlapping voices.
    return b''.join(struct.pack('<h', round(value / peak * 16000)) for value in samples)


class AudioEngine:
    def __init__(self):
        mixer.init(frequency=RATE, size=-16, channels=1, buffer=256, allowedchanges=0)
        mixer.set_num_channels(32)
        self.bank = {style: [mixer.Sound(buffer=synthesize(style, i)) for i in range(3)] for style in STYLES}
        self.enabled = False
        self.error = None
        self.style = 'Gunshot'
        self.volume = 0.2
        self.index = 0
        self.events = queue.SimpleQueue()
        self.worker = threading.Thread(target=self.run, name='KeyBang audio', daemon=True)
        self.worker.start()

    def put(self, event):
        self.events.put(event)

    def run(self):
        while True:
            event = self.events.get()  # Wakes immediately; no UI timer.
            if event == 'quit':
                break
            try:
                if isinstance(event, tuple):
                    self.style, self.volume = event
                elif event == 'toggle':
                    self.enabled = not self.enabled
                    if not self.enabled:
                        mixer.stop()
                elif event == 'preview' or (event == 'play' and self.enabled):
                    if self.volume > 0:
                        channel = mixer.find_channel(force=True)
                        channel.set_volume(self.volume)
                        channel.play(self.bank[self.style][self.index % 3])
                        self.index += 1
            except Exception as exc:
                self.error = str(exc)
                self.enabled = False
                mixer.stop()

    def close(self):
        self.put('quit')
        self.worker.join()
        mixer.quit()
