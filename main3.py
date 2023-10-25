"""
Web crawler with python 1
"""

import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin
from dataclasses import dataclass, asdict


@dataclass
class Item:
    """
    item
    """
    # In case there is no info: None
    name: str | None
    item_num: str | None
    price: str | None
    rating: float | None


def get_html(url, **kwargs):
    """
    get html response text from url with optional argument page

    input:
        url: url
        **kwargs: optional atguments, here is page

    return:
        yield data
        False when exceed page limit
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36f"
    }
    if kwargs.get("page"):
        res = httpx.get(
            url + str(kwargs.get("page")), headers=headers, follow_redirects=True)
    else:
        res = httpx.get(url, headers=headers, follow_redirects=True)

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r} \
            . Page Limit Exceed")
        return False
    html = HTMLParser(res.text)

    return html


def extract_text(html, selector):
    """
    extract text from selector of html text
    Input:
        html: html text
        selector: selector css_first
    Output:
        text from selector
    """
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None


def parse_item_page(html):
    """
    parse item page get item's info
    """
    new_item = Item(
        name=extract_text(html, "h1#product-page-title"),
        item_num=extract_text(html, "span#product-item-number"),
        price=extract_text(html, "span#buy-box-product-price"),
        rating=extract_text(html, "span.cdr-rating__number_13-5-3")
    )
    return new_item

def parse_search_page(html: HTMLParser):
    """
    parse page
    yield url of products in page
    Input:
        html: HTMLParser/html text from get_html()
    Output:
        yield url of each product in page
    """
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")

    for product in products:
        yield urljoin("http://www.rei.com", product.css_first("a").attributes["href"])


def main():
    """
    main function
    sleep 1s to reduce server load
    """
    products = []
    url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="
    for x in range(1, 2):
        print(f'Getting page {x}')
        html = get_html(url, page=x)

        if html is False:
            break

        products_url = parse_search_page(html)
        for url in products_url:
            print(url)
            html = get_html(url)
            # print(html.css_first("title").text())
            products.append(parse_item_page(html))
            time.sleep(1)

    for product in products:
        # print(product)
        # if u want to get product in dictionary to CSV or Json:
        print(asdict(product))


if __name__ == "__main__":
    main()
