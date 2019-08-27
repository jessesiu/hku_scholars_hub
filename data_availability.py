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
#input the journal name
journal_name = "plos+one"

#input the year

#search_time = "%5B2016+TO+2018%5D"
search_time = "2016"

#PLOS ONE
purl = "http://hub.hku.hk/simple-search?query=&location=publication&filter_field_1=journal&filter_type_1=equals&filter_value_1="+journal_name+"&filter_field_2=dateIssued&filter_type_2=equals&filter_value_2="+search_time+"&sort_by=score&order=desc&rpp=25&etal=0&start=0";
print(purl)


fo = open("/Users/xiaosizhe/Desktop/temp/test.txt", "w")
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

# print('--------------------------------\n')
# loc = ("/Users/xiaosizhe/Desktop/figshare.xls")
# wb = xlrd.open_workbook(loc)
# worksheet = wb.sheet_by_index(0)
# num_rows = worksheet.nrows - 1
# num_cells = worksheet.ncols - 1
# curr_row = -1
# error_count_plos=0
# error_count_sr=0
# t_count_plos=0
# t_count_sr=0
# while curr_row < num_rows:
#   curr_row += 1
#   row = worksheet.row(curr_row)
#   #print('Row:', curr_row)
#   journal = worksheet.cell_value(curr_row,0)
#   hub_url = worksheet.cell_value(curr_row,1)
#   if 'PLOS' in journal and 'CITYU' not in journal:
#       t_count_plos+=1
#       all_href_excel_plos.append(hub_url.strip())
#       print(hub_url.strip())
#       if check_url(hub_url.strip()) is False:
#         print ("PLOS error: "+hub_url.strip()+"\n")
#         error_count_plos+=1
#
#   # while curr_cell < num_cells:
#   #   curr_cell += 1
#   #   # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
#   #   cell_type = worksheet.cell_type(curr_row, curr_cell)
#   #   cell_value = worksheet.cell_value(curr_row, curr_cell)
#   #   print ' ', cell_type, ':', cell_value
# # For row 0 and column 0
#
# print("For PLOS ONE\n")
# print("Total number in scholarshub search page: "+ str(count_plos) +"\n")
# print("Total number in figshare files: "+ str(t_count_plos) +"\n")
# print("error connection number: " + str(error_count_plos) + "\n")
# print("url in scholarshub search but not in the figshare files\n")
# temp1 = [x for x in all_href_plos if x not in all_href_excel_plos]
# for string in temp1:
#     print (string)
#
# print("url in figshare files but not in scholarshub search\n")
# temp2 = [x for x in all_href_excel_plos if x not in all_href_plos]
# for string in temp2:
#     print (string)





#print(html)

# html = urlopen("http://hub.hku.hk/handle/10722/229358").read().decode('utf-8')
# print(html)

