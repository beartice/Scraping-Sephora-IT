import pandas as pd


product_info = pd.read_csv('/Scraping-Sephora-IT/scraper/data/pd_info_1.csv', names=['pd_id','size_and_item','category','price','love_count','reviews_count','img','name','brand'])


#print(product_info)

result = []
ids = []
dupes = []
for index, row in product_info.iterrows():
    
    id = str(row['pd_id'])
    name = str(row['name']).replace('"', '')
    brand =  str(row['brand']).replace('"', '')
    size = str(row['size_and_item']).replace('"', '')
    cat = str(row['category']).replace('"', '')
    price = str(row['price']).replace('"', '')
    love = str(row['love_count']).replace('"', '')
    rev = str(row['reviews_count']).replace('"', '')
    img = str(row['img']).replace('""','')

    tot = name+brand+size+cat+price+love+rev+img

    if id not in ids:
        ids.append(id)

        if(tot not in dupes):
            dupes.append(tot)

            s = 'INSERT INTO SephoraIT (pd_id,name,brand,size_and_item,category,price,love_count,reviews_count, img) VALUES '
            s = s+ '("'+id+'","'+name+'","'+brand+'","'+size+'","'+cat+'","'+price+'","'+love+'","'+rev+'","'+img+'");'
            result.append(s)

print(result)
with open('/Scraping-Sephora-IT/scraper/data/sql.txt', 'w') as f:
    for item in result:
        f.write(item+"\n")



