import requests
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Replace with your API details
api_key = "xxxxxxxxxxxxxxxxxxxx"
password = "xxxxxxxxxxxxxxxxxxxxxx"
shop_name = "xxxxxxxxx"
api_version = "2024-07"

# List of collection IDs you want to fetch products from
collection_ids = ["266008952878", "266046734382"]  # Add your collection IDs here

# Function to fetch products for a given collection
def fetch_products_from_collection(collection_id):
    # Construct the API endpoint for each collection
    url = f"https://{shop_name}.myshopify.com/admin/api/{api_version}/products.json?collection_id={collection_id}"
    
    # Make the API request
    response = requests.get(url, auth=(api_key, password))
    
    if response.status_code == 200:
        products_data = response.json()
        products = products_data.get("products", [])
        return products
    else:
        print(f"Failed to fetch products for collection {collection_id}: {response.status_code} - {response.text}")
        return []

# Initialize an empty list to store all product information
all_products_info = []

# Loop through each collection ID and fetch products
for collection_id in collection_ids:
    products = fetch_products_from_collection(collection_id)
    
    # Extract product details from each product
    for product in products:
        product_id = product.get('id')
        product_title = product.get('title')
        variants = product.get('variants', [])
        
        for variant in variants:
            variant_info = {
                'Product ID': str(product_id),
                'Product Title': str(product_title),
                'Variant ID': str(variant.get('id')),
                'Variant SKU': str(variant.get('sku')),
                'Collection ID': str(collection_id)  # Add collection ID for reference
            }
            all_products_info.append(variant_info)

# Convert the list of products to a DataFrame
df = pd.DataFrame(all_products_info)

# Convert all columns to text (string)
df = df.astype(str)

# Export to Excel with adjusted column widths
excel_filename = 'shopify_products_multiple_collections.xlsx'
with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Adjust column widths based on content
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    for column in worksheet.columns:
        max_length = 0
        column_name = column[0].column_letter  # Get the column name
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2  # Adjust width with a little padding
        worksheet.column_dimensions[column_name].width = adjusted_width

print(f"\nExcel file '{excel_filename}' exported successfully with adjusted column widths.")
