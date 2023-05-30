def foo():
    print('ello foo')
    
async def scrap(urltoScrap):
    browser = await launch(executablePath='/usr/bin/google-chrome-stable', headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(urltoScrap, {'waitUntil': 'networkidle2'})
    await page.waitForFunction('document.readyState === "complete"')
    htmlContent = await page.content()
    await browser.close()
    return htmlContent