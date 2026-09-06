import asyncio
from playwright.async_api import async_playwright

async def capture(html_path, png_path, width=960):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(device_scale_factor=2)
        await page.goto(f'file://{html_path}')
        await page.wait_for_load_state('networkidle')
        body = await page.query_selector('body')
        box = await body.bounding_box()
        if box:
            await page.set_viewport_size({'width': max(width, int(box['width']) + 80), 
                                           'height': max(800, int(box['height']) + 80)})
        await page.screenshot(path=png_path, full_page=True)
        await browser.close()
        print(f'Captured: {png_path}')

async def main():
    await capture(
        '/home/z/my-project/download/qnvm/qnvm_dataflow.html',
        '/home/z/my-project/download/qnvm/qnvm_architecture_dataflow.png',
        width=960
    )

asyncio.run(main())
