import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie' :  'RT="z=1&dm=sephora.it&si=4f2df800-32ba-4737-87ba-7882300d876d&ss=lsnh0o7e&sl=1&tt=a5f&bcn=%2F%2F02179918.akstat.io%2F&ld=a5i"; _screload=; cto_bundle=tACIeV9tNUFIQmtickh2b0R2MzlZaUtBZVRwZVE1ZXJFZ0UlMkJBZUt6Rm1FQzR5UmR2U3haOGk3QSUyRm1sb0VwckROTGdRQ3RjWDhQSERPTEVuUlJMbnVXZTZNM3QlMkZZWW5GSmU4QmpFNGxrR2JBSERIaWlTeDNUOFZDMElyV05XUWpicE1OUA; bm_sv=854E0C5FA33617A098F82FA3ABAFB354~YAAQhMgWwy8LjH6NAQAAkvy5rRazuWg2oJtqig8kL7/WAdh4dAgd+IIGmh2jFqFsDJQuGTo5esaegLFLcZpIQsmNHy2UJrmFjO5ZLjcnW5f9JcQTONEI+N7pu21CVzwMDqnC6im300NyM1+jM4THTHxenP2UUskpwtGy6plVoB/Ckx3JeDQQhJmy5WEG1kOkspQ+ixflnDIVvM0hdie0fPDyLGqECAms0Hn+9B7VJoc2sDsjrJ+olEVHAIf/GAFd1g==~1; __cq_dnt=0; dw_dnt=0; _pin_unauth=dWlkPU1UWXlZV1ppTjJNdE5Ea3pOQzAwTXpSbExXRXdaak10TlRBNFpqTmlOR1UzWkdGbQ; offers=%7B%22resultCountOffers%22%3A0%2C%22isOffersViewed%22%3Atrue%2C%22offerIDs%22%3A%5B%5D%2C%22firstOffer%22%3A%22%22%7D; ABTasty=uid=awn4gdwr6qh18gkv&fst=1706783050206&pst=1708010569557&cst=1708013330661&ns=7&pvt=60&pvis=36&th=; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.sephora.it%252F; __cq_bc=%7B%22bcvw-Sephora_IT%22%3A%5B%7B%22id%22%3A%22P4026095%22%2C%22sku%22%3A%22512510%22%7D%5D%7D; __cq_seg=; __cq_uuid=efjVbdcnQtZTSTKa1I6xiwNEDP; _cs_id=06802916-6fc5-a54d-9a73-2f9bc12dedfe.1707992083.4.1708016660.1708013331.1.1742156083669.1; _cs_s=42.5.0.1708018460696; _fbp=fb.1.1707992083758.1903446801; _ga=GA1.2.498181226.1707992081; _ga_2YZ9FQ8XWV=GS1.1.1708013329.7.1.1708016660.0.0.0; _ga_JF05BE885E=GS1.1.1708013329.7.1.1708016660.0.0.0; _gac_UA-87625978-8=1.1707992081.CjwKCAiAibeuBhAAEiwAiXBoJFPddECm0Qp3_z1qVDW4GE--SidptAxjru7MLqKPSKqWoWE-t9rbqxoCvh0QAvD_BwE; _gcl_au=1.1.510950238.1707990786; _gcl_aw=GCL.1707992078.CjwKCAiAibeuBhAAEiwAiXBoJFPddECm0Qp3_z1qVDW4GE--SidptAxjru7MLqKPSKqWoWE-t9rbqxoCvh0QAvD_BwE; _gid=GA1.2.886878786.1707992081; _scid_r=237b5005-b4be-4043-a834-caefd8f54995; _uetsid=09c5b860cbeb11ee922d3b1a5e8525f3; _uetvid=0e4ccf00c0ec11eeb25b27a023964569; lastVisitedProducts=P4026095|P10046057|P10053048; t2s-p=a635448f-1da3-4e88-a307-6b450ffae823; tCdebugLib=1; tc_AbTastyConsent=true; tc_cj_v2=%5Ecl_%5Dny%5B%5D%5D_mmZZZZZZKQJRJKPPOSOLMZZZ%5D; tc_cj_v2_cmp=; tc_cj_v2_med=; tc_compteur_page=61; ak_bmsc=E060E217A848A786EF8294F5B8B902DD~000000000000000000000000000000~YAAQhMgWw4EKjH6NAQAA/bm5rRZHbP8vtllT2Yb61jW3JLWhetiCu9z2Qn8jcqCbxGm/VESzvOmc5r9722b/fXjrTzYXh4yWtHShlepHRVIYTXg+pViJC9ZArpmExUi1+LRnTY1MzfkCGD8+BKLd24Q06fCLfSKKx7vEtX8aw88RpA2KY0NITtYo3QElBeTXfcRGQYU9+LMv/AqVnrBAAVLAS3cFgQntJ+xC4vBx+W7q118oDmh1Lubxx8roYUfPJAwVi4RkcsjU3TPAxL8Gmg3FS7ruRPMU306sjAUXz/LAEmgsnwaemwZMdn2M33g/xwLfsCfwQWG5IqEisHN0hOAE3TBEik42HiivvGM/qrDF1+eeiJSCZg+ffzsL3XCq58wPsvw2XlvQkYlUuUEaxbrfCw0Fbp2SDnNwM9aNpICHx53ydd+C85FHP+bNxfO6TrPjudaTYGFOKJJwmus3Jerzy2GBTyEhxQ2M1oTAJA7q5zj8uz8IQxEfYA/rNqRXcbCt6HQWFki39MvWExCUo9vicp4bgJwCD6AqO4eSEqnFB80=; bm_mi=E8B6B5730BC8867F0AD44BA199A54261~YAAQhMgWw2kKjH6NAQAAPbS5rRb7+bBfhoiSBt1cQRx3c9VwQuwyYZr2pTmKrnZJRL96dF8mXmQQGV0ca6Lo/Lljb+0XXitZnivcqeMdaUWwfmD3c0AO9bZv/8uQNJPzI4uXqA7o0wWCK6ts6N+jNbCVkGjOvb4gPidpnj6IDknYmXmOxZn7KGzqEb3hJNnm4q4tptkEYzBSeNvW2xP8+pEJjkRmdAN1w/p1xa4DfLdUSfrS3ec1BHWPxh7AXK9vOew1M+N3zpfVChJVQGrT1+llMmmSh01GoB7gIH6KsEY94v5YPcFXqvnHiKnWePVNu/K1tY8RseRN24R8L896~1; BVBRANDID=61ae4e41-c3f6-41ae-abd2-b4b47aefd344; BVBRANDSID=66966dda-3742-4907-ae32-bdf5c75bb609; AKA_A2=A; _abck=E48F55AAE866DE433AAC7973158A7D72~0~YAAQ68gWwwV1hoWNAQAAPR+HrQvhm7bO9He+y/8wHdlHuI+tnMwyqq22SBu/kUgB8r0TcSJJM8191qH9MUZUHBIp7CH6igUqu4TO+0Pc0EMsz/BFETRTfC+yw5icuUXorriSEp84pgzszAeeriVHMeHZeaa7fbQPI45/hQ4QtiZwmfXWA5+A56YWebkG35U7+Ii4rKrcZ1vxymwmKhqQ9xxb4d+cQ0jAhTVz4iGZIJqVWhj/7wmEpj3rjHkLBvlUX4uFv28bUFLjmBFTZQJzTE4S0b2qLiXkHElLyneM8URihK2RgW3RWc63hce1a9Sq5JePkYErHruayNWl7UtD/OHL7DNXokKCxhOpcVxKvdVKLZ7YK7n82haLWTjfJDm2Jon/fxl/pbHsSP6SHG5FOcsit4VeU5QHIRr2W+em~-1~-1~1708016930; dwac_9d7af4d525a0a5ec17989f2e04=Hfwl03es4464GpEkKOcKdb-4wa7EHdwS_eg%3D|dw-only|||EUR|false|Europe%2FRome|true; dwsid=JkZFDZnBm1XIbKg7QknArYQCoXAqcKTJjZ74IJzGDp4WrYmne0H3ObL7UwQWBb923GsFKXuvhCzlORMr4cyWYQ==; sid=Hfwl03es4464GpEkKOcKdb-4wa7EHdwS_eg; _sc_cspv=; bm_sz=8F5019715047B36127F7514D46BD564B~YAAQ68gWwxnGhYWNAQAAvUM+rRaz8GGkumG/jAamZS4y5H8dvUGUTbJZSCgaE+9KacX6MeL92eQnOHu0qcQ6CxRafDIgn2HJJykBA6ir5HppFJLPxnYcrJ6yKHFyLc6naCOPxRri23Pz+waqTsgaL0w1Xlc8/ap+mhH5XsqjNXCZ4LQJ1IEHlBHYFOfCPT6GZaRPlFPnmANKNP/IVrFQiAoDYDJiQr5N99CwfydhfvbJwcYqX603l7GPEGn4To6dg58izFhNcCC5o5X+faO2PGqpJ8iMlJ/3wmTJGi2yRyNXrCIyZVidI9OOvv7HsXEMvt9wt0JCNde+7QLfTP1bDeLNA842OvgG02V8moj/+YuMlKcGgg==~3687481~4277318; _cs_c=0; _scid=237b5005-b4be-4043-a834-caefd8f54995; _tt_enable_cookie=1; _ttp=Qrm_BI68h2lvTVft3CMHeAHW1Re; t2s-analytics=a635448f-1da3-4e88-a307-6b450ffae823; TC_PRIVACY=0%40004%7C13%7C1008%402%2C3%2C4%401%401707992078963%2C1707992078963%2C1723544078963%40_v__; TC_PRIVACY_CENTER=2%2C3%2C4; tc_consent_mode_update=actif; TCPID=12424105377900638981; CYB=false; cqcid=efjVbdcnQtZTSTKa1I6xiwNEDP; cquid=||; dtCookie=v_4_srv_20_sn_FTIB7J32NQJ6P6VT4A6EVV9QIHTMQRBB_app-3A923e4e2c2ee0c645_0_ol_0_perc_100000_mul_1; dtSa=-; rxVisitor=17067830486857TQ6MML7O422OU926AVKS0NU76THAMIH; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22XPmk9ZpSonGIn241pUEE%22%7D; dtPC=-85$383048684_728h-vCLICAESCPLQTWCVDCESDHLPQQHFNHBMV-0e0; rxvt=1706784850770|1706783048686; dwanonymous_9ba7b620ffc5ebb782d1bef0c6819ea7=efjVbdcnQtZTSTKa1I6xiwNEDP; akacd_Sephora_IT_PR=2177452799~rv=85~id=e90b2664e6acb2059e08e1e5b58b0571',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
    }


def get_data(product_link):
   
    data_dic = {'pd_id': [], 'size_and_item': [], 'category': [],
                'price': [], 'love_count': [], 'reviews_count': [], 'img': []}
    
    while True:

        try:
            id = re.findall(R'P*[0-9]{3,7}', product_link)[0]
            #print(id)
            if(id not in scraped_ids):
                scraped_ids.append(id)
                data_dic['pd_id'] = id
                print(data_dic['pd_id'])
            else:
                return {}
            
        except:
            return {}
        
        print("ok")
        
        try:
            response = requests.get(product_link, headers=headers, timeout=15)
        except:
            print('error')
            continue
        
        #with open('/Scraping-Sephora-IT/scraper/sephora_item_details.html', 'wb+') as f:
        #    f.write(requests.get(link, headers=headers, timeout=15).content)
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        #get name
        try:
            name_box = soup.find_all('span', class_='product-name')[0]
            name = name_box.contents[0].replace('\n', '')

        except:
            name = None

        #get brand
        try:

            brand_box = soup.find_all('span', class_='brand-name')[0]
            brand = brand_box.contents[0].replace('\n', '')

        except:
            brand = None


        # Get Category
        try:
            cat_box = soup.find_all('div', class_='breadcrumb-element')
            cat_list = []
            for cat in cat_box:
                cat_list.append(cat.find_all('a')[0].text.replace('\n', ''))
               
            category = ', '.join(cat_list[1:])
        except:
            category = None

        # Size and Content
        try:
            size_and_item = soup.find(
                'span', class_='variation-title').get_text().replace('\n', '')
           
        except:
            size_and_item = None

        # Get Price
        try:
            price = soup.find_all('span', class_='price-sales')[0].get_text().replace('\n', '')[:-3]
        except:
            price = None

        # Get love counts
        try:
            love_count = soup.find('span', attrs={
                "itemprop": "ratingValue"}).get_text().replace('\n', '')
        except:
            love_count = None

        # review nums
        try:
            rev = soup.find('span', class_='bv_numReviews_text')
            print(rev.contents[0].replace('\n', ''))
            reviews_count = rev.contents[0].replace('\n', '')
        except:
            reviews_count = None


        # image
        try:
            img = soup.find('img', class_='primary-image')['src']
            #print(img['src'])
        except:
            img = ''

        data_dic['name'] = name
        data_dic['brand'] = brand
        data_dic['category'] = category
        data_dic['size_and_item'] = size_and_item
        data_dic['love_count'] = love_count
        data_dic['reviews_count'] = reviews_count
        data_dic['price'] = price
        data_dic['img'] = img

        print(data_dic)
        break
    return data_dic

pd_links_df = pd.read_csv('/Scraping-Sephora-IT/scraper/data/product_links.csv')
product_links = pd_links_df['product_links']

scraped_df = pd.read_csv('/Scraping-Sephora-IT/scraper/data/pd_info.csv')
#scraped_ids = scraped_df['pd_id']

scraped_ids =[]

print(scraped_ids)

result = []
for i, link in enumerate(product_links[:]):
    print(link)

    data = get_data(link)
    if(data!={}):
        result.append(data)
    pd_df = pd.DataFrame(result)
    pd_df.to_csv('/Scraping-Sephora-IT/scraper/data/pd_info_1.csv', index=False)
    print(f'{i + 1:06d} / {len(product_links)} || {link}')
