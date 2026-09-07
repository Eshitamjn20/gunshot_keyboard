# KeyBang

A free, offline Windows app that plays sound effects as you type, with
shotgun audio, volume control, and rhythm accents for fast typing.

## Download without Git or Python

Visit the [KeyBang download website](https://eshitamjn20.github.io/sounding_keyboard/)
or download `KeyBang.exe` from the [latest release](https://github.com/Eshitamjn20/sounding_keyboard/releases/latest).
Open the EXE, preview a sound, and enable sounds. Windows may show a warning
because the app is unsigned.

The website source is in `docs/`. GitHub Pages serves that folder from `main`.
Its download button targets the latest release asset named `KeyBang.exe`.
When publishing updates, build the EXE and attach it under that exact name
to the new release. Keep the sound credits with the app.

## Platform support

| Platform | Supported? |
| --- | --- |
| Windows 10/11, Intel/AMD 64-bit | Current target; developed on Windows 11 with Python 3.14 |
| macOS, including Apple Silicon | No — neither the EXE nor the current source works on macOS |
| Linux | No — the keyboard listener is Windows-specific |

Python source is not automatically cross-platform. `KeyboardHook` in
`app.py` uses Windows `user32`/`kernel32` APIs through `ctypes`. A Mac version
would need a macOS keyboard listener, permission handling for global input,
and a separately built and tested macOS package. That port is not implemented.

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

## Run from Git (Windows)

### Prerequisites

- [Git for Windows](https://git-scm.com/downloads/win).
- [Python 3.14 for Windows](https://www.python.org/downloads/windows/), 64-bit,
  with Tcl/Tk support and the Python launcher. This is the tested version.
- PowerShell and an audio output device.
- Internet for cloning and installing dependencies. The app itself runs offline.

### 1. Clone the repository

Open PowerShell in the folder where you keep projects:

```powershell
git clone https://github.com/Eshitamjn20/sounding_keyboard.git
cd sounding_keyboard
```

### 2. Create an environment and install dependencies

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The `.venv` folder keeps this project's dependencies separate from other
Python projects. These commands use its Python directly, so you do not need
to activate the environment or change PowerShell's execution policy.
If `py` is unavailable but `python --version` reports Python 3.14, use
`python -m venv .venv` for the first command.

### 3. Start the app

From the repository folder:

```powershell
.\.venv\Scripts\python.exe app.py
```

Click **Preview sound**, then **Enable sounds**, and type in another app.
Press **F8** to mute. Keep the window open or minimized; closing it exits.
For later runs, repeat just this command. You do not need to build an EXE
or download the original recording archive to run from source: the processed
sample is included in `assets/shotgun.wav`.

### 4. Get updates

Close KeyBang first, then run these commands from the repository folder:

```powershell
git pull --ff-only
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

If Git reports conflicting local changes or diverged branches, resolve those
before updating; do not discard your work just to run these commands.

## Test and build an EXE (Windows)

Run the automated checks using the environment above:

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

To build a standalone EXE without running a PowerShell script:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --add-data "assets;assets" --name KeyBang app.py
```

The result is `dist/KeyBang.exe`. Close any running copy before rebuilding
because Windows locks running executables. The `--add-data` option includes
the shotgun sample and credits; keep it in the command.

Alternatively, with `python` available on PATH, `./build.ps1` creates the
environment, installs build dependencies and builds the EXE. If PowerShell
blocks scripts, use the explicit commands above.

The build folders and EXE are ignored by Git. A fresh clone has source and
assets, but no `dist` executable until you build one. Recipients of an EXE
need neither Python nor Git.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `py` or `python` is not recognized | Install Python, then reopen PowerShell; use the alternate command described above. |
| `No module named pygame` | Install `requirements.txt` with the same `.venv` Python used to launch the app. |
| `No module named tkinter` | Modify/reinstall the Windows Python installation with Tcl/Tk support. |
| Shotgun asset missing | Keep `assets/shotgun.wav` in the clone; include `--add-data "assets;assets"` when packaging. |
| EXE build says access denied | Close the running KeyBang window before rebuilding. |
| No sound | Enable sounds, raise the app volume, and check KeyBang's level and output device in Windows Volume Mixer. |
| Audio feels delayed | Compare laptop speakers or wired headphones with Bluetooth; close duplicate KeyBang instances. End-to-end latency is not measured. |
| F8 does not toggle | Try Fn+F8 if your keyboard uses media keys by default. Some apps may also act on F8. |
| macOS reports a Windows API error | macOS is not supported by the current source; installing more Python packages will not add the missing listener. |

## Share

Send `dist/KeyBang.exe`, or attach it to a GitHub repository release to
provide a download link. For this update, a local build named
`dist/KeyBang-Shotgun.exe` was also produced; the standard build command
above produces `dist/KeyBang.exe`.
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
