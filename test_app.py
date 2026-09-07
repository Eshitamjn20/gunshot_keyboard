import ctypes
import queue
import unittest
from unittest.mock import Mock
from app import KeyboardHook
from audio_engine import AudioEngine, synthesize, STYLES
from unittest.mock import patch
import struct


class Tests(unittest.TestCase):
    def test_audio(self):
        for style in STYLES:
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
            self.assertEqual(mixer.find_channel.return_value.play.call_count, 13)
            mixer.find_channel.return_value.set_volume.assert_called_with(0.4)
            mixer.stop.assert_called_once()
            mixer.quit.assert_called_once()
            self.assertFalse(engine.worker.is_alive())

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
