# Release process

Current state: hold. The original v0.1.0 release stays in draft. Do not overwrite
its sample; it is evidence for the unresolved detection.

1. Obtain a vendor determination for the flagged sample and document its scope.
   Record the submission ID and date without publishing private account data.
2. Build from reviewed source and verified dependencies in an isolated environment.
   Preserve the source revision, wheel hashes, build command and EXE SHA-256.
3. Run tests and scan the exact candidate with current Defender definitions.
   Do not assume a verdict for one hash applies to another. Recheck the final
   downloaded release artifact before enabling the public download link.
4. Create a new draft release in `Eshitamjn20/sounding_keyboard`. Attach the
   candidate as `KeyBang.exe`, a checksum file and sound credits. Never place
   executable files in the website repository.
5. Once review is resolved and the release is approved, publish that release
   and replace the website's paused status with this asset link:
   `https://github.com/Eshitamjn20/sounding_keyboard/releases/latest/download/KeyBang.exe`
6. Verify the public website, redirect and downloaded hash. Preserve earlier
   reports rather than deleting evidence. A new detection means pause and review.

Website source: `https://github.com/Eshitamjn20/keybang-website`.
GitHub Pages serves its root on `main`. No paid service or custom domain is
required for this setup. Visitors do not need GitHub accounts to view it.
