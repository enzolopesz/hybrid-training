from playwright.sync_api import sync_playwright
from pathlib import Path
import json
BASE='http://127.0.0.1:8765/'
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(Path('/mnt/data/hybrid-training-v2.2/index.html').read_text())
 page.add_style_tag(content=Path('/mnt/data/hybrid-training-v2.2/styles.css').read_text())
 page.evaluate("""() => { const saved={}; Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:(k)=>saved[k]||null,setItem:(k,v)=>saved[k]=String(v)}}) }""")
 page.add_script_tag(content=Path('/mnt/data/hybrid-training-v2.2/app.js').read_text()); page.wait_for_timeout(100)
 assert page.locator('#nav-home').get_attribute('class') is not None
 assert page.locator('#nav-calendar svg').count()==1
 page.locator('#nav-calendar').click()
 assert page.locator('#nav-calendar').get_attribute('class') == 'active'
 day=page.locator('.days button[data-action="cal-pick"]').filter(has=page.locator('strong')).nth(10)
 day.click()
 assert page.locator('#nav-calendar').get_attribute('class') == 'active','Selecting date switched tabs'
 assert page.locator('#agendaDetail').count()==1
 assert page.locator('.agenda-detail').count()==1
 assert page.locator('.agenda-preview').count()==1
 assert page.locator('.agenda-buttons button[data-action="pick"]').count()==1
 assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Agenda overflow mobile'
 # navigate to a monday to test gym, still agenda
 page.locator('.days button[data-date="2026-10-19"]').click()
 assert 'Supino reto com barra' in page.locator('.agenda-detail').inner_text()
 page.screenshot(path='/mnt/data/hybrid-training-v2.2/preview-agenda-v22.png',full_page=True)
 page.locator('.agenda-buttons [data-action="pick"]').click()
 assert page.locator('#nav-training').get_attribute('class') == 'active'
 assert page.locator('.exercise').count()==7
 assert page.locator('[data-action="start-rest"]').count()==0
 assert page.locator('input#exRest').count()==0
 # 150s for supino, 75s for elevação lateral
 assert '2min 30s' in page.locator('.exercise').first.inner_text()
 assert '1min 15s' in page.locator('.exercise').nth(4).inner_text()
 # Enter values and finish first set to start timer
 page.locator('.exercise').first.locator('input[data-field="kg"]').first.fill('50')
 page.locator('.exercise').first.locator('input[data-field="reps"]').first.fill('8')
 page.locator('.exercise').first.locator('button[data-action="toggle-set"]').first.click()
 assert '02:30' in page.locator('#timerDock').inner_text(), page.locator('#timerDock').inner_text()
 page.locator('[data-tab="settings"]').last.click()
 page.locator('button[data-action="editor"][data-type="A"]').first.click()
 page.locator('.editrow button[data-action="edit-ex"]').first.click()
 assert page.locator('input#exRest').count()==0
 assert 'Incremento peso' in page.locator('#modalRoot').inner_text()
 assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),'Form overflow mobile'
 page.screenshot(path='/mnt/data/hybrid-training-v2.2/preview-editor-v22.png')
 # cross-check on narrow width
 page.set_viewport_size({'width':320,'height':700});page.wait_for_timeout(200)
 assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), '320 viewport overflow'
 page.set_viewport_size({'width':390,'height':844});page.locator('#modalRoot [data-action="close-modal"]').click()
 # save persistence after reload
 page.evaluate("() => { document.getElementById('app').innerHTML=''; tab='home'; selected=new Date().toISOString().slice(0,10); state=normalized(JSON.parse(localStorage.getItem(STORE))); render() }")
 page.locator('#nav-training').click()
 page.evaluate("selectDate('2026-10-19')")
 assert page.locator('.exercise').first.locator('input[data-field="kg"]').first.input_value()=='50'
 assert not errors,errors
 print('PASS browser: inline agenda, vector icons, automatic rest, no manual rest input, mobile 320/390, persistence')
 browser.close()
