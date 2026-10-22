# Steady

A private, offline phone app that helps a person ride out anxious urges (to check, text, conclude, react) instead of acting on them, with daily rules, worry parking, a journal, an evidence log and weekly habits. Everything is editable. Nothing leaves the phone.

This is the generic, shareable edition built from `SPEC.md`. It contains no personal content. Steady is a self-help tool, not therapy or medical care.

## In a nutshell

- **Now:** quote of the day, night banner, the SOS button, park a worry, progress.
- **SOS flow:** rate the urge, name it, breathe (animated, 1 to 5 minutes), move, ride the wave (5 to 20 minute timer), rate again. Distress of 9 or 10 shows help numbers without blocking. Leaving mid-flow resumes where you were.
- **Daily:** a checklist that resets at 04:00 (not midnight), one-time setup steps with how-to notes, your own rules.
- **Journal:** fact or story entries, and the "It turned out fine" evidence log.
- **Week:** habits per ISO week, weekly review, checkpoint questions.
- **Help:** why this happens, what helps, when to get help quickly, verified numbers for Estonia, Brazil and Portugal (see `HELP-NUMBERS.md`), your own numbers.
- **Settings:** language (English, Eesti, Português do Brasil), country, theme, night hours, SOS options, three starter packs, an editor for every list, export, import and erase.

## Files

| Path | What it is |
|---|---|
| `index.html` | The whole app: HTML, CSS and JS in one file, about 126 KB, no build step |
| `manifest.webmanifest`, `sw.js`, `icon-*.png` | PWA install and offline support |
| `android/` | apktool project: manifest, resources, the WebView launcher in smali, `build.sh` |
| `tests/e2e.py` | Playwright checks from spec section 15 (15 checks) |
| `SPEC.md` | The brief this was built from |
| `DECISIONS.md` | Every choice the spec left open, with reasons |
| `HELP-NUMBERS.md` | Help numbers with sources and the date checked |
| `REUSE.toml`, `LICENSES/` | The licence of every file and the licence texts |
| `TRADEMARKS.md`, `CONTRIBUTING.md` | Use of the name and icons, and the contributor agreement |
| `CLAUDE.md` | Ground rules for future build sessions |
| `.github/workflows/ci.yml` | CI: `reuse lint`, the character check and `tests/e2e.py` |

## Run, test, build

```sh
python3 -m http.server 8000                         # open http://localhost:8000
CHROME=/path/to/chrome python3 tests/e2e.py         # all checks; add a word to run matching checks only
KS=/path/steady-release.jks KS_PASS=... TOOLS=/dir/with/jars ./android/build.sh
```

`build.sh` needs Java, `apktool.jar` (v2.10.0) and `uber-apk-signer.jar` (v1.3.0) from their GitHub releases. The signing keystore is not in this repository and never should be.

## Status

1.0.1, 2026-10-22. The About screen states the licences (GPL-3.0-or-later, starter texts also CC BY-SA 4.0, name and icons not covered). A CI workflow runs `reuse lint`, a character check and all 15 browser checks on every push and pull request. The test clocks now use Tallinn time on any machine.

1.0.0, 2026-10-14. All 15 automated checks pass at 360 and 390 px, light and dark, in all three languages, including a mocked clock for the daily reset and the week rollover, an offline reload and a run with storage blocked.

Before sharing it widely:
1. **Native review of the Estonian and Portuguese text.** Both were drafted by Claude and are marked in the app as not yet reviewed (spec section 10).
2. **Manual checks on Android 10, 13 and 14:** launch, rotate, background and return, back button, tel: links, screen staying on during timers, large font.
3. **Re-check the help numbers** right before each release.

## Licence

Free software. Each file says which licence covers it in `REUSE.toml` (REUSE standard, checked with `reuse lint`):

- **Code:** GPL-3.0-or-later, including `index.html`. See `LICENSE`.
- **Starter texts:** the quotes, rules, checklists and other starter lists inside `index.html` may also be reused under CC BY-SA 4.0.
- **Documentation:** CC BY-SA 4.0. **Help numbers** (`HELP-NUMBERS.md`): CC BY 4.0.
- **The name, logo and icons** are not licensed for reuse; see `TRADEMARKS.md`. Contributions come with the agreement in `CONTRIBUTING.md`.
