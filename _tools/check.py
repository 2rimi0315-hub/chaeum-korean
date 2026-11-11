import sys, asyncio
from playwright.async_api import async_playwright
async def main(names):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width':820,'height':1000})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        for n in names:
            await pg.goto(f'file:///home/claude/korean/site/{n}.html')
            if not n.startswith(('vocab','index')):
                await pg.click('.rvgroup button >> nth=0')
                await pg.click('.mc button >> nth=0'); await pg.click('.checkbtn')
                print(n, await pg.inner_text('#result'))
            await pg.screenshot(path=f'/home/claude/korean/shots/full_{n}.png', full_page=True)
        print('errors:', errs)
        await b.close()
asyncio.run(main(sys.argv[1:]))
