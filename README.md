# KeyBang

A free, offline Windows keyboard sound toy.

## Try it

Open `dist/KeyBang.exe`, click **Preview sound**, then **Enable sounds**.
Choose Shotgun, Gunshot, Deep shot, Arcade laser, or Soft pop and adjust the volume.
**F8** mutes/unmutes from any normal desktop app. F8 still reaches that app.
Starts muted at 60%. Minimize to keep it running; close to quit.
Rhythm accents follow your keystrokes immediately with a four-hit pattern;
there is no fixed BPM or beat-grid delay. A pause resets the pattern.
No administrator access, account, server or paid API is required.

## How it works: a beginner's tour

1. **Interface:** Python's Tkinter draws the window, buttons and slider.
2. **Input:** `KeyboardHook` in `app.py` asks Windows for keyboard events,
   including while other apps are focused. Events pass onward unchanged.
3. **Audio:** The default Shotgun uses a processed real recording, with
   pre-shot noise trimmed, a low body layer and compression. See
   `assets/CREDITS.md` for source attribution and licensing. Other effects
   are synthesized. All effects are preloaded before listening starts.
4. **Responsiveness:** The hook queues signals to a worker that wakes on
   each event. An open pygame-ce mixer plays sounds with a 256-sample
   buffer at 48 kHz (5.3 ms of samples, not total measured latency).
   Four channels let tails fade beneath fresh attacks. No files open per press;
   the UI timer updates labels only. Smaller buffers reduce mixer latency:
   https://www.pygame.org/docs/ref/mixer.html
5. **Distribution:** PyInstaller bundles Python and the app into one EXE.
   Your friends do not need to install Python.

The listener temporarily tracks held key codes to suppress key repeat.
It never saves typed text and makes no network connections. Closing the
app removes the hook and shuts down the mixer.

## Develop and build

With Python 3.14 on Windows:

```powershell
.\build.ps1
.\.venv\Scripts\python.exe app.py
.\.venv\Scripts\python.exe -m unittest -v
```

The build script creates a local virtual environment and downloads
PyInstaller and pygame-ce. The finished app works offline. Source-only
development can instead use `python -m pip install -r requirements.txt`.

## Share

Send `dist/KeyBang.exe`, or attach it to a GitHub repository release to
provide a download link. No public release has been uploaded yet.
You do not need to distribute `.venv` or `build`.

This build targets Windows 10/11 Intel/AMD 64-bit PCs. Test on another
PC without Python before claiming broader compatibility. The executable
is unsigned, so Windows/antivirus may show a reputation warning. Paid
code signing is optional and outside this free prototype.

## First-version limits and verification

- Earlier sounds fade over 35 ms at reduced volume for mix headroom.
  Hits less than 120 ms apart get 150 ms tails; slower hits get 430 ms.
  Rhythm accents use a repeating strong/soft/medium/soft pattern and reset
  after 450 ms idle. Disable the checkbox for equal accents. No input
  events are deliberately coalesced or held back to align with a beat.
- Holding a key produces one sound, not automatic repeated shots.
- Secure screens and some elevated apps/games may not provide events.
- Settings reset at startup. No system tray or startup service yet.
- Automated checks cover audio format, attack/fade, variations, burst
  playback, rhythm accents/reset, rapid-tail selection, shotgun sample
  bounds, mute, repeat suppression, F8 routing and event forwarding.
  Native mixer initialization and shutdown are also checked locally.
  Real speaker latency and typing elsewhere need a hands-on check;
  no end-to-end latency measurement has been made. Try laptop speakers
  or wired headphones when evaluating delay, since Bluetooth adds latency.

## Learn by changing it

Start with the decay numbers in `audio_engine.py` to change the length of
an effect. Then try adding another sound or saving settings in JSON.
Build again after changes to generate an updated EXE.
