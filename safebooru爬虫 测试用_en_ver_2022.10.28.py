#2022.10.28.17:22
#en_ver
#ver 1.6
import urllib
from bs4 import BeautifulSoup
import re
import requests
import time

def inp_tag():
    tag = input('\033[1;35m\nInput the tag/author/character to crawl:\033[0m')
    while True:
        page = input("\033[1;35m\nInput the number of pages to crawl\n(Input 'page' to get the total number of pages):\033[0m")
        if page == 'page':
            get_page('https://safebooru.org/index.php?page=post&s=list&tags=' + tag,tag,'ret')
        else:
            if get_page('https://safebooru.org/index.php?page=post&s=list&tags=' + tag,tag,'not'):
                for i in range(0,40*int(page),40):
                    url = 'https://safebooru.org/index.php?page=post&s=list&tags=' + str(tag) + '&pid=' + str(i)
                    if i == 0:
                        print('\033[1;34mCrawling page 1...\033[0m')
                        url1_parse(url,int(i/40)+1)
                    else:
                        print('\033[1;34mCrawling page %s...\033[0m'%(int(i/40)+1))
                        url1_parse(url,int(i/40)+1)
                time.sleep(1)
                break
            else:
                break

def inp_page():
    while True:
        page = input("\033[1;35m\nInput the number of pages to crawl\n(Input 'page' to get the total number of pages):\033[0m")
        if page == 'page':
            get_page('https://safebooru.org/index.php?page=post&s=list',None,'ret')
        else:
            for i in range(0,40*int(page),40):
                url = 'https://safebooru.org/index.php?page=post&s=list&pid=' + str(i)
                if i == 0:
                    print('\033[1;34mCrawling page 1...\033[0m')
                    url1_parse(url,int(i/40)+1)
                else:
                    print('\033[1;34mCrawling page %s...\033[0m'%(int(i/40)+1))
                    url1_parse(url,int(i/40)+1)
            time.sleep(1)
            break

header = {  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/72.0.3626.121 Safari/537.36'}

def get_page(url,index,retornot):
    print('\033[1;33mGetting...\033[0m')
    req = urllib.request.Request(url = url,headers = header)
    response = urllib.request.urlopen(req)
    res = response.read().decode('UTF-8')
    bs = BeautifulSoup(res,'html.parser')
    try:
        last_page_label = bs.find_all('a',alt = 'last page')
        last_page = int(re.search(r'[0-9]{1,}',str(re.search(r'pid=[0-9]{1,}',str(last_page_label)).group())).group())/40 + 1
        if retornot == 'ret':
            print('\033[1;33m%s pages in total\033[0m'%int(last_page))
        elif retornot == 'not':
            pass
        return True
    except Exception:
        pagination_judge = bs.find_all('div', class_ = 'pagination')
        if len(pagination_judge) == 1:
            print('\033[1;33m1 pages in total\033[0m')
            return True
        elif len(pagination_judge) == 0:
            print("\033[1;33m0 pages in total,no '%s' related pictures found\n\033[0m"%index)
            search()
            return False

def url1_parse(url_1,order):
    try:
        req = urllib.request.Request(url = url_1,headers = header)
        response = urllib.request.urlopen(req)
        res = response.read().decode('UTF-8')
        bs = BeautifulSoup(res,'html.parser')
        last_page = bs.find_all('a',href = re.compile(r".*pid=[0-9]{1,}.*"))
        if len(last_page) == 0:
            print('\033[1;34m1 pages in total\033[0m')
        else:
            last_page = re.search(r'[0-9]{1,}',str(last_page[-1]))
            print('\033[1;34m%s pages in total\033[0m'%(int(int(last_page.group())/40) + 1))
        j = 0
        for i in bs.find_all('span',class_='thumb'):
            global img_id
            j += 1
            img_id = re.findall(re.compile(r'id=[0-9]{1,8}'),str(i))[0][3:10]
            url_2 = 'https://safebooru.org/index.php?page=post&s=view&id=' + img_id
            print('Page %s-Picture %s\t'%(order,j) + url_2)
            url2_parse(url_2)
            time.sleep(1)
    except Exception as error:
        print('\t\t\t\033[0;31;40mError:%s\033[0m'%error)
        print('\t\t\tRetrying...')
        url1_parse(url_1,order)

def url2_parse(url_2):
    try:
        req = urllib.request.Request(url = url_2,headers = header)
        response = urllib.request.urlopen(req)
        res = response.read().decode('UTF-8')
        bs = BeautifulSoup(res,'html.parser')
        full_img_url_list = []
        for i in bs.find_all('meta'):
            full_img_url_list.append(re.findall(re.compile(r'https://safebooru.org//images/[0-9]{0,4}/[a-z0-9]{10,50}.[a-z]{3,4}'),str(i)))
        full_img_url = full_img_url_list[-1][-1]
        print('\t\t\t' + full_img_url)
        img_resources = requests.get(full_img_url,'html.parser').content
        with open(r'./safebooru_photoes/{0}{1}'.format(img_id,re.search(r'.(jpg|png|jpeg|gif|webp|bmp)',full_img_url).group()),'wb') as f:
            f.write(img_resources)
    except Exception as error:
        print('\t\t\t\033[0;31;40mError:%s\033[0m'%error)
        print('\t\t\tRetrying...')
        url2_parse(url_2)

def search():
    while True:
        charge = input('\033[1;35mInput 1 to crawl by tag/author/character\nInput 2 to crawl by page number\nInput 3 to get the total number of pages:\033[0m')
        if charge.isdigit():
            if int(charge) == 1:
                inp_tag()
                break
            elif int(charge) == 2:
                inp_page()
                break
            elif int(charge) == 3:
                get_page('https://safebooru.org/index.php?page=post&s=list',None,'ret')
            else:
                print("\033[1;36mIt's useless to input something else!\n\033[0m")
        else:
            print("\033[1;36mIt's useless to input something else!\n\033[0m")

if __name__ == '__main__':
    search()
    print('\033[1;36mCrawl Done\033[0m')