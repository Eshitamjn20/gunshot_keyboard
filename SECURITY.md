# Security and contact

KeyBang is an experimental Windows keyboard sound application. Downloads are
paused because Microsoft Defender detected the original release as
`Trojan:Win32/Wacatac.B!ml`. See [the investigation](SECURITY-INVESTIGATION.md).
No vendor clearance has been obtained.

## Report an issue

Contact the maintainer through [GitHub Issues](https://github.com/Eshitamjn20/sounding_keyboard/issues).
Include the app version, SHA-256, antivirus product, definition version and
detection name. Redact usernames, private paths, signed download URLs, account
details and other personal information. Do not attach executable samples to
public issues. This is a public contact channel, not a private disclosure inbox.

## Data handling

The app receives global Windows keyboard events to trigger sounds. It keeps
held-key codes in memory to suppress repeat events, without recording typed
text. It has no account, telemetry, network requests, remote command feature,
automatic updates, or automatic startup service. F8 toggles audio and closing
the window removes the hook. Muting audio does not unregister the hook.

These describe the source behavior, not a certification of packaged binaries.

## Vendor analysis

Use [Microsoft's submission portal](https://www.microsoft.com/en-us/wdsi/filesubmission).
The prepared [submission details](security/MICROSOFT-SUBMISSION.md) distinguish
the flagged original from the locally clean rebuild. GitHub metadata, a clean
local scan, or code signing alone do not establish that a detection is false.
