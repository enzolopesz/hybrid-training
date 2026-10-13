from playwright.sync_api import sync_playwright
from pathlib import Path
import re
base=Path(__file__).resolve().parent.parent
html=(base/'index.html').read_text(encoding='utf-8')
html=re.sub(r'<link[^>]*>', '', html)
html=re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in [320,375,390,430,768]:
  ctx=browser.new_context(viewport={'width':width,'height':844}, device_scale_factor=1, is_mobile=True,has_touch=True,service_workers='block')
  page=ctx.new_page()
  errors=[]
  page.on('pageerror',lambda e: errors.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded')
  page.add_style_tag(content=(base/'styles.css').read_text(encoding='utf-8'))
  page.add_style_tag(content=(base/'fitness-theme.css').read_text(encoding='utf-8'))
  page.evaluate("""() => {const db={}; Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>db[k]||null,setItem:(k,v)=>{db[k]=v},removeItem:k=>delete db[k]}})}""")
  page.add_script_tag(content=(base/'app.js').read_text(encoding='utf-8'))
  page.wait_for_timeout(150)
  assert page.locator('.activity-ring').count()==3
  assert page.locator('.ring-card').count()==3
  for name in ('home','calendar','training','progress','settings'):
   page.locator(f'#nav-{name}').click()
   page.wait_for_timeout(50)
   info=page.evaluate('''() => ({vw:innerWidth, doc:document.documentElement.scrollWidth, body:document.body.scrollWidth, bg:getComputedStyle(document.body).backgroundColor, active:document.querySelector('.bottomnav button.active')?.id, big:[...document.querySelectorAll('input, select,textarea')].filter(x=>x.offsetParent!==null).map(x=>Math.round(x.getBoundingClientRect().right)).filter(x=>x>innerWidth+1)})''')
   assert info['doc']<=width+1, (name,width,info)
   assert not info['big'],(name,width,info)
   assert info['bg']=='rgb(0, 0, 0)', info
   if width==390 and name in ('home','training','calendar','progress'):
    page.screenshot(path=str(base/f'preview-fitness-{name}.png'),full_page=True)
  # exercising the calendar selection does not leave calendar
  page.locator('#nav-calendar').click()
  page.locator('.day').nth(12).click()
  assert page.locator('#nav-calendar').get_attribute('class') == 'active'
  # training use on a specific date to ensure no input overflow
  page.evaluate("selectDate('2026-10-19')")
  if width==390:page.screenshot(path=str(base/'preview-fitness-strength.png'),full_page=True)
  page.evaluate("selectDate('2026-10-20')")
  assert page.locator('[data-input=run][data-field=minutes]').count()==1
  page.locator('[data-action=run-edit]').first.click()
  assert page.locator('.sheet').is_visible()
  ri=page.evaluate('''() => ({fields:[...document.querySelectorAll('.sheet input,.sheet select,.sheet textarea')].filter(e=>e.offsetParent!==null).map(e=>({r:e.getBoundingClientRect().right,l:e.getBoundingClientRect().left})),width:innerWidth})''')
  assert all(f['r']<=width+1 and f['l']>=-1 for f in ri['fields']),(width,ri)
  assert not errors,errors
  print('PASS',width,'no overflow / 5 views / calendar / forms',flush=True)
  ctx.close()
 browser.close()
