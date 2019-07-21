from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
from urllib.request import Request
from urllib.request import urlopen

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except:
        pass

    return html_content

def get_details(tr):
    
    stamp = {}
    
    try:
        url_item = tr.find_all("a", {"title":"View full details"})[0]
        url = 'https://www.purvesphilatelics.co.uk/' + url_item.get('href')
    except:
        return stamp

    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price = html.select('.price')[0].get_text()
        price = price.replace(",", "").strip()
        price = price.replace("£", "").strip()
        stamp['price'] = price
    except:
        stamp['price'] = None

    try:
        category = html.select("#content a.subtext")[0].get_text()
        stamp['category'] = category
    except:
        stamp['category'] = None

    try:
        stamp['raw_text'] = get_td_value(tr, 5)
    except:
        stamp['raw_text'] = None
        
    try:
        stamp['condition'] = get_td_value(tr, 6)
    except:
        stamp['condition'] = None    
        
    try:
        stamp['country'] = get_td_value(tr, 1)
    except:
        stamp['country'] = None          
        
    try:
        stamp['SG'] = get_td_value(tr, 2)
    except:
        stamp['SG'] = None
        

    stamp['currency'] = 'GBP'
    
    # image_urls should be a list
    images = []
    try:
        image_items = html.select('img.insetLeft')
        for image_item in image_items:
            img = 'https://www.purvesphilatelics.co.uk/' + image_item.get('src')
            images.append(img)
    except:
        pass

    stamp['image_urls'] = images

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.stamps tr'):
            items.append(item)
    except:
        pass

    try:
        next_items = html.select('#rppForm a')
        for next_item in next_items:
            next_item_text = next_item.get_text().strip()
            if 'Next' in next_item_text:
                next_url = 'https://www.purvesphilatelics.co.uk/' + next_item.get('href')
                break
    except:
        pass

    shuffle(items)

    return items, next_url

def get_td_value(tr, index):
    return tr.select('td')[index].get_text().strip()

# start url
url = 'https://www.purvesphilatelics.co.uk/price_list.cfm'

while(url):
    page_items, url = get_page_items(url)
    for page_item in page_items:
        stamp = get_details(page_item)
