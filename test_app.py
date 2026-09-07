import ctypes
import queue
import unittest
from unittest.mock import Mock
from app import KeyboardHook
from audio_engine import AudioEngine, synthesize, STYLES
from unittest.mock import patch
import struct
import wave
from pathlib import Path


class Tests(unittest.TestCase):
    def test_audio(self):
        for style in STYLES[1:]:
            data = synthesize(style)
            self.assertEqual(len(data), 26880)
            samples = struct.unpack('<13440h', data)
            self.assertEqual(samples[0], 0)
            self.assertEqual(samples[-1], 0)
            self.assertEqual(max(abs(x) for x in samples), 16000)
            self.assertTrue(any(samples[:48]))  # Attack starts within 1 ms.
            self.assertTrue(data != synthesize(style, 1), style)

    def test_burst_is_not_coalesced_and_mute_stops_audio(self):
        with patch('audio_engine.mixer') as mixer:
            engine = AudioEngine()
            engine.put('play')  # Starts muted.
            engine.put('toggle')
            for _ in range(12):
                engine.put('play')
            engine.put('toggle')
            engine.put('play')  # Muted again.
            engine.put(('Deep shot', 0.4))
            engine.put('preview')
            engine.close()  # Drains prior commands before stopping.
            self.assertEqual(mixer.Channel.return_value.play.call_count, 13)
            mixer.Channel.return_value.set_volume.assert_called_with(0.4)
            mixer.stop.assert_called_once()
            mixer.quit.assert_called_once()
            self.assertFalse(engine.worker.is_alive())

    def test_shotgun_asset_and_rhythm(self):
        with wave.open(str(Path(__file__).parent / 'assets/shotgun.wav')) as source:
            self.assertEqual(source.getparams()[:3], (1, 2, 48000))
            data = source.readframes(source.getnframes())
        samples = struct.unpack('<%dh' % (len(data) // 2), data)
        self.assertEqual(max(abs(x) for x in samples), 28000)
        self.assertEqual(samples[0], 0)
        self.assertEqual(samples[-1], 0)
        self.assertGreater(max(abs(x) for x in samples[:48]), 1000)
        with patch('audio_engine.mixer') as mixer, patch('audio_engine.time.monotonic', side_effect=[0, .08, .16, .24, 1]):
            engine = AudioEngine()
            engine.put('toggle')
            for _ in range(5):
                engine.put('play')
            engine.close()
            plays = mixer.Channel.return_value.play.call_args_list
            self.assertEqual([call.kwargs['maxtime'] for call in plays], [430, 150, 150, 150, 430])
            volumes = mixer.Channel.return_value.set_volume.call_args_list
            accents = [volumes[i].args[0] for i in range(4, len(volumes), 5)]
            for actual, expected in zip(accents, [.6, .492, .552, .492, .6]):
                self.assertAlmostEqual(actual, expected)

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
