import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Function to fetch all image URLs from a given page URL
def extract_image_urls(page_url, headers):
    response = requests.get(page_url, headers=headers)
    img_urls = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            img_url = img.get('src')
            if img_url:
                img_url = urljoin(page_url, img_url)
                img_urls.append(img_url)

    return img_urls

# Define the URL of the site
base_url = "https://mensreapod.com/"

# Custom headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# List to store all image URLs from all pages
all_img_urls = []

# Extract images from the base URL
base_img_urls = extract_image_urls(base_url, headers)
all_img_urls.extend(base_img_urls)

# Extract images from subsequent pages (if applicable)
# Example: Assuming pagination like https://mensreapod.com/page/2/ etc.
page_number = 2
while True:
    page_url = f"https://mensreapod.com/page/{page_number}/"
    page_img_urls = extract_image_urls(page_url, headers)
    
    if not page_img_urls:
        break
    
    all_img_urls.extend(page_img_urls)
    page_number += 1

# Define a directory to save the images
img_dir = "mensrea_images"
os.makedirs(img_dir, exist_ok=True)

# Download and save each image
for i, img_url in enumerate(all_img_urls):
    img_response = requests.get(img_url, headers=headers)
    if img_response.status_code == 200:
        img_extension = os.path.splitext(img_url)[1]
        img_name = os.path.join(img_dir, f"image_{i+1}{img_extension}")
        with open(img_name, 'wb') as img_file:
            img_file.write(img_response.content)

print(f"Downloaded {len(all_img_urls)} images.")
