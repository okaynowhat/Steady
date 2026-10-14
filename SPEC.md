# Steady: product and technical specification (generic, customisable edition)

Version 1.0 of this spec, written 14 Oct 2026.
Purpose: a complete brief for building a generic, shareable version of the personal "Steady" app in a fresh session.
Perspectives used: clinical psychology (CBT, ACT, DBT skills, anxiety and attachment), product management, UX and accessibility, privacy and security, Android engineering, localisation.

---

## 1. Summary

Steady is a private, offline phone app that helps a person get through moments of anxious urges and emotional overwhelm, especially in relationships and life transitions (new relationship, breakup, separation, waiting for replies, checking someone's online status, rumination at night).

It does three things:
1. **In the moment:** a short guided flow that helps the person ride out an urge (to check, text, conclude, react) instead of acting on it.
2. **Day to day:** simple rules, a daily checklist and a worry-parking tool that reduce triggers and impulsive actions.
3. **Over time:** a journal, an evidence log and weekly habits that build self-trust and a fuller life outside the trigger.

Everything is editable by the user. Nothing leaves the phone.

The generic edition contains **no personal content** from the original owner. It ships with neutral starter content and lets each user write their own.

---

## 2. Goals and non-goals

### Goals
- Help users pause between urge and action (the core skill).
- Reduce checking, reassurance seeking and late-night conclusions.
- Make the user's own rules and insights visible at the right moment.
- Build a counterweight to anxiety: evidence that worries often do not come true.
- Encourage a balanced life: sleep, movement, social contact, own interests.
- Be fully customisable, multilingual (English, Estonian, Brazilian Portuguese at launch) and private.
- Install as an Android APK and as a PWA from a single codebase.

### Non-goals
- Not a medical device, therapy, diagnosis or treatment. Must say so clearly.
- No accounts, cloud sync, analytics, ads or tracking.
- No social features, no sharing of entries.
- No monitoring of other people (no tracking of a partner's online status, no message analysis of others). The app must never become a tool for surveillance.
- No AI chat in v1.

---

## 3. Target users and personas

1. **The anxious partner (primary).** In a new or uncertain relationship. Checks "last seen", reads meaning into reply times, spirals at night, swings between extremes. Needs: a pause button, rules, evidence, sleep protection.
2. **The person going through separation.** Living through divorce or breakup, possibly still under the same roof, lonely, guilty, overloaded. Needs: grounding, daily structure, permission to rest, help resources, a place to put feelings.
3. **The generally stressed.** Work and family overload, rumination. Needs: breathing, worry parking, habits.

Users may be bilingual, low on energy, reading on a phone with one hand, often at night. Design for 30-second interactions.

---

## 4. Clinical foundation (expert notes for content and behaviour)

The app draws on well-established, low-risk self-help techniques. Content must stay at self-help level.

| Technique | Source tradition | Where used |
|---|---|---|
| Urge surfing (ride the wave, urges peak and pass in about 10 to 20 minutes) | Mindfulness-based relapse prevention, ACT | SOS flow step 6 |
| Slow breathing with a longer exhale (for example 4 in, 6 out, about 6 breaths a minute) | Physiology of the vagal "brake", widely used in CBT and DBT | SOS flow step 3, standalone breathing |
| Labelling ("this is anxiety, not information") | Affect labelling, ACT defusion | SOS flow step 2, quotes |
| Postponing a worry (worry time, two-hour rule) | CBT for generalised anxiety | Park a worry |
| Fact versus story (separating events from interpretations) | CBT thought records | Journal |
| Behavioural activation, movement, opposite action | CBT, DBT | SOS step 5, weekly habits |
| Reducing safety behaviours (checking, reassurance seeking) | CBT for anxiety and OCD spectrum | Rules, daily checklist, stats |
| Sleep hygiene, no decisions at night | CBT-I basics | Night mode |
| Self-compassion | Compassion-focused therapy | Copy tone, after-flow messages |

### Principles for all content
- Warm, plain, short sentences. No jargon. No blame.
- Never imply the other person is good or bad. The app does not judge relationships; it helps the user act from calm.
- Never promise outcomes ("she will reply"). Speak about the user's own actions and feelings.
- Never encourage checking, testing or confronting someone.
- Normalise: "This is common", "Urges pass".
- Every content text must be editable or hideable by the user, except the safety screen.

### Safety requirements (non-negotiable)
- A permanent, easy-to-reach **Help** screen with: when to seek help, emergency number, local helplines, and a sentence that the app is not therapy.
- If a user rates distress 9 or 10 in the SOS flow, show a gentle extra card: "If this feels like too much, you don't have to handle it alone" with the help numbers, without blocking the flow.
- No content about self-harm methods. If a user writes such content in the journal, the app does not analyse text (no text analysis at all), but the Help screen is always one tap away.
- Help numbers must be verified per country before each release (see section 13).

---

## 5. Information architecture

Bottom navigation with five tabs (icons plus labels):

1. **Now**: quote of the day, night banner, SOS button, park a worry, stats.
2. **Daily**: today's checklist (resets each morning), one-time setup checklist, my rules.
3. **Journal**: fact or story, evidence it turned out fine, past entries.
4. **Week**: weekly habits, weekly review, checkpoint questions.
5. **Help**: why this happens, what helps over time, get help, settings entry, data.

Settings opens from the Help tab and from a small gear icon in the header.

---

## 6. Features in detail

### 6.1 Header
- App name, today's date in the user's locale.
- Gear icon opens Settings.

### 6.2 Night mode banner
- Shown when local time is within the user's night window (default 22:00 to 07:00, editable).
- Default text: "Night thoughts are not data. No big conclusions until morning. Phone face down, out of the bedroom."
- Re-evaluated every minute.
- Optional setting: during night hours, the SOS flow adds the line "It's late. Most things look different in the morning."

### 6.3 Quote of the day
- Picks one quote per day from the user's quote list, rotating by day number.
- Starter list of about 12 neutral quotes (see section 9). User can add, edit, delete, reorder.

### 6.4 SOS flow ("I feel the urge")
A large primary button on the Now tab. Label editable (default: "I feel the urge to check or react"). Subtitle: "A few calm minutes, step by step."

Steps, with a progress indicator (6 segments):

1. **Rate the urge** 0 to 10 (11 large tap targets). Next is disabled until a value is chosen.
   - If 9 or 10: show the safety card (section 4) below the scale.
2. **Name it.** Title "Name it". Body (editable): "This is anxiety, not information." plus 2 or 3 short lines explaining why acting now won't help (default: "Checking or texting now won't bring the calm you're looking for. Whatever you find will feed the worry.").
3. **Breathe** for a configurable duration (default 2 minutes; options 1, 2, 3, 5). Animated circle: grows on the in-breath, shrinks on the out-breath. Pattern configurable (default 4 seconds in, 6 out; options 4 to 6, 4 to 7, box 4 to 4 to 4 to 4). Text inside the circle: "In 4", "Out 6". Countdown below. Skip button. Optional gentle vibration at phase changes (Android only, if enabled).
4. **Move.** Shows the user's movement list (default: walk around the block; stairs or 15 push-ups; drink a glass of water outside; do something with your hands; 10 minutes of a hobby; time with your child or pet). User picks or just taps "Done, start the timer".
5. **Ride the wave.** Countdown timer (default 15 minutes, options 5, 10, 15, 20). Text: "Urges peak and pass if you don't feed them." Button "It has passed". Keeps the screen awake while running (Android: FLAG_KEEP_SCREEN_ON is set app-wide; PWA: Wake Lock API where supported, wrapped in try/catch).
6. **Check in.** Rate again 0 to 10. Finish.

After finishing: summary card "From X to Y. You didn't act on it. That's the skill." plus "Add to evidence log?" shortcut. Saves a record (section 8).

Rules:
- Any step can be skipped; the record still saves if the user finishes step 6.
- Leaving the app mid-flow and returning resumes the current step (store flow state).
- No sounds by default.

### 6.5 Park a worry (worry postponement)
- Text field "What is the worry?" and button "Park it for 2 hours" (duration editable: 30 min, 1 h, 2 h, 4 h, until tomorrow morning).
- Parked worries list shows text, parked time and "Look again at HH:MM".
- When due: shows "Does it still matter?" with two buttons:
  - "No, it faded" (marks dissolved, counts in stats).
  - "Yes" opens a small choice: "Plan to raise it calmly in person", "Write it in the journal", "Keep for the weekly review".
- Optional (Android v1.1): local notification when due. In v1 the list updates on open and every minute while open.

### 6.6 Stats card
Three tiles:
- Urges ridden out (count of finished SOS flows).
- Average drop in intensity (mean of before minus after, one decimal).
- Worries that faded.
Optional fourth tile toggle: "Days without checking" (from daily checklist item flagged as "no checking").
Stats must be encouraging, never punishing. No streak-breaking shame; show "best run" rather than "streak lost".

### 6.7 Daily checklist
- List of items that reset every local morning at the user's chosen reset time (default 04:00 to avoid midnight confusion).
- Starter items (editable): no checking online status today; no follow-up message within two hours; no big conclusions at night; phone out of the bedroom; moved my body; something just for me.
- Round checkboxes, checked items fade with strikethrough.
- History kept per day (for the weekly review).

### 6.8 One-time setup checklist
- Items that stay checked once done. Starter items (editable): hide "last seen" and read receipts in your messaging app; mute the chat that triggers you during work hours; book a counsellor or therapist; message one friend; set a bedtime alarm.
- Each item can have an optional "How to" note (for example, the steps to hide last seen in WhatsApp). Keep these generic and editable, because app menus change.

### 6.9 My rules
- An ordered list of short rules the user writes for themselves (for example texting rules).
- Starter rules (generic, editable): one question at a time; no follow-up within two hours; heavy topics only in person; one apology is enough; silence is not a message; judge by actions over weeks, not single messages.
- Shown on the Daily tab. Optionally one random rule appears in the SOS flow step 2.

### 6.10 Journal: fact or story
Fields:
- What actually happened (facts only).
- The story I'm telling myself.
- A kinder or likelier explanation.
- Optional: emotion and intensity 0 to 10.
- Optional: what I'll do (or not do).
Saved with timestamp. List newest first, each entry can be edited or deleted (with confirm).

### 6.11 Evidence log ("It turned out fine")
- One-line entries: moments when a worry did not come true.
- Shortcut from SOS summary and from "No, it faded".
- Shown on Journal tab. Optionally, one random evidence line appears in SOS step 2 ("Remember: ...").
- This is a key feature: it builds self-trust over time.

### 6.12 Weekly habits
- Habits with target counts per ISO week (Monday start, configurable to Sunday).
- Starter habits: exercise 3x; one social contact outside the relationship 1x; one evening fully for myself 1x; weekly review 1x.
- Tap boxes to mark. Resets each new week; history kept.

### 6.13 Weekly review
Prompts (editable):
- What went well?
- What worried me?
- Which worries came true?
- One thing for next week.
Saving marks the "weekly review" habit as done. Past reviews listed.

### 6.14 Checkpoint questions
- A user-defined set of questions for a calm, rested reflection on a chosen date (for example "Do I feel good with this person in person?").
- Optional checkpoint date with a reminder banner on that day.
- Starter questions are neutral and relationship-agnostic:
  - Do I feel good and safe with this person in person?
  - Are plans usually kept or replaced with a new date?
  - Is effort mutual?
  - Have my clearly stated needs been met halfway?
  - How is my sleep and wellbeing overall?
- Copy: "Answer on a rested day, not at night."

### 6.15 Help tab
Sections (editable except "Get help quickly"):
- **Why this happens** (psychoeducation, 5 bullets): uncertainty triggers the alarm system; old hurts make silence feel dangerous; stress and poor sleep amplify everything; early stages are the most uncertain; checking gives on-and-off relief, which makes it compulsive.
- **What helps over time**: sleep first; move; people outside the relationship; your own projects; a counsellor; legal or practical advice for big decisions; use AI or friends for decisions, not for constant reassurance.
- **Get help quickly if** (fixed): several nights without sleep; worry takes over most of the day or affects work or children; feeling hopeless or overwhelmed; any thoughts of harming yourself. Then: contact a doctor, counsellor or someone you trust the same week. In an emergency call the emergency number.
- Country-specific numbers (tap to call via tel: links).
- Disclaimer: "Steady is a self-help tool, not therapy or medical care."

### 6.16 Settings
- Language: English, Eesti, Português (Brasil). Default from device locale, fallback English.
- Country for help numbers: Estonia, Brazil, Portugal, Other (custom numbers).
- Name or nickname (optional, used in greetings).
- Theme: Light (default), Dark, System.
- Night window start and end.
- Daily reset time. Week starts on Monday or Sunday.
- SOS settings: breathing pattern, breathing duration, wave timer length, vibration on or off, show a rule or evidence line in step 2.
- Content editors: quotes, rules, daily checklist, one-time setup, movement list, weekly habits, review prompts, checkpoint questions, help texts.
- Starter pack picker (see 6.17), with "Reset to starter content" per list.
- Data: export, import, erase all (double confirm).
- About: version, privacy statement, disclaimer, licences.

### 6.17 Starter packs (themes)
On first launch the user picks one (changeable later). Each pack pre-fills editable lists:
- **Relationship worries** (checking, waiting for replies, new relationship).
- **Separation or breakup** (grief, guilt, loneliness, co-parenting stress, no rushing big decisions).
- **General stress** (work and life overload, rumination).
Packs differ mainly in quotes, rules, checklist items and checkpoint questions. Structure is identical.

### 6.18 Onboarding (first launch, 4 short screens, skippable)
1. Welcome: what Steady is and is not (self-help, private, offline).
2. Pick language and country.
3. Pick a starter pack.
4. Optional: set night window, and a one-tap tour of the SOS button.
Then land on Now.

---

## 7. Design system

Based on Steady 1.2 (calm, light, elegant). Keep it.

### Tokens (light)
- bg #f7f5f0, bg2 #eef2ee (top gradient), card rgba(255,255,255,.8)
- ink #2e3a36, muted #7d8a85, line #e7e4dc
- accent #6f9a8d, accent-deep #4f7d70, accent-soft #e6efeb
- warm #b07a5a, warm-soft #f7ece4 (night banner, safety card)
- shadow: 0 1px 2px rgba(46,58,54,.04), 0 8px 24px rgba(46,58,54,.06)

### Tokens (dark, new for this edition)
- bg #141a18, bg2 #18201d, card rgba(30,38,35,.85)
- ink #e6ece9, muted #9aa6a1, line #2a3330
- accent #8fbcae, accent-deep #b4d8cc, accent-soft #23332e
- warm #e0a882, warm-soft #3a2c22
Dark mode must keep at least WCAG AA contrast.

### Typography
- Headings and quotes: Georgia, "Noto Serif", serif (system fonts only, no downloads).
- Body: "Segoe UI", Roboto, system-ui, sans-serif. Base 16px, line-height 1.6.
- Section labels: 12 to 13px uppercase, letter-spacing .08em, muted.

### Components
- Cards: radius 22px, padding 20px, soft shadow, no borders.
- Primary button: pill shape; SOS button is full-width, radius 22px, gradient #7fa99c to #5e8b7e.
- Ghost button: transparent with 1px accent inset.
- Checkboxes: 22px circles; checked: filled accent with white tick.
- Bottom nav: floating, 12px from edges, radius 24px, blurred white, active tab with soft accent pill. Line icons (inline SVG, stroke 1.6).
- Breathing orb: radial gradient white to #c9ddd6, halo rings; scale .62 to 1.0; in-breath transition 4s, out 6s (follows chosen pattern).
- Transitions: 0.3s fade and 4px rise on tab change. Respect prefers-reduced-motion (disable animations, keep breathing as text countdown).

### Writing style in UI
- Short, kind, second person ("you") or first person in checklists ("Moved my body").
- No em dashes and no ellipses in any UI text, in any language.
- No exclamation-heavy cheerleading.

---

## 8. Data model

Single JSON document stored locally. Key: `steady_generic_v1`.

```json
{
  "schema": 1,
  "settings": {
    "lang": "en",
    "country": "EE",
    "name": "",
    "theme": "light",
    "night": { "start": "22:00", "end": "07:00" },
    "dailyReset": "04:00",
    "weekStart": 1,
    "sos": { "pattern": [4, 0, 6, 0], "breathSec": 120, "waveMin": 15, "vibrate": false, "showRule": true, "showEvidence": true },
    "pack": "relationship",
    "onboarded": true
  },
  "content": {
    "quotes": [ { "id": "q1", "text": "This is anxiety, not information." } ],
    "rules": [ { "id": "r1", "text": "One question at a time." } ],
    "daily": [ { "id": "d1", "text": "No checking online status today", "noChecking": true } ],
    "once": [ { "id": "o1", "text": "Hide last seen and read receipts", "howTo": "" } ],
    "moves": [ { "id": "m1", "text": "Walk around the block" } ],
    "habits": [ { "id": "h1", "text": "Exercise", "target": 3, "isReview": false } ],
    "reviewPrompts": [ "What went well?", "What worried me?", "Which worries came true?", "One thing for next week" ],
    "checkpoint": { "date": null, "questions": [ "Do I feel good and safe with this person in person?" ] },
    "help": { "why": [], "helps": [], "customNumbers": [] }
  },
  "state": {
    "dailyChecks": { "2026-10-14": { "d1": true } },
    "onceDone": { "o1": true },
    "weekChecks": { "2026-W42": { "h1": [true, false, false] } },
    "sosInProgress": null
  },
  "records": {
    "urges": [ { "id": "u1", "t": 1791900000000, "before": 8, "after": 3, "night": false } ],
    "worries": [ { "id": "w1", "t": 1791900000000, "text": "...", "dueAt": 1791907200000, "status": "parked|faded|kept", "keptAction": null } ],
    "journal": [ { "id": "j1", "t": 1791900000000, "fact": "", "story": "", "alt": "", "emotion": "", "intensity": null, "action": "" } ],
    "evidence": [ { "id": "e1", "t": 1791900000000, "text": "" } ],
    "reviews": [ { "id": "rv1", "t": 1791900000000, "answers": ["", "", "", ""] } ]
  }
}
```

Rules:
- IDs: short random strings (crypto.getRandomValues), not timestamps.
- Dates for daily checks use the local date after applying the daily reset time.
- ISO week keys "YYYY-Www".
- Migrations: `schema` integer; a `migrate(data)` function upgrades older versions on load.
- Storage: localStorage for v1 (data is small), every read and write wrapped in try/catch with an in-memory fallback. If storage fails, show a small non-blocking notice "Saving is not available on this device".
- Debounce writes (300 ms) for text fields.

---

## 9. Starter content (English; translate with native review)

### Quotes (relationship pack)
1. This is anxiety, not information.
2. Checking can't give me the calm I'm looking for.
3. Silence is not a message.
4. Judge by actions in person, over weeks.
5. The pressure is my alarm system, not a fact about them.
6. Every urge I ride out teaches my brain that waiting is survivable.
7. Fewer, lighter messages. More real time together.
8. Say needs out loud, calmly, in person.
9. Sleep first. Everything looks heavier at 4 am.
10. I can feel this and still choose what I do.
11. Most worries never happen.
12. Be kind to yourself. This is hard.

### Quotes (separation pack, additions)
- Grief comes in waves. Let this one pass.
- I don't have to decide my whole future tonight.
- Guilt means I care. It doesn't mean I'm bad.
- One small good thing today is enough.

### Movement list
Walk around the block; stairs or 15 push-ups; a glass of water outside; something with your hands (dishes, tidying); 10 minutes of a hobby; play with your child or pet; stretch for 5 minutes.

### Psychoeducation ("Why this happens")
- Uncertainty switches on the brain's alarm system. A silent phone is pure uncertainty.
- Old hurts can make silence feel like danger, even when nothing is wrong.
- Stress, loneliness and poor sleep amplify every feeling.
- The early stage of a relationship, or a big life change, is when uncertainty is highest.
- Checking gives a quick, unreliable relief, which is exactly what makes it a habit.

---

## 10. Localisation

- Languages at launch: `en`, `et`, `pt-BR`.
- All UI strings in a single `i18n` object keyed by language. No hard-coded strings in markup.
- Starter content per language and per pack.
- Dates and times via `Intl.DateTimeFormat` with the chosen locale.
- Translations must be reviewed by a native speaker before release; mark machine-drafted strings with a `// review` comment.
- Portuguese should be Brazilian Portuguese, warm and informal ("você").
- Estonian: informal "sina".
- No em dashes or ellipses in any language.

---

## 11. Help numbers per country (VERIFY BEFORE EVERY RELEASE)

| Country | Emergency | Health advice | Emotional support (verify) |
|---|---|---|---|
| Estonia (EE) | 112 | Family doctor advice line 1220 | Verify current national emotional support line before shipping |
| Brazil (BR) | 192 (SAMU), 190 (police) | | CVV 188 (verify) |
| Portugal (PT) | 112 | SNS 24: 808 24 24 24 (verify) | Verify current line |
| Other | user-entered | user-entered | user-entered |

Rules: never ship an unverified number as fact. If unverified, show only the emergency number plus "Add your local helpline in Settings".

---

## 12. Privacy and security

- No network requests at all in the Android build. The WebView loads only `file:///android_asset/`.
- No INTERNET permission in the Android manifest (WebView works for local files without it). External tel: links open the dialer via an intent.
- PWA: service worker caches the app shell only. No analytics, no fonts or scripts from CDNs.
- Data stays in app storage. Uninstalling deletes it. Explain this in Settings.
- Export: JSON file download (PWA) or share sheet (Android, v1.1). In v1 Android, export copies JSON to clipboard and shows it in a text box for manual saving.
- Import: paste JSON, validate schema, preview counts, confirm, then replace or merge.
- Optional app lock (v1.1): PIN stored as a salted hash (Web Crypto PBKDF2); the screen blurs when the app goes to background.
- Privacy statement text: "Steady stores everything only on this phone. It has no account, no internet access and no tracking. If you uninstall it, your entries are deleted."

---

## 13. Accessibility (WCAG 2.2 AA)

- Tap targets at least 44 by 44 px.
- Contrast at least 4.5:1 for body text in both themes.
- All icons have labels; nav buttons have text labels.
- Screen reader: proper headings, aria-live for timers ("1 minute left"), aria-pressed on scale buttons.
- prefers-reduced-motion respected.
- Text scales with system font size up to 200 percent without layout breaking.
- No colour-only meaning (checked items also show a tick and strikethrough).

---

## 14. Technical architecture

### Codebase
- One self-contained `index.html` (HTML, CSS, vanilla JS, inline SVG). No frameworks, no build step. Target under 150 KB.
- Modules inside the script: `store` (load, save, migrate), `i18n`, `router` (tabs), `sos`, `worries`, `daily`, `journal`, `week`, `help`, `settings`, `onboarding`, `ui` (helpers).
- PWA files: `manifest.webmanifest`, `sw.js`, icons (192 and 512 PNG, maskable).

### Android packaging (proven route from the personal build)
Lesson learned: a hand-assembled APK (custom DEX and binary XML) installed but crashed on launch. The working route was apktool plus smali plus uber-apk-signer.

- Project folder for apktool:
  - `AndroidManifest.xml`: package `ee.steady.calm` (different from the personal `ee.steady.app` so both can coexist), label `@string/app_name`, icon `@drawable/ic_launcher`, theme `@style/AppTheme`, single exported launcher activity `ee.steady.calm.MainActivity`, `configChanges="orientation|screenSize|keyboardHidden"`, `windowSoftInputMode="adjustResize"`. No INTERNET permission.
  - `apktool.yml`: minSdk 26, targetSdk 34, versionCode and versionName, `doNotCompress: [resources.arsc, png]`.
  - `res/values/strings.xml`, `res/values/styles.xml` (parent `Theme.DeviceDefault.Light.NoActionBar`, light status and navigation bars, windowBackground #eef2ee), `res/values-night/styles.xml` for dark, `res/drawable-xxhdpi/ic_launcher.png` (144 px).
  - `smali/ee/steady/calm/MainActivity.smali`: onCreate creates a WebView, enables JavaScript, DOM storage and file access, adds FLAG_KEEP_SCREEN_ON, sets a WebViewClient that opens `tel:` and `http(s):` links via ACTION_VIEW intents, loads `file:///android_asset/index.html`, and handles the back button (WebView goBack, else finish).
  - `assets/index.html` (copied from the web build).
- Build: `java -jar apktool.jar b <dir> -o unsigned.apk`
- Sign and align: `java -jar uber-apk-signer.jar -a unsigned.apk --ks <keystore> --ksAlias <alias> --ksPass <pass> --ksKeyPass <pass>` (v2 and v3 signatures).
- Tools come from official GitHub releases (Apktool v2.10.0, uber-apk-signer v1.3.0). Google Maven and Gradle downloads are blocked in that environment.
- Use a new keystore for this app, kept safe. Keep the same key for all future updates.
- Alternative for developers with Android Studio: a standard Gradle WebView project (Java MainActivity, assets/index.html).

### Optional native bridge (v1.1)
A small JavaScript interface for: local notifications (parked worry due, night reminder), vibration, share sheet export. Must not add network access.

---

## 15. Testing and acceptance

### Automated (Playwright, Chromium, viewport 390 by 844 and 360 by 740)
- No console errors on load and in every tab.
- No horizontal scroll at 360 px.
- SOS flow completes end to end; record saved with correct before and after.
- Breathing timer counts down and advances; skip works; resume after reload restores the step.
- Park a worry with a 1-minute test duration; due state appears; "faded" increments stats.
- Daily checklist resets after the reset time (mock the clock).
- Week rollover by ISO week (mock the clock across Sunday to Monday).
- Language switch changes all visible strings; no missing keys (test fails on any missing i18n key).
- Export then erase then import restores identical data.
- localStorage disabled: app still works in memory and shows the notice.
- Grep build output for em dashes and ellipses: must be zero.

### Manual on device
- Install APK on Android 10, 13 and 14 or newer.
- Launch, rotate, background and return, back button.
- tel: links open the dialer.
- Screen stays on during timers.
- Dark mode and large font.

### Acceptance criteria (v1)
1. A first-time user can complete onboarding and an SOS flow in under 3 minutes without help.
2. Every starter list is editable and resettable.
3. All three languages are complete and reviewed.
4. No network requests (verified with the Android build having no INTERNET permission and the web build passing an offline test).
5. Help screen reachable in one tap from any tab and shows verified numbers or the safe fallback.

---

## 16. Roadmap

- **v1.0:** everything above except items marked v1.1.
- **v1.1:** local notifications, PIN lock, share-sheet export, vibration on breath phases.
- **v1.2:** simple charts (urge intensity over weeks), more packs (social anxiety, grief), widget for the SOS button.
- **Later, only if wanted:** encrypted personal sync (for example via Nostr with the user's own keys), never default.

---

## 17. Prompt for the build session

Paste this into the new session together with this file:

> Build the app described in Steady_Generic_Spec.md. Start with index.html (all features of v1.0, English first, then Estonian and Brazilian Portuguese strings marked for review). Test it with Playwright at 360 and 390 px widths using the test list in section 15. Then package it as an Android APK using the apktool, smali and uber-apk-signer route in section 14, with package ee.steady.calm and a new keystore. Deliver the HTML, the APK and the keystore details as files. Do not include any personal content. No em dashes or ellipses anywhere.