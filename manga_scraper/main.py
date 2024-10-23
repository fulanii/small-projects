# """Import our libs """
import requests as req
from bs4 import BeautifulSoup
import os


def get_chapter_url(chapter_num:str) -> str:

    """
    gets the correct chapter url with the random number return: str

    :param chapter_num:str
    """
    base_url = "https://tcbscans.me/mangas/5/one-piece"
    
    res = req.get(base_url)
    res.raise_for_status() 

    soup = BeautifulSoup(res.text, "html.parser")
    chapter_links = soup.find_all("a", href=True)
    
    for link in chapter_links:
        href = link["href"]
        if f"one-piece-chapter-{chapter_num}" in href:
            return f"https://tcbscans.me{href}"
        
    # If no link is found, return None
    return None


def get_images_url(page_url:str) -> list[str]:
    """takes a chapter page url and return a list of all manga panels on the page download url"""
    # get the page 
    res = req.get(page_url) # "https://tcbscans.me/chapters/7817/one-piece-chapter-999"

    # give the res text to bs4
    soup = BeautifulSoup(res.text, 'html.parser')

    # getting all the <picture> tag from html
    all_pic_tags = soup.find_all("picture")
    raw_html_images = []
    final_manga_links = []

    for picture in all_pic_tags:
        # taking the <img> tag from <picture>
        img_tag = picture.find('img')

        # removing the tcb scans promo page
        if not img_tag['src'].endswith('_01.png'):
            raw_html_images.append(img_tag)
        
    for panel in raw_html_images:
        final_manga_links.append(panel['src'])

    return final_manga_links


def download_images(image_urls, folder_name):
    """Takes list of manga url and download locally"""
    # Loop through each image URL in the list
    for index, url in enumerate(image_urls):
        try:
            # Send a GET request to fetch the content of the image
            response = req.get(url)
            
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()
            
            # Create the folder if it doesn't exist
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            # Extract the image name from the URL: will remove any %20 (spaces) or similar encoded characters
            image_name = os.path.basename(url).replace('%20', '_')
            # Define the full path for the image inside the specified folder
            image_path = os.path.join(folder_name, image_name)

            # Save the image in the current working directory
            with open(image_path, 'wb') as file:
                file.write(response.content)
            
            print(f"Downloaded: {image_name} saved to: {image_path}")
        except req.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")



def main():
    chapter_num = input("What is the chapter number (1-1130): ")
    url = get_chapter_url(chapter_num)

    print(url)
    
    download_links = get_images_url(page_url=url)

    download_images(download_links, chapter_num)

if __name__ == "__main__":
    main()