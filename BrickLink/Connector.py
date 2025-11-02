from Brick.Piece import Piece
from Brick.Type import Type
import requests
from bs4 import BeautifulSoup
import re
from functools import lru_cache
from urllib.parse import urlencode, quote
from json import dumps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from BrickLink.WantedList import WantedList
from BrickLink.Color import Color as BrickLinkColor
import json


class Connector:
    buy_url = "https://www.bricklink.com/v2/catalog/catalogitem.page"
    color_url = "https://v2.bricklink.com/en-fr/catalog/color-guide"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/130.0.0.0 Safari/537.36"
        ),
    }

    @staticmethod
    def get_piece_price(piece: Piece) -> float:
        url = f"{Connector.buy_url}{piece.id}"
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
    def get_bricklink_url(cls, ref: Type, color_id: int, quantity: int) -> str:
        query_params = {"P": ref, "C": color_id}
        fragment_data = {"color": color_id, "minqty": str(quantity), "iconly": 0}
        fragment_encoded = quote(
            dumps(fragment_data, separators=(",", ":")), safe="{}:,"
        )
        return f"{cls.buy_url}?{urlencode(query_params)}#T=S&C={color_id}&O={fragment_encoded}"

    @classmethod
    @lru_cache(maxsize=None)
    def get_piece_stock(
        cls, ref: Type, color_id: int, quantity: int
    ) -> tuple[int, str]:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(options=options)

        url = cls.get_bricklink_url(ref, color_id, quantity)
        driver.get(url)
        time.sleep(3)  # Wait for JS to load

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
    @lru_cache(maxsize=None)
    def get_piece_colors_with_stock(ref: Type) -> list[BrickLinkColor]:
        url = f"{Connector.buy_url}?P={ref}#T=C"
        response = requests.get(url, headers=Connector.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        colors = []

        lots_div = soup.find(
            "div", class_="pciColorTitle", string=lambda s: s and "Lots For Sale:" in s
        )
        if lots_div:
            td_parent = lots_div.find_parent("td")
            for flex_div in td_parent.find_all(
                "div", style=lambda s: s and "display:flex" in s
            ):
                color_div = flex_div.find("div", class_="pciColorTabListItem")
                text_div = color_div.find_next_sibling("div") if color_div else None
                if not text_div:
                    continue

                a_tag = text_div.find(lambda t: t.name and t.name.lower() == "a")
                if not a_tag:
                    continue

                style = color_div.get("style", "")
                match_color = re.search(r"#([0-9A-Fa-f]{6})", style)
                color_hex = match_color.group(1) if match_color else None

                onclick = a_tag.get("onclick", "")
                match_id = re.search(
                    r"showInventoryWithColor\(\s*(\d+)\s*\)", onclick, re.IGNORECASE
                )
                color_id = int(match_id.group(1)) if match_id else None

                color_name = a_tag.get_text(strip=True)
                text = text_div.get_text(strip=True)
                match_stock = re.search(r"\((\d+)\)", text)
                color_stock = int(match_stock.group(1)) if match_stock else None

                if color_hex:
                    # Used to filter for the first line 'Non Applicable'
                    colors.append(
                        BrickLinkColor(color_id, color_name, color_hex, color_stock)
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
        wanted_list: WantedList, piece: Piece, quantity: int
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
