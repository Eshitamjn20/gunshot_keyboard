# Microsoft submission draft

Status: prepared, not submitted. Do not describe this as Microsoft clearance.

Portal: https://www.microsoft.com/en-us/wdsi/filesubmission

| Field | Value |
| --- | --- |
| Submit as | Software developer |
| Developer/company | Eshitamjn20 (independent developer) |
| Product | Microsoft Defender Antivirus (Windows 11) |
| Detection name | Trojan:Win32/Wacatac.B!ml |
| Recorded definition version | 1.459.88.0 |
| Application | KeyBang |
| Source | https://github.com/Eshitamjn20/sounding_keyboard |
| Public contact | https://github.com/Eshitamjn20/sounding_keyboard/issues |

## Additional information (under 1,900 characters)

I maintain KeyBang, a free Windows keyboard sound application. Please review a
suspected false positive; I am not asserting that the detection is incorrect.
Defender identified the original v0.1.0 KeyBang.exe as Trojan:Win32/Wacatac.B!ml.
The detection reproduced on a local custom scan with definitions 1.459.88.0,
and Defender removed the file. The public download has been withdrawn.

Original SHA-256:
59cd3345911515016bed56b7c7ef9a19ad14084f36ea5f7e2ca13641775408de

The source uses a Windows low-level keyboard hook to enqueue sound events,
Tkinter for the UI, and pygame-ce for audio. It tracks held key codes in
memory, does not save typed text, makes no network requests and has no remote
command functionality. It is packaged with PyInstaller 6.22.0 / Python 3.14.3.

A fresh virtual environment on the same laptop, with wheel hashes verified
against PyPI metadata, produced a different binary that passed a local scan:
7eec4dd023db702a202c1903eb3dfb43c9ad08177584b2205ea7ef8d275a392b
This is not the originally detected sample and does not resolve that detection.

Source and investigation:
https://github.com/Eshitamjn20/sounding_keyboard
https://github.com/Eshitamjn20/sounding_keyboard/blob/main/SECURITY-INVESTIGATION.md
Please advise on the original detection and whether further samples are needed.

## Sample selection

The original flagged sample is retained in the unpublished GitHub release;
Microsoft cannot access that draft through its normal public URL. Its local
copy was removed by Defender. Do not restore it or disable protection merely
to submit. If the portal requires the original file, request vendor guidance
for supplying the quarantined sample or refer to the exact original hash.

The clean-build candidate is a separate sample. If submitted for validation,
identify it explicitly as the rebuild, retain its hash and do not claim the
original detection occurred on it. A clean verdict on it does not clear v0.1.0.

Submission tracking: record the ID and result here after the portal confirms
receipt. No submission ID exists yet. The signed-in Microsoft account/contact
email must be supplied by the maintainer and kept out of public source history.

## Manual submission steps

1. Visit the portal above. Choose **Software developer**, then sign in.
2. Choose **Microsoft Defender Antivirus (Windows 11)** and enter
   **Eshitamjn20** as the developer/company name.
3. Select the exact sample you want analyzed. The sole current local EXE is
   `dist/KeyBang.exe`: it is the clean rebuild, not the originally flagged file.
   Do not claim that the earlier detection occurred on this new hash.
4. If submitting the original detected file, use **Incorrectly detected as
   malware/malicious** as your suspected classification, detection
   `Trojan:Win32/Wacatac.B!ml`, and definitions `1.459.88.0`. This is a request
   for review, not a claim that Microsoft has already confirmed a false positive.
5. Paste the Additional information text above. For the rebuilt sample, add:
   "The attached file is the clean rebuild with SHA-256 7eec4dd023db702a202c1903eb3dfb43c9ad08177584b2205ea7ef8d275a392b.
   It passed a local scan. The original detection concerns the other hash in
   this report; please validate this candidate and advise on the original."
6. Review the form, submit, and save the confirmation/submission ID. Track the
   result through the portal's submission history. Keep downloads paused.

If the portal offers no appropriate category for validating an undetected
candidate, do not mislabel it. Request guidance through the portal help using
both hashes. Reviewing the rebuilt sample cannot establish a verdict on the
original. If the original is unavailable because Defender removed it, explain
that; do not disable Defender or restore the sample merely to fill the form.
