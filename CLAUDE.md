# Steady: notes for future sessions

Read README.md, then SPEC.md, then DECISIONS.md.

## Ground rules

1. Nothing personal in the repository. This is the generic edition: names, places and private stories never go into code, starter content, tests or docs.
2. Every UI string exists in English, Estonian and Brazilian Portuguese. Non-English text stays marked `// review` and shows "not yet reviewed" in the app until a native speaker checks it.
3. Help numbers ship only with a source and the date checked in HELP-NUMBERS.md. Never ship an unverified number as fact.
4. Nothing leaves the phone: no network requests, analytics, fonts, scripts or images from elsewhere.
5. On a release, bump the version in all places together: `VERSION` in index.html, `CACHE` in sw.js and `versionCode`/`versionName` in android/apktool.yml. Add a line to the README status.
6. The signing keystore never enters the repository.
7. Record every decision the spec leaves open as a new row in DECISIONS.md.
8. Licences live in `REUSE.toml`. A new file that is not GPL code gets an entry there; `reuse lint` must pass.

## Writing style

Plain sentences, sentence case. No em dashes, en dashes, ellipses or middle dots, and no arrows between words, in UI text, starter content or docs.

## Completion gate

The CI workflow (`.github/workflows/ci.yml`: `reuse lint`, the character check and `python3 tests/e2e.py`) is green. Look at the screenshots in `tests/shots/` for any screen change, and update the README status.
