import gzip
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests

url = "https://www.sephora.it/marques/de-a-a-z/"
print(url)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie' :  'bm_sv=166BFF1C119C8F44C28CE657DA8052D8~YAAQhMgWw/h/i36NAQAA/XtdrRb6LKQhl52Xd3wA6738DP4RSVwCqZ5nSU+kQDJDR2PR+1KUcPKRNvEshd1bVjWdBWbG9/xokQDhZrUUH0ZlBN2uk96+UXlNC1X90Wy0tK8B8MIfmsCb/4DSyulc/mKdM1zx2nqG07j99AgNFjL1Zfn2EV2r/vHfkn3MJzs3zttFr6aMQH8NmhrfQngdro0Fku5ta7qe2XxyT4hsgIHerZz0uZgfehh8Ibj96gL4tA==~1; __cq_dnt=0; dw_dnt=0; ABTasty=uid=awn4gdwr6qh18gkv&fst=1706783050206&pst=1708008557193&cst=1708010569557&ns=6&pvt=22&pvis=2&th=; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.sephora.it%252Fmarques%252Fde-a-a-z%252F; _cs_id=06802916-6fc5-a54d-9a73-2f9bc12dedfe.1707992083.3.1708010587.1708010569.1.1742156083669.1; _cs_s=2.0.0.1708012387998; _fbp=fb.1.1707992083758.1903446801; _ga_2YZ9FQ8XWV=GS1.1.1708010540.6.0.1708010575.0.0.0; _ga_JF05BE885E=GS1.1.1708010540.6.0.1708010575.0.0.0; RT="z=1&dm=sephora.it&si=4f2df800-32ba-4737-87ba-7882300d876d&ss=lsnc6znm&sl=4&tt=hvr&bcn=%2F%2F684dd330.akstat.io%2F&hd=16jvj"; __cq_seg=; __cq_uuid=efjVbdcnQtZTSTKa1I6xiwNEDP; cto_bundle=OyxMg19tNUFIQmtickh2b0R2MzlZaUtBZVR2akVKRlh6UFIlMkZacWJ4OElJVURRZ3BJemxoSWJVazlINk5sT0doUk4lMkY3TVA0UmJodWVFTHNiYWlCdXZFYzhSYmwwTXVuMkVIVjlnSE5hdkFyR2l1ZVMwZTBNcHUwaCUyRm9CSFNacWw0enJGbQ; _pin_unauth=dWlkPU1UWXlZV1ppTjJNdE5Ea3pOQzAwTXpSbExXRXdaak10TlRBNFpqTmlOR1UzWkdGbQ; _screload=; _ga=GA1.2.498181226.1707992081; _gac_UA-87625978-8=1.1707992081.CjwKCAiAibeuBhAAEiwAiXBoJFPddECm0Qp3_z1qVDW4GE--SidptAxjru7MLqKPSKqWoWE-t9rbqxoCvh0QAvD_BwE; _gcl_au=1.1.510950238.1707990786; _gcl_aw=GCL.1707992078.CjwKCAiAibeuBhAAEiwAiXBoJFPddECm0Qp3_z1qVDW4GE--SidptAxjru7MLqKPSKqWoWE-t9rbqxoCvh0QAvD_BwE; _gid=GA1.2.886878786.1707992081; _scid_r=237b5005-b4be-4043-a834-caefd8f54995; _uetsid=09c5b860cbeb11ee922d3b1a5e8525f3; _uetvid=0e4ccf00c0ec11eeb25b27a023964569; tCdebugLib=1; tc_AbTastyConsent=true; tc_compteur_page=21; offers=%7B%22resultCountOffers%22%3A0%2C%22isOffersViewed%22%3Atrue%2C%22offerIDs%22%3A%5B%5D%2C%22firstOffer%22%3A%22%22%7D; tc_cj_v2=%5Ecl_%5Dny%5B%5D%5D_mmZZZZZZKQJRJJROSOPRLZZZ%5D; tc_cj_v2_cmp=; tc_cj_v2_med=; _sc_cspv=; AKA_A2=A; ak_bmsc=C155D483781FEDCBBFEE740D671781E0~000000000000000000000000000000~YAAQ68gWwy7GhYWNAQAAAVY+rRYuJi5XKRcFKo0BP79QPzapgGIbudYewCOUrShM9xlMnW4+X4ZVMatlwhFYxgrJntXONCgdjjkJC2O/GcahSkBd0fHXB+KdfaL7QPwE08BARoT+RB+55aA3L6mKybJOoKDd71V3TCbfL0KADxU1Yt6XKzJCG+Ble06RES5BrV/705t2/g0rjMaf7bbchRIAvLzcLCQclz/qkar3tntGSTsiA8iUg/xpffuUezFXUPGKGmMUPzKPO4t+ODuqwupxvpuLnAW/PCo5y03OGONfWs2+pf28dec+i6vjD74V/4oh35j0y1rysp4zThILq2j9kYWoXVRBchb++V3Hzd+t/O4ox9yuPof66pKcuQmZAlILKhNSpSvpybdwHevQChXjuLYLvoTelgx+SVPEp6E2JQpQxT21fTET3podnrlgZG3XS6tMm6AU5OzGqgrb3TZvTRPhfie6VB/uNvgSsQZA//q7FezBELE9wghIxzu9rPDoWga1WeNzt61io7XizBUWokI+9eQF8dUeL6aP1lgSsR00JajABq+V7KMBrVMIZqIOdASx92bjuRNa2B1YY+sSH9oNv1GCTSzG5NTLJQBo2bVyOXw=; t2s-p=a635448f-1da3-4e88-a307-6b450ffae823; _abck=E48F55AAE866DE433AAC7973158A7D72~0~YAAQ68gWwxvGhYWNAQAAAEY+rQu0zs5CkF1OhKbRifMWwDr3GzA6J0zegZFGEeAQRRfr75yxTd1oGKqCUxkmjCY09cUX50DOKNWB642/TVm0Jtc4ySI5JGktuUoKbdSOqyJG3wrUiFI58XPIvNJdPLIXO9C2GKWzl8Jy4uCd62quw2c5TQwPl6NQp0xvzmYmJxRFb0rgS4k5oYsWlkAx5jOdyqlzTcDcGS8s5hviCUAJ1mmYAuQrwLoBnhsISOBP+4QzFCQ9Kd+9WId5qxU/rye6YrFRsHCa9OgsWEuAFvQiF9pZsjtyBDfaitjzw8lq6Gqg9EWzkvKzeLj+tmHJzHsZY+KYB189gaFOgWo7gWKNavFOksZ9oXQV+APblf7U3EDgzGP/UnoeBuo2/e5GZ8XV2DHxuW7bRo82XnOM~-1~-1~1708012156; bm_mi=0D18CC7FFCF95AE3231DA98AF3DAF70D~YAAQ68gWwyfGhYWNAQAAbkc+rRZAiAVsFTxaJ4DdLRfMr9NBJEjv2OAD61p22itGbVKfE0LegWFWxZrvjGnMFGZ+DvV4PvjwSXPtL14ugfCHzT+nJAol/hyt0jYexl/Hymv2uy5rAW8fPgxXFK0wNf/GBSULQl2dRb9ZaZ9BBFG8EApV2Ul6GFgbJFZDqdRMrz6jK5OVYcWqHECPolOmC63yz4RxEIZDx5B1abGxOQwaidWH+pXXHD8jp5S5hj44MciXb67UEj3ZsmZbB8nk4wq1bAPb3sIAS/dUjTQVKKb37grnvFp+oQ0/s/P5Lvi6uwvz1TW19yZXroAHIr07fonTbfUzK75t+xNTlCFNT2qYyYl6xrp5B6nyUZLSA83nMfUhPrlxByZtSiSMES3mv1fS6UXrDbW91+9CDDpK~1; bm_sz=8F5019715047B36127F7514D46BD564B~YAAQ68gWwxnGhYWNAQAAvUM+rRaz8GGkumG/jAamZS4y5H8dvUGUTbJZSCgaE+9KacX6MeL92eQnOHu0qcQ6CxRafDIgn2HJJykBA6ir5HppFJLPxnYcrJ6yKHFyLc6naCOPxRri23Pz+waqTsgaL0w1Xlc8/ap+mhH5XsqjNXCZ4LQJ1IEHlBHYFOfCPT6GZaRPlFPnmANKNP/IVrFQiAoDYDJiQr5N99CwfydhfvbJwcYqX603l7GPEGn4To6dg58izFhNcCC5o5X+faO2PGqpJ8iMlJ/3wmTJGi2yRyNXrCIyZVidI9OOvv7HsXEMvt9wt0JCNde+7QLfTP1bDeLNA842OvgG02V8moj/+YuMlKcGgg==~3687481~4277318; _cs_c=0; _scid=237b5005-b4be-4043-a834-caefd8f54995; _tt_enable_cookie=1; _ttp=Qrm_BI68h2lvTVft3CMHeAHW1Re; t2s-analytics=a635448f-1da3-4e88-a307-6b450ffae823; TC_PRIVACY=0%40004%7C13%7C1008%402%2C3%2C4%401%401707992078963%2C1707992078963%2C1723544078963%40_v__; TC_PRIVACY_CENTER=2%2C3%2C4; tc_consent_mode_update=actif; TCPID=12424105377900638981; CYB=false; dwac_9d7af4d525a0a5ec17989f2e04=P1AOB8kk4F7aYd-So3WgGUp5ZpOyaOZPx1A%3D|dw-only|||EUR|false|Europe%2FRome|true; dwsid=OW3J2Dj7US_QNEWGlcidrUxEoUxDt1c-zQX5r0QqgYd3nlr6xpYPF1w38LnYaEYuhdkeYifu1AQex6r9KYl-Tg==; sid=P1AOB8kk4F7aYd-So3WgGUp5ZpOyaOZPx1A; cqcid=efjVbdcnQtZTSTKa1I6xiwNEDP; cquid=||; dtCookie=v_4_srv_20_sn_FTIB7J32NQJ6P6VT4A6EVV9QIHTMQRBB_app-3A923e4e2c2ee0c645_0_ol_0_perc_100000_mul_1; dtSa=-; rxVisitor=17067830486857TQ6MML7O422OU926AVKS0NU76THAMIH; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22XPmk9ZpSonGIn241pUEE%22%7D; dtPC=-85$383048684_728h-vCLICAESCPLQTWCVDCESDHLPQQHFNHBMV-0e0; rxvt=1706784850770|1706783048686; dwanonymous_9ba7b620ffc5ebb782d1bef0c6819ea7=efjVbdcnQtZTSTKa1I6xiwNEDP; akacd_Sephora_IT_PR=2177452799~rv=85~id=e90b2664e6acb2059e08e1e5b58b0571',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
    }

#with open('/Scraping-Sephora-IT/scraper/sephora_brands.html', 'wb+') as f:
#    f.write(requests.get(url, headers=headers).content)

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

# Scraping brand links and save them into a list
brand_link_lst = []
brand_name_lst = []

main_box = soup.find_all('a', class_='sub-category-link', href=True)


for item in main_box:
    brand_name_lst.append(item.contents[0])
    brand_link_lst.append(item['href'])
    
    
# Indicate scraping completion
print(f'Got All Brand Links! There are {len(brand_link_lst)} brands in total.')

new_brands = []

for link in  brand_link_lst:
    if 'marche' not in link:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_box = soup.find_all('a', attrs={"title": "Scopri tutti i prodotti"})
        try:
            new_brands.append(main_box[0]['href'])
        except:
            new_brands.append(link)

    else:
        new_brands.append(link)


# Write brand links into a file:
with open('/Scraping-Sephora-IT/scraper/data/brand_names.txt', 'w') as f:
    for item in brand_name_lst:
        f.write( item)


