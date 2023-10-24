"""
Web crawler with python 1
"""

import httpx
from selectolax.parser import HTMLParser
import time

def get_html(baseurl, page):
    """
    get html from url by page

    input:
        baseurl: url
        page: numb of pages

    return:
        yield data in dict
        False when exceed page limit
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36f"
    }
    # if not follow_redirects=True=> donot redirect page when page =1, status code is 301
    res = httpx.get(baseurl + str(page), headers=headers,
                    follow_redirects=True)

    # handling when response not 2xx success code httpx.HTTPStatusError
    # handling when response is 4xx or 5xx  httpx.HTTPError
    # https://www.python-httpx.org/quickstart/#exceptions

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r} \
            . Page Limit Exceed")
        return False
    html = HTMLParser(res.text)
    # print(res.status_code)
    return html


def extract_text(html, selector):
    """
    extract text from selector of html
    html: html
    selector: selector css_first
    """
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None


def parse_page(html):
    """
    parse page
    get infomation
    """
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")

    for product in products:
        item = {
            "name": extract_text(product, "span[data-ui=product-title]"),
            "price": extract_text(product, "span[data-ui=sale-price]"),
            "savings": extract_text(product, "div[data-ui=savings-percent-variant2]")
        }
        yield item


def main():
    """
    main function
    sleep 1s to reduce server load
    """
    url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="
    for x in range(1, 100):
        print(x)
        html = get_html(url, x)
        data = parse_page(html)
        if html is False:
            break
        for item in data:
            print(item)
        time.sleep(1)


if __name__ == "__main__":
    main()
