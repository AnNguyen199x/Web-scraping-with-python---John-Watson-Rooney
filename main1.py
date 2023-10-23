import httpx
from selectolax.parser import HTMLParser

url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36f"}

res = httpx.get(url, headers=headers)
# print status url
# print(res.status_code)
# page html
# print(res.text)

# pars html
html = HTMLParser(res.text)
# get tilte from css first item
# print(html.css_first("title").text())

# products = html.css("div#search-results ul li")

'''
for product in products:
    if product.css_first(".Xpx0MUGhB7jSm5UvK2EY") is not None:
        print(product.css_first(".Xpx0MUGhB7jSm5UvK2EY").text())
'''
# css path
# search-results > ul > li:nth-child(1) > a.O8aFd2MOq4cf8b3yUR2p.tS6GbfEJ9cTyCftpIpEO > h2 > span.Xpx0MUGhB7jSm5UvK2EY
# search-results > ul > li:nth-child(1)

products = html.css("li.VcGDfKKy_dvNbxUqm29K")
# for product in products:
#     item = {
#         "name": product.css_first(".Xpx0MUGhB7jSm5UvK2EY").text(),
#         "price": product.css_first("span[data-ui=sale-price]").text()
#     }
#     print(item)

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

for product in products:
    item = {
        "name": extract_text(product,"span[data-ui=product-title]"),
        "price": extract_text(product, "span[data-ui=sale-price]")
    }
    print(item)
