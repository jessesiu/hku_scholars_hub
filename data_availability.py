from bs4 import BeautifulSoup as bts
import re
import csv
from urllib.request import urlopen
import xlrd
import xlwt

def check_url(url):
    html = urlopen(url).read().decode('utf-8')
    content = bts(html, features='lxml')
    result = True
    if "Item Withheld" in content.title.get_text():
        result = False
    return result

count_plos = 0
count_sc = 0
all_href_plos = []
all_href_sc = []
all_href_excel_plos = []
all_href_excel_sc = []

journal_name = input("Enter the journal name (e.g. plos one): ")
journal_name = journal_name.replace(" ","+")
#print ("you entered " + input_var)
#input the journal name
#journal_name = "plos+one"

#input the year

#search_time = "%5B2016+TO+2018%5D"
search_time = input("Enter the search time (e.g. 2016): ")
#search_time = "2016"

#PLOS ONE
purl = "http://hub.hku.hk/simple-search?query=&location=publication&filter_field_1=journal&filter_type_1=equals&filter_value_1="+journal_name+"&filter_field_2=dateIssued&filter_type_2=equals&filter_value_2="+search_time+"&sort_by=score&order=desc&rpp=25&etal=0&start=0";
print(purl)


fo = open("./test.txt", "w")
fo.write("HKU Scholarhub URL"+"|"+"Manuscript DOI URL"+"|"+"Data Availability Comment"+"\n")


while purl is not None:
    html = urlopen(purl).read().decode('utf-8')
    content = bts(html, features='lxml')

    pages= content.find('ul','pagination pull-right')
    #print (pages)
    next_url = None
    flag = False
    pages_refs = pages.find_all('li')
    for page_ref in pages_refs:
        if page_ref.has_attr('class'):
            flag = True
            continue
        if flag == True:
            next_url = page_ref.find('a')['href']
            break
    #print(next_url)
    if next_url is None:
        purl = None
    elif "simple-search" in next_url:
        purl = 'http://hub.hku.hk'+ next_url
    else:
        purl = None

    titles = content.find_all('div',{"class":"dctitle"})


    for title in titles:
            href = title.find('a')['href']
            count_plos+=1

            href = "http://hub.hku.hk" + href
            #record handle url
            print(href)
            html = urlopen(href).read().decode('utf-8')
            content = bts(html, features='lxml')
            dcdoi = content.find('div',{"class":"dcdoi"})
            doi_link = dcdoi.find('a')['href']
            ##record doi_link
            print(doi_link)
            html = urlopen(doi_link).read().decode('utf-8')
            content = bts(html, features='lxml')
            temp = content.find('div',{"class":"articleinfo"})
            data_comments = temp.find_all('p')
            for comment in data_comments:
                if "Data Availability:" in comment.get_text():
                    ## record data_comment
                    data_comment= comment.get_text().split(':',1)[1].strip()
                    print(data_comment)
                    fo.write(href+"|"+doi_link+"|"+data_comment+"\n")
                    all_href_plos.append(href.strip())

fo.close()



