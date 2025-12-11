from playwright.sync_api import sync_playwright

url = "https://www.furlenco.com/rent/products/sara-solid-wood-queen-bed-in-timeless-teak-finish-4730-rent"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
    )
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    
    # Block images/fonts
    page.route("**/*.{png,jpg,jpeg,svg,css,woff,woff2}", lambda route: route.abort())
    
    print(f"Navigating to {url}")
    try:
        page.goto(url, timeout=60000, wait_until='domcontentloaded')
        print("Page loaded args")
        page.wait_for_selector('h1', timeout=20000)
        title = page.evaluate("document.querySelector('h1').innerText")
        print(f"Title: {title}")
    except Exception as e:
        print(f"Error: {e}")
        # Screenshot for debugging if needed
        # page.screenshot(path="error.png")
    
    browser.close()
