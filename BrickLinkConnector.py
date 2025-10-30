from LegoPiece import LegoPiece
from LegoType import LegoType
import requests
from bs4 import BeautifulSoup
import re
from functools import lru_cache
from urllib.parse import urlencode, quote
from json import dumps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from WantedList import WantedList
import json


class BrickLinkConnector:
    buy_url = "https://www.bricklink.com/v2/catalog/catalogitem.page"
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

    @classmethod
    def get_bricklink_url(cls, ref: LegoType, color_id: int, quantity: int) -> str:
        query_params = {"P": ref, "C": color_id}
        fragment_data = {"color": color_id, "minqty": str(quantity), "iconly": 0}
        fragment_encoded = quote(
            dumps(fragment_data, separators=(",", ":")), safe="{}:,"
        )
        return f"{cls.buy_url}?{urlencode(query_params)}#T=S&C={color_id}&O={fragment_encoded}"

    @classmethod
    def get_piece_stock(
        cls, ref: LegoType, color_id: int, quantity: int
    ) -> tuple[int, str]:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(options=options)

        url = cls.get_bricklink_url(ref, color_id, quantity)
        driver.get(url)
        time.sleep(5)  # Wait for JS to load

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        element = soup.find("span", {"id": "_idtxtTotalFound"})
        if element and element.text.strip():
            text = element.text.strip()
            number = int(text.split()[0].replace(",", ""))
            return number, url

        return 0, url

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

    @staticmethod
    def create_wanted_list(name: str, description: str = None) -> str:
        url = "https://www.bricklink.com/ajax/clone/wanted/editList.ajax"
        data = {"wantedMoreName": name, "wantedMoreDesc": description, "action": "C"}
        cookies = {}
        response = requests.post(url, data=data, cookies=cookies)
        if response.status_code == 200:
            try:
                result = response.json()
            except ValueError:
                print("Réponse non JSON :", response.text)
                return None

            id = result.get("wantedMoreID")

            return WantedList(id, name, description)

    @staticmethod
    def add_piece_to_wanted_list(
        wanted_list: WantedList, piece: LegoPiece, quantity: int
    ) -> bool:
        url = "https://www.bricklink.com/ajax/clone/wanted/add.ajax"

        wanted_item = [
            {
                "itemID": piece.reference,
                "colorID": piece.color.bricklink_id,
                "wantedQty": quantity,
                "wantedQtyFilled": 0,
                "wantedNew": "N",
                "wantedNotify": "N",
                "wantedRemarks": None,
                "wantedPrice": None,
            }
        ]

        data = {
            "wantedItemStr": json.dumps(wanted_item),
            "wantedMoreID": wanted_list.id,
            "sourceLocation": 1300,
        }

        cookies = {}

        response = requests.post(url, data=data, cookies=cookies)

        if response.status_code == 200:
            return True
        return False
