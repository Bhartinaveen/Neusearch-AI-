import json
import time
from playwright.sync_api import sync_playwright

class FurlencoScraper:
    def __init__(self):
        self.products = []
        self.urls = [
            "https://www.furlenco.com/rent/products/sara-solid-wood-queen-bed-in-timeless-teak-finish-4730-rent",
            "https://www.furlenco.com/rent/products/mattress-premium-foam-queen-size-(78-x-60-x-6-inches)-48-rent",
            "https://www.furlenco.com/rent/products/blanca-engineered-wood-single-bed-with-6--premium-mattress-4288-rent",
            "https://www.furlenco.com/rent/products/lit-double-bed-with-premium-4--mattress-5174-rent",
            "https://www.furlenco.com/rent/products/blanca-queen-bed-with-4--premium-mattress-4994-rent",
            "https://www.furlenco.com/rent/products/dune-queen-bed--mattress-with-hako-bedside-table-5138-rent",
            "https://www.furlenco.com/rent/products/aara-solid-wood-upholstered-queen-bed-5414-rent",
            "https://www.furlenco.com/rent/products/mojave-queen-bed-with-4--premium-mattress-4998-rent",
            "https://www.furlenco.com/rent/products/abstract-energy-queen-bed---lsr-molfino-300031-5493-rent",
            "https://www.furlenco.com/rent/products/hako-solid-wood-bedside-table-in-timeless-teak-finish-4506-rent",
            "https://www.furlenco.com/rent/products/vitello-solid-wood-queen-box-storage-bed-in-timeless-teak-finish---dark-grey-4510-rent",
            "https://www.furlenco.com/rent/products/mojave-upholstered-queen-bed-with-4--premium-mattress-5342-rent",
            "https://www.furlenco.com/rent/products/dune-upholstered-queen-bed-with-4--premium-mattress-5001-rent",
            "https://www.furlenco.com/rent/products/blaze-queen-hydraulic-storage-bed-grey-28-rent",
            "https://www.furlenco.com/rent/products/mojave-upholstered-queen-box-storage-bed-in-moroccan-blue-5588-rent",
            "https://www.furlenco.com/rent/products/haimish-engineered-wood-king-bed-in-lyon-walnut-with-6--premium-mattress-4569-rent",
            "https://www.furlenco.com/rent/products/vitello-solid-wood-queen-box-storage-bed-with-6--premium-mattress---dark-grey-4511-rent",
            "https://www.furlenco.com/rent/products/mojave-queen-box-storage-bed-with-premium-4--mattress-5511-rent",
            "https://www.furlenco.com/rent/products/mojave-upholstered-king-box-storage-bed-in-moroccan-blue-color-5589-rent",
            "https://www.furlenco.com/rent/products/sol-queen-bed-with-4--premium-mattress-5004-rent",
            "https://www.furlenco.com/rent/products/blanca-queen-bed--mattress-with-hako-bedside-table-5124-rent",
            "https://www.furlenco.com/rent/products/blanca-queen-bed-with-6premium-mattress-3461-rent",
            "https://www.furlenco.com/rent/products/mojave-king-bed-with-6-premium-king-mattress-3826-rent",
            "https://www.furlenco.com/rent/products/blaze-queen-hydraulic-storage-bed-aqua-27-rent",
            "https://www.furlenco.com/rent/products/mojave-queen-bed-with-6-premium-queen-mattress-3828-rent",
            "https://www.furlenco.com/rent/products/blaze-queen-hydraulic-storage-bedgrey-with-6premium-mattress-3507-rent",
            "https://www.furlenco.com/rent/products/mojave-queen-bed--mattress-with-taki-bedside-table-5127-rent",
            "https://www.furlenco.com/rent/products/mojave-upholstered-king-bed-with-6--premium-mattress-5457-rent",
            "https://www.furlenco.com/rent/products/mojave-upholstered-queen-bed-with-6--premium-mattress-5343-rent",
            "https://www.furlenco.com/rent/products/dune-upholstered-storage-bed-with-6--mattress---bianca-bedside-table-4907-rent",
            "https://www.furlenco.com/rent/products/sara-solid-wood-queen-bed-with-momkin-bedside-table-5601-rent",
            "https://www.furlenco.com/rent/products/blaze-queen-hydraulic-storage-bedaqua-with-6premium-mattress-3505-rent",
            "https://www.furlenco.com/rent/products/vitello-queen-box-storage-bed-with-4--premium-mattress-5510-rent"
        ]

    def scrape(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for link in self.urls:
                print(f"Scraping Product: {link}")
                try:
                    product_data = self.scrape_product_details(page, link)
                    if product_data:
                        self.products.append(product_data)
                        print(f"Scraped: {product_data['title']}")
                except Exception as e:
                    print(f"Failed to scrape {link}: {e}")
                
            browser.close()

        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(self.products, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.products)} products to products.json")

    def scrape_product_details(self, page, url):
        try:
            page.goto(url, timeout=45000)
            # Wait for either h1 or error
            page.wait_for_selector('h1', state='visible', timeout=15000)
        except Exception as e:
            print(f"Timeout loading {url}")
            return None

        data = page.evaluate('''() => {
            const getValidText = (el) => el ? el.innerText.trim() : "";
            const title = getValidText(document.querySelector('h1'));
            
            // Price: heuristic
            let price = "0";
            const allPs = Array.from(document.querySelectorAll('p'));
            const priceEl = allPs.find(p => p.innerText.includes('₹') && p.innerText.includes('/mo'));
            if (priceEl) price = priceEl.innerText.replace(/\\n/g, " ").trim();
            
            // Description
            let description = "";
            const allDivs = Array.from(document.querySelectorAll('div, p'));
            // Look for a div that contains descriptive text like "Rent Sara..."
            // Or look for text content > 100 chars
            const descEl = allDivs.find(el => el.innerText.includes("Rent " + title) || (el.innerText.length > 50 && el.innerText.includes("Product Description")));
            if (descEl) description = descEl.innerText.substring(0, 500);

            // Features
            let features = {};
            // Try key-value extraction from entire body text if specific selector fails
            // Or look for "Dimensions" / "Material"
            const bodyText = document.body.innerText;
            const keywords = ["Brand", "Dimensions", "Material", "Color", "Style"];
            keywords.forEach(key => {
                const regex = new RegExp(key + "\\\\s*[:\\\\-]?\\\\s*([^\\\\n]+)", "i");
                const match = bodyText.match(regex);
                if (match) features[key] = match[1].trim();
            });

            const img = document.querySelector('img[src*="ful-shared-assets"]'); 
            const image_url = img ? img.src : "";

            return {
                title,
                price,
                description: description || title,
                features,
                image_url,
                category: "Bedroom",
                link: document.location.href
            };
        }''')
        
        return data

if __name__ == "__main__":
    scraper = FurlencoScraper()
    scraper.scrape()
