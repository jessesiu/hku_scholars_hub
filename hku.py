from bs4 import BeautifulSoup as bts
import re
import csv
from urllib.request import urlopen
import xlrd

count = 0
all_href = []
all_href_excel = []
#PLOS ONE
#url = "http://hub.hku.hk/simple-search?query=&location=publication&filter_field_1=journal&filter_type_1=equals&filter_value_1=plos+one&filter_field_2=dateIssued&filter_type_2=equals&filter_value_2=%5B2016+TO+2018%5D&sort_by=score&order=desc&rpp=25&etal=0&start=0";
#Scientific Reports
url = "http://hub.hku.hk/simple-search?query=&location=publication&rpp=25&sort_by=score&order=desc&filter_field_1=journal&filter_type_1=equals&filter_value_1=scientific+reports&filter_field_2=dateIssued&filter_type_2=equals&filter_value_2=%5B2016+TO+2018%5D"
while url is not None:
    html = urlopen(url).read().decode('utf-8')
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
        url = None
    elif "simple-search" in next_url:
        url = 'http://hub.hku.hk'+ next_url
    else:
        url = None

    titles = content.find_all('div',{"class":"dctitle"})

    for title in titles:
            href = title.find('a')['href']
            count = count + 1
            href = "http://hub.hku.hk" + href
            print(href)
            all_href.append(href.strip())


#PLOS ONE
#loc = ("/Users/xiaosizhe/Desktop/plosone.xls")
#Scientific Reports
loc = ("/Users/xiaosizhe/Desktop/report.xls")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

# For row 0 and column 0
sheet.cell_value(0, 0)

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
error_count=0
f_count=0
for i in range(sheet.nrows):
    #print(sheet.cell_value(i, 0))
    url = sheet.cell_value(i, 0)
    all_href_excel.append(url.strip())
    f_count+=1
    html = urlopen(url).read().decode('utf-8')
    content = bts(html, features='lxml')
    if "Item Withheld" in content.title.get_text():
        print ("error: "+url+"\n")
        error_count+=1
print("Total number in search page: "+ str(count) +"\n")
print("Total number in excel file: "+ str(f_count) +"\n")
print("error connection number: " + str(error_count) + "\n")
print("url in current search but not in the excel file\n")
temp1 = [x for x in all_href if x not in all_href_excel]
for string in temp1:
    print (string)

print("url in excel file but not in current search\n")
temp2 = [x for x in all_href_excel if x not in all_href]
for string in temp2:
    print (string)

#print(html)

# html = urlopen("http://hub.hku.hk/handle/10722/229358").read().decode('utf-8')
# print(html)