import json
import requests
from bs4 import BeautifulSoup, Tag

URL_BASE = "https://quotes.toscrape.com"


def process_page(soup: BeautifulSoup):
    """
    #### Función ocupada para procesar paginas y extraer la información necesaria.
    """
    quotes = soup.find_all("div", class_="quote")
    next_button = soup.find("li", class_="next")
    res = []

    for quote in quotes:
        if type(quote) != Tag:
            continue
        content = quote.find("span", class_="text")
        author = quote.find("small", class_="author")

        content = content.text if content else "[Dato no encontrado]"
        author = author.text if author else "[Dato no encontrado]"

        res.append({
            "cita": content,
            "autor": author
        })
    url = next_button.find("a") if type(next_button) == Tag else None
    return res, url


def main():
    """
    #### Punto de entrada del script.
    """
    res = requests.get(URL_BASE)
    soup = BeautifulSoup(res.content, "html.parser")
    response, next_button = process_page(soup)

    while next_button:
        if type(next_button) != Tag:
            continue
        url = next_button.attrs['href']
        url = URL_BASE + str(url)
        res_page = requests.get(url)
        soup = BeautifulSoup(res_page.content, "html.parser")
        response_page, next_button = process_page(soup)

        response.extend(response_page)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(response, f, indent=4)


if __name__ == "__main__":
    main()
