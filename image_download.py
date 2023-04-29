import requests
from bs4 import BeautifulSoup


link = "https://www.aaaauto.cz/cz/cars.php?carlist=1&make=109&page={}&modern-request&origListURL=%2Fskoda%2F"
img_number = 0

for page_number in range(1, 69):   # up to 69 because there are no photos from the page 70
    response = requests.get(link.format(page_number)).text
    soup = BeautifulSoup(response, 'lxml')
    block = soup.find('div', class_="carsGrid carsColumns")
    allCarsOnPage = block.find_all('figure', itemprop="associatedMedia")

    for car in allCarsOnPage:
        imgSrc = car.find('img').get('src')
        img = requests.get(imgSrc).content

        with open(f"images/{img_number}.jpg", "wb") as f:
            f.write(img)
        img_number += 1
