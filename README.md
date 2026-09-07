# KeyBang

A free, offline Windows keyboard sound toy.

## Try it

Open `dist/KeyBang.exe`, click **Preview sound**, then **Enable sounds**.
Choose Gunshot, Arcade laser, or Soft pop and adjust the volume.
**F8** mutes/unmutes from any normal desktop app. F8 still reaches that app.
Starts muted at 20%. Minimize to keep it running; close to quit.
No administrator access, account, server or paid API is required.

## How it works: a beginner's tour

1. **Interface:** Python's Tkinter draws the window, buttons and slider.
2. **Input:** `KeyboardHook` in `app.py` asks Windows for keyboard events,
   including while other apps are focused. Events pass onward unchanged.
3. **Audio:** `make_sound` combines noise and tones and fades them out.
   These original synthesized effects become temporary WAV files; volume
   changes their amplitude. No third-party sound downloads are needed.
4. **Responsiveness:** The hook queues play/toggle signals. The interface
   checks every 10 ms and Windows plays the sound asynchronously.
5. **Distribution:** PyInstaller bundles Python and the app into one EXE.
   Your friends do not need to install Python.

The listener temporarily tracks held key codes to suppress key repeat.
It never saves typed text and makes no network connections. Closing the
app removes the hook and cleans up temporary audio files.

## Develop and build

With Python 3.14 on Windows:

```powershell
python app.py
python -m unittest -v
.\build.ps1
```

The build script creates a local virtual environment and downloads
PyInstaller. The finished app works offline. Running the source uses
only Python's standard library.

## Share

Send `dist/KeyBang.exe`, or attach it to a GitHub repository release to
provide a download link. No public release has been uploaded yet.
You do not need to distribute `.venv` or `build`.

This build targets Windows 10/11 Intel/AMD 64-bit PCs. Test on another
PC without Python before claiming broader compatibility. The executable
is unsigned, so Windows/antivirus may show a reputation warning. Paid
code signing is optional and outside this free prototype.

## First-version limits and verification

- Fast typing restarts the sound; effects do not overlap. Events inside
  one 10 ms poll are coalesced so old sounds do not build up.
- Holding a key produces one sound, not automatic repeated shots.
- Secure screens and some elevated apps/games may not provide events.
- Settings reset at startup. No system tray or startup service yet.
- Automated checks cover audio format, silence at zero volume, repeat
  suppression, F8 routing, and forwarding events. Real speakers and
  typing in other applications still need a hands-on check.

## Learn by changing it

Start with the decay numbers in `make_sound` to change the length of
an effect. Then try adding another sound or saving settings in JSON.
Build again after changes to generate an updated EXE.
