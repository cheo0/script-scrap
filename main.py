import requests
from bs4 import BeautifulSoup

def main():
    res = requests.get("https://quotes.toscrape.com/")
    soup = BeautifulSoup(res.content, "html.parser")
    print(soup)


if __name__ == "__main__":
    main()
