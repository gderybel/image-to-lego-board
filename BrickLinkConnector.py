from LegoPiece import LegoPiece
import requests
from bs4 import BeautifulSoup


class BrickLinkConnector:
    base_url = "https://www.bricklink.com/v2/catalog/catalogitem.page?P="

    def get_piece_price(piece: LegoPiece) -> float:

        url = f"{BrickLinkConnector.base_url}={piece.id}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the price element in the HTML (this is an example, actual implementation may vary)
        price_element = soup.find("span", class_="price")
        if price_element:
            price_text = price_element.text.strip().replace("$", "")
            try:
                return float(price_text)
            except ValueError:
                return 0.0
        return 0.0
