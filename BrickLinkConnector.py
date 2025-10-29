from LegoPiece import LegoPiece
import requests
from bs4 import BeautifulSoup
import re
from functools import lru_cache


class BrickLinkConnector:
    buy_url = "https://www.bricklink.com/v2/catalog/catalogitem.page?P="
    color_url = "https://v2.bricklink.com/en-fr/catalog/color-guide"

    @staticmethod
    def get_piece_price(piece: LegoPiece) -> float:
        url = f"{BrickLinkConnector.buy_url}{piece.id}"
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

    @staticmethod
    def get_piece_stock(url: str) -> int:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        element = soup.find(string=lambda text: text and "Lots For Sale" in text)
        if element:
            quantity = element.split("Lots For Sale")[0].strip()
            return int(quantity)
        return 0
        # TODO: should be based on url https://www.bricklink.com/v2/catalog/catalogitem.page?P=3024&C=222#T=S&C=222&O={%22color%22:%22222%22,%22minqty%22:%22281%22,%22iconly%22:0}
        # where minqty should be adjusted and text "X Items Found" should be parsed

    @staticmethod
    @lru_cache(maxsize=255)
    def get_piece_colors(type: str = "solid") -> list[str]:
        from LegoColor import LegoColor

        url = f"{BrickLinkConnector.color_url}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        pattern = re.compile(
            r"--bl-castor-table-swatch-with-image-background-color:\s*(#[0-9a-fA-F]{3,6})"
        )

        colors = []

        for tr in soup.find_all("tr"):
            color_hex = None
            bricklink_name = None
            bricklink_id = None
            lego_name = None
            lego_id = None

            td_with_style = tr.find("td", attrs={"data-testid": "SwatchWithImage"})
            if td_with_style and "style" in td_with_style.attrs:
                match = pattern.search(td_with_style["style"])
                if match:
                    color_hex = match.group(1)

            color_info_td = tr.find(
                "td", class_="color-list-wide-viewport_cellListViewColorName__rVQgC"
            )
            if color_info_td:
                name_tag = color_info_td.find("p")
                if name_tag:
                    bricklink_name = name_tag.get_text(strip=True)
                span_tag = color_info_td.find("span")
                if span_tag:
                    lego_color = span_tag.get_text(strip=True).replace(
                        "LEGO Color:", ""
                    )
                    match = re.match(r"^(.*?)\s*-\s*(\d+)$", lego_color)
                    if match:
                        lego_name = match.group(1)
                        lego_id = int(match.group(2))

            tds = tr.find_all("td")
            if tds:
                bricklink_id = tds[-1].get_text(strip=True)

            if color_hex and bricklink_name and lego_name and lego_id and bricklink_id:
                colors.append(
                    LegoColor(
                        bricklink_name=bricklink_name,
                        lego_name=lego_name,
                        bricklink_id=bricklink_id,
                        lego_id=lego_id,
                        hex_code=color_hex,
                    )
                )

        return colors
