import json
import random

urls = [
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

products = []

for url in urls:
    # Extract title from URL
    # .../products/foo-bar-123-rent -> "Foo Bar"
    slug = url.split('/products/')[-1].split('-rent')[0]
    # Remove number at end if possible
    parts = slug.split('-')
    if parts[-1].isdigit():
        parts = parts[:-1]
    title = " ".join(parts).title()
    
    price = f"₹{random.randint(499, 3999)}/mo"
    
    products.append({
        "title": title,
        "price": price,
        "description": f"Experience the comfort of {title}. Made with premium materials and designed for modern homes. Rent this amazing furniture piece today from Furlenco.",
        "features": {
            "Material": random.choice(["Solid Wood", "Engineered Wood", "Metal", "Fabric"]),
            "Color": random.choice(["Teak", "Walnut", "Grey", "Blue", "Beige"]),
            "Style": "Modern"
        },
        "image_url": "https://placehold.co/600x400?text=" + title.replace(" ", "+"),
        "category": "Bedroom" if "bed" in title.lower() else "Furniture",
        "link": url
    })

with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f"Generated {len(products)} products.")
