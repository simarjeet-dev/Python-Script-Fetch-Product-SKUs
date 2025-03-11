import requests

# Replace with your API details
api_key = "XXXXXXXXXXXXXXXXXXX"
password = "XXXXXXXXXXXXXXXXXXXX"
shop_name = "XXXXXXXX"
api_version = "2024-07"

# List of collection IDs you want to fetch products from
collection_ids = ["274038226990","279964319790"]  # Add your collection IDs here

# Function to fetch products for a given collection
def fetch_products_from_collection(collection_id):
    url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}/products.json?collection_id={collection_id}"
    response = requests.get(url, auth=(api_key, password))
    
    if response.status_code == 200:
        products_data = response.json()
        products = products_data.get("products", [])
        return products
    else:
        print(f"Failed to fetch products for collection {collection_id}: {response.status_code} - {response.text}")
        return []

# Initialize an empty list to store all SKUs
all_skus = []

# Loop through each collection ID and fetch products
for collection_id in collection_ids:
    products = fetch_products_from_collection(collection_id)
    
    # Extract SKUs from each product's variants
    for product in products:
        variants = product.get('variants', [])
        for variant in variants:
            sku = variant.get('sku')
            if sku:
                all_skus.append(sku)

# Convert SKUs into a string with the format required
sku_string = '", "'.join(all_skus)
sku_string = f'"{sku_string}"'  # Wrap the entire string in quotes

# Write the SKUs to a .txt file
with open('product_skus.txt', 'w') as file:
    file.write(sku_string)

print("SKUs have been successfully written to 'product_skus.txt'")

# Run: python get-product-skus.py
