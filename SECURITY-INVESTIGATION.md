# KeyBang antivirus investigation — 2026-09-07

Status: unresolved detection. Public download release remains a draft.
The separate website is an information page with downloads disabled.
Do not redistribute a replacement based only on a clean local scan.

## Exact published build

- File: `release-build/KeyBang.exe`
- Size before scanning: 18,609,521 bytes
- SHA-256: `59cd3345911515016bed56b7c7ef9a19ad14084f36ea5f7e2ca13641775408de`
- Hash matches the hash recorded when v0.1.0 was published.
- Defender custom file scan reproduced one threat and completed remediation.
- Detection: `Trojan:Win32/Wacatac.B!ml`, threat ID `2147735505`.
- Defender reported `ActionSuccess: True`, `IsActive: False`,
  `DidThreatExecute: False`. These are Defender's observations, not a guarantee
  that no prior execution or compromise occurred.
- The file no longer exists at the original path after scanning.
- Antivirus and real-time protection were enabled. Signature version:
  `1.459.88.0`, last updated 2026-09-07 07:15:22 local time.
- No executable was launched, restored, or excluded during this investigation.

## Earlier local build

- File: `dist/KeyBang.exe`
- SHA-256: `ba22ebab63a8dbb0aa615d6539bd155b147b49c87c4bc4548d270b5cb49a9b91`
- Defender custom file scan reported no threats.
- This is a different binary. Its result does not clear the published build
  or prove that either binary is safe. No replacement was published.

## Source and dependency inspection

Reviewed `app.py`, `audio_engine.py` and dependency declarations. The app source
uses a Windows keyboard hook, in-memory key state, a queue, Tkinter and audio
playback. No typed-text persistence, network requests or external command
execution were found in those app modules.

Checked SHA-256 file hashes against installed package RECORD metadata:
PyInstaller 6.22.0 (578 files), pygame-ce 2.5.8 (521),
pyinstaller-hooks-contrib 2026.7 (716), pefile 2024.8.26 (11),
pywin32-ctypes 0.2.3 (39), altgraph 0.17.5 (13), packaging 26.3 (29),
setuptools 84.0.0 (343). No mismatches found.

Local RECORD checks are not independent publisher verification or a malware
audit. The packaged code could not be compared to source after Defender
removed the release executable. Native dependencies were not reverse engineered.

## Conclusion and next step

The antivirus detection is reproducible. Whether it is a false positive is
not established. Microsoft analysis of the exact flagged release is needed:
https://www.microsoft.com/en-us/wdsi/filesubmission

No manual sample submission has been completed. The local flagged file was
removed by Defender; the unpublished GitHub release retains the original
asset. Do not disable protection, restore quarantined files, or alter the
binary merely to avoid detection.

## Fresh environment rebuild — 2026-09-07

Created `clean-build-20260907/venv` with the existing Python 3.14.3 runtime.
Windows verified the Python executable's Authenticode signature as valid.
This uses the same laptop and base Python installation, not an independently
verified machine or a fresh operating system.

Downloaded all eight pinned packages from PyPI without using cached downloads.
Each wheel SHA-256 matched the published PyPI JSON metadata. Installed offline
from those wheels with `--require-hashes`. Verification records and a fully
pinned hash lock are in the ignored `clean-build-20260907/` directory.

Copied the app source, tests and assets to a separate source directory and
used new PyInstaller cache, work and output directories. Kept the original
one-file packaging format and application behavior. All four unit tests passed.

New executable: `clean-build-20260907/dist/KeyBang.exe`

SHA-256: `7eec4dd023db702a202c1903eb3dfb43c9ad08177584b2205ea7ef8d275a392b`

Defender custom scan completed and reported **no threats** for this binary.
The EXE was not executed, uploaded, or published. This local scan is not
independent vendor clearance and does not explain or overturn the original
release detection. Public downloads remain disabled pending further review.

## Repository cleanup and submission preparation

Website files moved to `Eshitamjn20/keybang-website`; app source and binary
release ownership remain in `Eshitamjn20/sounding_keyboard`. The new website
has no active download link. The original app repository's Pages remains off.

Removed obsolete local build output, generated specs, caches, the downloaded
sound-source archive, and the duplicate clean-build environment and wheels.
Retained the clean candidate, copied source, verification script and records
under ignored `clean-build-20260907/`. Published sanitized wheel verification,
hash lock and candidate hash records under `security/evidence/`.

Prepared `security/MICROSOFT-SUBMISSION.md`. The portal requires Microsoft
sign-in; no submission has been confirmed and there is no vendor verdict.
