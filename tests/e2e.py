"""Automated checks from SPEC.md section 15. Run: CHROME=/path/to/chrome python3 tests/e2e.py"""
import json, os, re, subprocess, sys, time, traceback
from datetime import datetime
from playwright.sync_api import sync_playwright, expect

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUT = os.path.join(HERE, 'shots'); os.makedirs(OUT, exist_ok=True)
PORT = 8790
BASE = f'http://127.0.0.1:{PORT}/'
TZ = 'Europe/Tallinn'
results = []

def check(name):
    def wrap(fn):
        def run(b):
            try:
                fn(b); results.append((name, True, '')); print('PASS', name)
            except Exception as e:
                results.append((name, False, str(e)[:500])); print('FAIL', name, '\n', traceback.format_exc()[-1500:])
        run.__name__ = name
        return run
    return wrap

def new_page(b, vp=(390, 844), clock=None, init=None, scheme='light'):
    ctx = b.new_context(viewport={'width': vp[0], 'height': vp[1]}, timezone_id=TZ, locale='en-GB', color_scheme=scheme, accept_downloads=True)
    pg = ctx.new_page()
    pg.errors = []
    pg.requests = []
    pg.on('pageerror', lambda e: pg.errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: pg.errors.append(f'console {m.type}: {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('request', lambda r: pg.requests.append(r.url))
    if init: pg.add_init_script(init)
    if clock: pg.clock.install(time=clock)
    return ctx, pg

def onboard(pg, pack='relationship', show=False):
    pg.wait_for_selector('#obNext')
    pg.click('#obNext')             # welcome
    pg.select_option('#obCountry', 'EE'); pg.wait_for_timeout(50)
    pg.click('#obNext')             # language and country
    pg.click(f'[data-pack="{pack}"]')
    pg.click('#obNext')
    pg.click('#obShow' if show else '#obFinish')
    pg.wait_for_selector('#sosBtn')

def no_overflow(pg):
    return pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')

def last_clear_of_nav(pg):
    # at full scroll, the last control on the page must sit above the floating tab bar
    return pg.evaluate('''(() => {
      window.scrollTo(0, document.documentElement.scrollHeight);
      const nav = document.querySelector('nav.tabs'); if (!nav) return true;
      const els = [...document.querySelectorAll('main button, main a, main input, main textarea')].filter(e => e.offsetParent);
      const last = els[els.length - 1]; if (!last) return true;
      return last.getBoundingClientRect().bottom <= nav.getBoundingClientRect().top;
    })()''')

def tab(pg, name):
    pg.click(f'nav.tabs a[href="#{name}"]')
    pg.wait_for_timeout(120)

TABS = ['now', 'daily', 'journal', 'week', 'help']

@check('onboarding, every tab, no console errors, no horizontal scroll at 360 and 390')
def t_tabs(b):
    for vp in [(360, 740), (390, 844)]:
        for scheme in ['light', 'dark']:
            ctx, pg = new_page(b, vp, scheme=scheme)
            pg.goto(BASE)
            pg.screenshot(path=f'{OUT}/{vp[0]}-{scheme}-0-onboarding.png', full_page=True)
            onboard(pg, show=True)
            if scheme == 'dark':
                pg.goto(BASE + '#settings'); pg.click('.seg button:has-text("Dark")'); pg.wait_for_timeout(100)
                assert pg.evaluate("document.documentElement.dataset.theme") == 'dark'
            for name in TABS + ['settings']:
                pg.goto(BASE + '#' + name); pg.wait_for_timeout(150)
                ow = no_overflow(pg)
                assert ow <= 0, f'{vp} {name} overflows by {ow}px'
                assert last_clear_of_nav(pg), f'{vp} {name}: last control hidden behind the tab bar'
                pg.screenshot(path=f'{OUT}/{vp[0]}-{scheme}-{name}.png', full_page=True)
            assert not pg.errors, pg.errors
            ctx.close()

@check('text at 200 percent keeps the layout without horizontal scroll')
def t_bigtext(b):
    ctx, pg = new_page(b, (360, 740))
    pg.goto(BASE); onboard(pg)
    for name in TABS + ['settings', 'settings/habits']:
        pg.goto(BASE + '#' + name); pg.wait_for_timeout(100)
        pg.evaluate("document.documentElement.style.fontSize = '200%'")
        ow = no_overflow(pg)
        assert ow <= 0, f'{name} overflows by {ow}px at 200 percent'
    pg.screenshot(path=f'{OUT}/360-bigtext-settings-habits.png', full_page=True)
    ctx.close()

@check('SOS flow end to end saves the right before and after, breathing counts down and skip works')
def t_sos(b):
    ctx, pg = new_page(b, clock=datetime(2026, 10, 14, 15, 0, 0))
    pg.goto(BASE); onboard(pg)
    pg.click('#sosBtn')
    pg.wait_for_selector('text=How strong is the urge?')
    assert pg.is_disabled('button:has-text("Next")'), 'Next must be disabled before a value'
    pg.click('.scale button:has-text("8")')
    pg.click('button:has-text("Next")')
    pg.wait_for_selector('text=Name it')
    pg.screenshot(path=f'{OUT}/sos-2-name.png', full_page=True)
    pg.click('button:has-text("Next")')
    pg.wait_for_selector('#breathLeft')
    pg.clock.run_for(1000)
    first = pg.inner_text('#breathLeft')
    pg.clock.run_for(5000)
    second = pg.inner_text('#breathLeft')
    assert first != second and '1:5' in second, f'breath countdown did not move: {first} then {second}'
    assert re.search(r'(In|Out) [46]', pg.inner_text('#orb')), pg.inner_text('#orb')
    pg.screenshot(path=f'{OUT}/sos-3-breathe.png', full_page=True)
    pg.clock.run_for(120000)
    pg.wait_for_selector('text=Done, start the timer')
    pg.click('.chip >> nth=0')
    pg.click('text=Done, start the timer')
    pg.wait_for_selector('#waveLeft')
    w1 = pg.inner_text('#waveLeft'); pg.clock.run_for(3000); w2 = pg.inner_text('#waveLeft')
    assert w1 != w2, 'wave timer did not move'
    pg.screenshot(path=f'{OUT}/sos-5-wave.png', full_page=True)
    pg.click('text=It has passed')
    pg.wait_for_selector('text=How strong is it now?')
    pg.click('.scale button:has-text("3")')
    pg.click('button:has-text("Finish")')
    pg.wait_for_selector('text=From 8 to 3.')
    pg.fill('input[placeholder="What turned out fine?"]', 'The reply came the next morning')
    pg.click('button:has-text("Add")')
    pg.screenshot(path=f'{OUT}/sos-summary.png', full_page=True)
    data = pg.evaluate("JSON.parse(localStorage.getItem('steady_generic_v1'))")
    u = data['records']['urges']
    assert len(u) == 1 and u[0]['before'] == 8 and u[0]['after'] == 3, u
    assert data['records']['evidence'][0]['text'] == 'The reply came the next morning'
    assert data['state']['sosInProgress'] is None
    pg.click('button[aria-label="Close"]')
    pg.wait_for_selector('#sosBtn')
    stats = pg.inner_text('.stats')
    assert '1\nUrges ridden out' in stats and '5.0' in stats, stats
    # skipping every step still saves on step 6
    pg.click('#sosBtn'); pg.wait_for_selector('text=How strong is the urge?')
    for _ in range(5):
        pg.click('button:has-text("Skip")'); pg.wait_for_timeout(80)
    pg.click('button:has-text("Skip")')
    pg.wait_for_selector("text=You didn't act on it.")
    n = pg.evaluate("JSON.parse(localStorage.getItem('steady_generic_v1')).records.urges.length")
    assert n == 2, n
    assert not pg.errors, pg.errors
    ctx.close()

@check('distress 9 or 10 shows the safety card with tappable numbers, without blocking')
def t_safety(b):
    ctx, pg = new_page(b)
    pg.goto(BASE); onboard(pg)
    pg.click('#sosBtn'); pg.click('.scale button:has-text("9")')
    pg.wait_for_selector(".safety >> text=you don't have to handle it alone")
    tels = pg.eval_on_selector_all('.safety a[href^="tel:"]', 'els => els.map(e => e.getAttribute("href"))')
    assert 'tel:112' in tels or 'tel:192' in tels, tels
    assert not pg.is_disabled('button:has-text("Next")')
    pg.screenshot(path=f'{OUT}/sos-1-safety.png', full_page=True)
    ctx.close()

@check('leaving mid-flow and reloading resumes the current step')
def t_resume(b):
    ctx, pg = new_page(b)
    pg.goto(BASE); onboard(pg)
    pg.click('#sosBtn'); pg.click('.scale button:has-text("6")'); pg.click('button:has-text("Next")'); pg.click('button:has-text("Next")')
    pg.wait_for_selector('#breathLeft'); pg.wait_for_timeout(2500)
    pg.reload(); pg.wait_for_selector('#breathLeft')
    left = pg.inner_text('#breathLeft')
    assert 'step 3 of 6' in pg.inner_text('.sosview').lower(), 'did not resume step 3'
    m = re.search(r'(\d):(\d\d)', left); secs = int(m.group(1)) * 60 + int(m.group(2))
    assert secs < 119, f'breathing restarted instead of resuming: {left}'
    pg.click('button[aria-label="Leave the exercise"]'); pg.wait_for_selector('#sosBtn')
    assert 'Continue where you left off' in pg.inner_text('#sosBtn')
    ctx.close()

@check('park a worry for one minute; it comes due; faded counts in stats and offers evidence')
def t_worry(b):
    ctx, pg = new_page(b, clock=datetime(2026, 10, 14, 12, 0, 0))
    pg.goto(BASE + '?test=1'); onboard(pg)
    pg.select_option('#worryDur', '1')
    pg.fill('#worryText', 'They have not answered since lunch')
    pg.click('#parkBtn')
    pg.wait_for_selector('text=Look again at 12:01')
    pg.clock.run_for(66000)
    pg.wait_for_selector('text=Does it still matter?')
    pg.screenshot(path=f'{OUT}/worry-due.png', full_page=True)
    pg.click('text=No, it faded')
    pg.wait_for_selector('text=Add this to your evidence')
    pg.click('.due button:has-text("Add")')
    stats = pg.inner_text('.stats')
    assert '1\nWorries that faded' in stats, stats
    # a second worry kept for the weekly review shows up in Week
    pg.fill('#worryText', 'Second worry'); pg.click('#parkBtn'); pg.clock.run_for(66000)
    pg.wait_for_selector('text=Does it still matter?')
    pg.click('.due button:has-text("Yes")'); pg.click('text=Keep for the weekly review')
    tab(pg, 'week'); pg.wait_for_selector('text=Second worry')
    assert not pg.errors, pg.errors
    ctx.close()

@check('daily checklist resets after the reset time, not at midnight')
def t_daily_reset(b):
    ctx, pg = new_page(b, clock=datetime(2026, 10, 14, 10, 0, 0))
    pg.goto(BASE + '?test=1'); onboard(pg)
    tab(pg, 'daily')
    first = pg.locator('#dailyCard label.check').first
    first.click()
    assert first.locator('input').is_checked()
    pg.clock.fast_forward('17:30:00')       # 03:30 next day, before the 04:00 reset
    pg.clock.run_for(6000)
    assert pg.locator('#dailyCard label.check input').first.is_checked(), 'reset too early'
    pg.clock.fast_forward('01:00:00')       # 04:30
    pg.clock.run_for(6000)
    assert not pg.locator('#dailyCard label.check input').first.is_checked(), 'did not reset after 04:00'
    hist = pg.evaluate("JSON.parse(localStorage.getItem('steady_generic_v1')).state.dailyChecks")
    assert hist.get('2026-10-14', {}).get('d1') is True, hist
    ctx.close()

@check('weekly habits roll over by ISO week, Sunday to Monday')
def t_week(b):
    ctx, pg = new_page(b, clock=datetime(2026, 10, 18, 20, 0, 0))   # Sunday, ISO week 42
    pg.goto(BASE + '?test=1'); onboard(pg)
    tab(pg, 'week')
    assert 'Week 42' in pg.inner_text('#habitsCard')
    pg.locator('#habitsCard .boxes button').first.click()
    assert pg.locator('#habitsCard .boxes button').first.get_attribute('aria-pressed') == 'true'
    pg.clock.fast_forward('14:00:00')       # Monday 10:00
    pg.clock.run_for(6000)
    assert 'Week 43' in pg.inner_text('#habitsCard'), pg.inner_text('#habitsCard')
    assert pg.locator('#habitsCard .boxes button').first.get_attribute('aria-pressed') == 'false'
    wk = pg.evaluate("JSON.parse(localStorage.getItem('steady_generic_v1')).state.weekChecks")
    assert wk['2026-W42']['h1'][0] is True, wk
    # saving a review ticks the review habit
    pg.fill('#rv_0', 'Slept better')
    pg.click('#rvSave')
    pg.wait_for_selector('text=Review saved.')
    data = pg.evaluate("JSON.parse(localStorage.getItem('steady_generic_v1'))")
    rev = [h['id'] for h in data['content']['habits'] if h['isReview']][0]
    assert data['state']['weekChecks']['2026-W43'][rev][0] is True
    ctx.close()

@check('language switch changes visible strings; no missing i18n keys in any language')
def t_lang(b):
    ctx, pg = new_page(b)
    pg.goto(BASE); onboard(pg)
    missing = pg.evaluate('window.SteadyDebug.missingKeys()')
    assert missing == [], missing
    seen = {}
    for code, nav in [('et', 'Päevik'), ('pt-BR', 'Diário'), ('en', 'Journal')]:
        pg.goto(BASE + '#settings'); pg.select_option('#setLang', code); pg.wait_for_timeout(150)
        assert nav in pg.inner_text('nav.tabs'), (code, pg.inner_text('nav.tabs'))
        for name in TABS + ['settings']:
            pg.goto(BASE + '#' + name); pg.wait_for_timeout(100)
            seen[(code, name)] = pg.inner_text('main')
            if code != 'en':
                pg.screenshot(path=f'{OUT}/lang-{code}-{name}.png', full_page=True)
        # starter content follows the language while unedited
        assert nav in pg.inner_text('nav.tabs')
    assert seen[('et', 'daily')] != seen[('en', 'daily')]
    assert 'Telefon on magamistoast väljas' in seen[('et', 'daily')]
    assert 'Celular fora do quarto' in seen[('pt-BR', 'daily')]
    assert not pg.errors, pg.errors
    ctx.close()

@check('edited lists survive a pack change; reset restores starter content')
def t_edit(b):
    ctx, pg = new_page(b)
    pg.goto(BASE); onboard(pg)
    pg.goto(BASE + '#settings/rules')
    pg.locator('#editor textarea').first.fill('My own first rule')
    pg.goto(BASE + '#settings'); pg.click('.pack:has-text("General stress")')
    pg.goto(BASE + '#daily')
    txt = pg.inner_text('main')
    assert 'My own first rule' in txt, 'edited rules were replaced'
    assert 'No checking work mail after hours' in txt, 'unedited checklist did not follow the pack'
    pg.on('dialog', lambda d: d.accept())
    pg.goto(BASE + '#settings/rules'); pg.click('#edReset', timeout=5000)
    pg.goto(BASE + '#daily')
    assert 'Work messages wait until working hours.' in pg.inner_text('main')
    ctx.close()

@check('export, erase, import restores identical data')
def t_roundtrip(b):
    ctx, pg = new_page(b)
    pg.on('dialog', lambda d: d.accept())
    pg.goto(BASE); onboard(pg)
    pg.fill('#worryText', 'Will I manage the move'); pg.click('#parkBtn')
    tab(pg, 'journal'); pg.fill('#j_fact', 'She said she was tired'); pg.fill('#j_story', 'She is losing interest'); pg.click('#jSave')
    pg.fill('#evText', 'The call went fine'); pg.click('#evAdd')
    tab(pg, 'week'); tab(pg, 'daily')
    pg.locator('#dailyCard label.check').nth(2).click()
    pg.goto(BASE + '#settings')
    with pg.expect_download() as dl:
        pg.click('#exportBtn')
    exported = json.load(open(dl.value.path()))
    pg.click('#eraseBtn')
    pg.wait_for_selector('#obSkip')
    assert pg.evaluate("localStorage.getItem('steady_generic_v1')") is None or 'Will I manage' not in pg.evaluate("localStorage.getItem('steady_generic_v1')")
    pg.click('#obSkip')
    pg.goto(BASE + '#settings'); pg.click('#importBtn')
    pg.fill('#importIn', json.dumps(exported))
    pg.click('#importCheck')
    pg.wait_for_selector('text=This file has 0 urges, 1 journal entries, 1 evidence lines and 1 worries.')
    pg.click('#importReplace')
    pg.wait_for_selector('text=Imported.')
    after = pg.evaluate("JSON.parse(localStorage.getItem('steady_generic_v1'))")
    assert after == exported, 'data differs after the round trip'
    ctx.close()

@check('localStorage blocked: app runs in memory and shows the notice')
def t_nostorage(b):
    block = "Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('blocked', 'SecurityError'); } });"
    ctx, pg = new_page(b, init=block)
    pg.goto(BASE); onboard(pg)
    pg.wait_for_selector('text=Saving is not available on this device.')
    pg.fill('#worryText', 'in memory'); pg.click('#parkBtn')
    pg.wait_for_selector('text=in memory')
    assert not [e for e in pg.errors if 'pageerror' in e], pg.errors
    pg.screenshot(path=f'{OUT}/no-storage.png', full_page=True)
    ctx.close()

@check('no network requests beyond the app itself, and it works offline after the first load')
def t_offline(b):
    ctx, pg = new_page(b)
    pg.goto(BASE); onboard(pg)
    for name in TABS + ['settings']:
        pg.goto(BASE + '#' + name); pg.wait_for_timeout(80)
    foreign = [u for u in pg.requests if not u.startswith(BASE) and not u.startswith('data:') and not u.startswith('blob:')]
    assert not foreign, foreign
    pg.goto(BASE + '#now')
    pg.evaluate('navigator.serviceWorker.ready.then(() => true)')
    pg.wait_for_timeout(500)
    pg.reload(); pg.wait_for_selector('#sosBtn')
    ctx.set_offline(True)
    pg.reload(); pg.wait_for_selector('#sosBtn')
    ctx.set_offline(False)
    ctx.close()

@check('Android mode (file:// as in the APK) loads without errors and exports to a text box')
def t_file(b):
    ctx, pg = new_page(b)
    pg.goto('file://' + os.path.join(ROOT, 'index.html')); onboard(pg)
    pg.goto('file://' + os.path.join(ROOT, 'index.html') + '#settings')
    pg.click('#exportBtn'); pg.wait_for_selector('#exportOut')
    assert '"schema": 1' in pg.input_value('#exportOut')
    tab(pg, 'help')
    assert pg.locator('a[href="tel:112"]').count() >= 1
    assert not pg.errors, pg.errors
    ctx.close()

@check('build has no em dashes, en dashes or ellipses, and stays under 150 KB')
def t_chars(b):
    s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    bad = [c for c in ['—', '–', '…', '...'] if c in s]
    assert not bad, bad
    size = len(s.encode('utf-8'))
    assert size < 150 * 1024, size

if __name__ == '__main__':
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
            only = sys.argv[1:]
            for fn in [t_tabs, t_bigtext, t_sos, t_safety, t_resume, t_worry, t_daily_reset, t_week, t_lang, t_edit, t_roundtrip, t_nostorage, t_offline, t_file, t_chars]:
                if not only or any(o in fn.__name__ for o in only):
                    fn(b)
            b.close()
    finally:
        srv.terminate()
    failed = [r for r in results if not r[1]]
    print(f'\n{len(results) - len(failed)} of {len(results)} checks passed')
    for r in failed: print('FAILED:', r[0], '|', r[2])
    sys.exit(1 if failed else 0)
