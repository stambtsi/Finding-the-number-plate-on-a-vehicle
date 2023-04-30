import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

# I found this link using the Burp Suite tool.
# Because the link taken from the browser doesn't go straight to the right page
# and takes time to load the images.
link = "https://www.aaaauto.cz/cz/cars.php?carlist=1&make=109&page={}&modern-request&origListURL=%2Fskoda%2F"


def parse_page(page_number: int):
    print("Page number", page_number, "is parsing now.")
    img_number = (page_number - 1) * 36
    response = requests.get(link.format(page_number)).text
    soup = BeautifulSoup(response, 'lxml')
    try:
        block = soup.find('div', class_="carsGrid carsColumns")
        all_cars_on_page = block.find_all('figure', itemprop="associatedMedia")
    except:
        print(f'Cannot find cars on page{page_number}')
        return

    for car in all_cars_on_page:
        try:
            img_src = car.find('img').get('src')
        except:
            print('Cannot find image in block:', car)
            continue
        img = requests.get(img_src).content

        with open(f"images/{img_number}.jpg", "wb") as f:
            f.write(img)
        img_number += 1


def main(pages: int):
    print('Parsing started.')

    # I use 4 processes because if using more, the site blocks access because of the large number of requests.
    # For even higher speeds it is necessary to make requests from different ip or mac addresses.
    with Pool(4) as p:
        p.map(parse_page, range(1, pages+1))
    print('Parsing successfully ended!')
