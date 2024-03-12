from bs4 import BeautifulSoup
import requests
import time
import csv

url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/?page="


def get_links(numbers_of_pages):
    pages = range(1, numbers_of_pages)
    links = []
    for page in pages:
        response = requests.get(url + str(page))
        soup = BeautifulSoup(response.text, 'html.parser')
        offers = soup.find_all('a', class_='css-rc5s2u')
        for l in offers:
            # skipping otodom offers, because for some reason i can't scrap otodom webpages
            if l['href'].startswith('http'):
                # links.append(l['href'])
                pass
            else:
                links.append('https://www.olx.pl' + l['href'])

    return links


def get_params(offer_url):
    # stopping thread for 2 seconds to prevent DDoS olx :)
    time.sleep(2)
    response = requests.get(offer_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    params = soup.find_all('p', class_='css-b5m1rv er34gjf0')

    return params


# napisać te funkcje ładniej-narazie jest napisana tylko tak, aby działało
def write_to_csv(params, writer):
    new_params = []
    for param in params[1:-1]:
        new_params.append(param.text
                          .replace('zł/', '')
                          .replace('m²', '')
                          .replace(' ', '')
                          .replace('pokoje', '')
                          .replace('iwięcej', '')
                          .replace('pokój', '')
                          .replace('pokój', '')
                          .replace(',', '.')
                          .strip()
                          .split(':')
                          )

    if len(new_params) == 7:
        print(new_params)
        writer.writerow(
            [
                float(new_params[0][1]),
                new_params[1][1],
                new_params[2][1],
                new_params[3][1],
                new_params[4][1],
                float(new_params[5][1]),
                int(new_params[6][1])
            ])
    else:
        print('skipped: ', new_params)


def run():
    number_of_pages = 26
    links_to_offers = get_links(number_of_pages)
    file = open('collect_data.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['Cena za m2', 'Poziom', 'Umeblowanie', 'Rynek', 'Rodzaj zabudowy', 'Powierzchnia', 'Liczba pokoi'])

    for link in links_to_offers:
        params = get_params(link)
        write_to_csv(params, writer)


if __name__ == "__main__":
    # scraping all oferts takes a lot of time
    # run()
    print()
