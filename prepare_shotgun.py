"""Rebuild bundled shotgun from sounds-source.zip (see assets/CREDITS.md)."""
import io
import math
from pathlib import Path
import struct
import wave
import zipfile

with zipfile.ZipFile('sounds-source.zip') as archive:
    with wave.open(io.BytesIO(archive.read('sounds/shotty.wav'))) as source:
        assert source.getparams()[:3] == (2, 2, 48000)
        raw = struct.unpack('<%dh' % (source.getnframes() * 2), source.readframes(source.getnframes()))
mono = [(raw[i] + raw[i + 1]) / 65536 for i in range(0, len(raw), 2)]
# Remove pre-shot handling noise and shape a dry, immediate keyboard hit.
mono = mono[round(0.148 * 48000):round(0.578 * 48000)]
output = []
low = 0
for i, sample in enumerate(mono):
    t = i / 48000
    low += 0.035 * (sample - low)
    body = 0.18 * math.sin(2 * math.pi * (90 * t + 0.9 * (1 - math.exp(-40 * t)))) * math.exp(-18 * t)
    value = math.tanh(2.3 * (sample + 0.65 * low + body))
    value *= math.exp(-6 * t) * min(1, i / 10) * min(1, (len(mono) - 1 - i) / 480)
    output.append(value)
peak = max(abs(x) for x in output)
Path('assets').mkdir(exist_ok=True)
with wave.open('assets/shotgun.wav', 'wb') as target:
    target.setparams((1, 2, 48000, 0, 'NONE', 'not compressed'))
    target.writeframes(b''.join(struct.pack('<h', round(x / peak * 28000)) for x in output))
