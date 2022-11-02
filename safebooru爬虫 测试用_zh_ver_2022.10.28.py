import urllib
from bs4 import BeautifulSoup
import re
import requests
import time

def inp_tag(): #按tag/作者/角色名爬取 #*当要爬取的tag/作者/角色相关图片名为空时会报错(已解决)
    tag = input('\033[1;35m\n输入要爬取的tag/作者/角色名:\033[0m') #获取需要爬取的tag
    while True:
        page = input('\033[1;35m\n输入要爬取的页数(输入page以获取所有页数):\033[0m') #获取需要爬取的页码数
        if page == 'page':
            get_page('https://safebooru.org/index.php?page=post&s=list&tags=' + tag,tag,'ret') #调用get_page函数获取所有页数
        else:
            if get_page('https://safebooru.org/index.php?page=post&s=list&tags=' + tag,tag,'not'): #判断布尔值,调用get_page函数检测所选的tag/作者/角色名相关图片是否为空,不为空则继续向下执行
                for i in range(0,40*int(page),40): #safebooru的第一页url结尾为0,第二页结尾为40,以此类推
                    url = 'https://safebooru.org/index.php?page=post&s=list&tags=' + str(tag) + '&pid=' + str(i) #完整的某一页的url
                    if i == 0:
                        print('\033[1;34m正在爬取第1页...\033[0m')
                        url1_parse(url,int(i/40)+1) #调用url1_parse函数开始解析
                    else:
                        print('\033[1;34m正在爬取第%s页...\033[0m'%(int(i/40)+1)) #输出正在爬取的页码数
                        url1_parse(url,int(i/40)+1) #调用url1_parse函数开始解析
                time.sleep(1)
                break
            else: #所选的tag/作者/角色名相关图片为空,跳出循环
                break

def inp_page(): #按页码爬取
    while True:
        page = input('\033[1;35m\n输入要爬取的页数(输入page以获取所有页数):\033[0m') #获取需要爬取的页码数
        if page == 'page':
            get_page('https://safebooru.org/index.php?page=post&s=list',None,'ret')
        else:
            for i in range(0,40*int(page),40): #safebooru的第一页url结尾为0,第二页结尾为40,以此类推
                url = 'https://safebooru.org/index.php?page=post&s=list&pid=' + str(i) #完整的某一页的url
                if i == 0:
                    print('\033[1;34m正在爬取第1页...\033[0m')
                    url1_parse(url,int(i/40)+1) #调用url1_parse函数开始解析
                else:
                    print('\033[1;34m正在爬取第%s页...\033[0m'%(int(i/40)+1)) #输出正在爬取的页码数
                    url1_parse(url,int(i/40)+1) #调用url1_parse函数开始解析
            time.sleep(1)
            break

header = {  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/72.0.3626.121 Safari/537.36'} #请求头

def get_page(url,index,retornot): #获取总页码数 #*last_page处可能有问题,如果所选的tag/作者/角色名只有一页的话,会报错,待测试(已解决)
    print('\033[1;33m获取中...\033[0m')
    req = urllib.request.Request(url = url,headers = header)
    response = urllib.request.urlopen(req)
    res = response.read().decode('UTF-8')
    bs = BeautifulSoup(res,'html.parser')
    try: #如果tag/作者/角色名相关的图片有两页及以上时,直接输出页码数,有一页或无相关图片时,触发异常捕获
        last_page_label = bs.find_all('a',alt = 'last page')
        last_page = int(re.search(r'[0-9]{1,}',str(re.search(r'pid=[0-9]{1,}',str(last_page_label)).group())).group())/40 + 1
        if retornot == 'ret':
            print('\033[1;33m总页数为%s页\033[0m'%int(last_page))
        elif retornot == 'not':
            pass
        return True #所选的tag/作者/角色名相关图片不为空,返回真
    except Exception:
        pagination_judge = bs.find_all('div', class_ = 'pagination')
        if len(pagination_judge) == 1: #根据网页源码,匹配到'class="pagination"'div的标签即为相关图片有一页
            print('\033[1;33m总页数为1页\033[0m')
            return True #所选的tag/作者/角色名相关图片不为空,返回真
        elif len(pagination_judge) == 0: #未匹配到即为无相关图片
            print('\033[1;33m总页数为0页,未找到和"%s"相关的图片\n\033[0m'%index)
            search()
            return False #所选的tag/作者/角色名相关图片为空,返回假

def url1_parse(url_1,order):
    try:
        req = urllib.request.Request(url = url_1,headers = header)
        response = urllib.request.urlopen(req)
        res = response.read().decode('UTF-8')
        bs = BeautifulSoup(res,'html.parser')
        last_page = bs.find_all('a',href = re.compile(r".*pid=[0-9]{1,}.*"))
        if len(last_page) == 0: #当匹配不到"last page"标签,即last_page为空时,根据网页源码,tag/作者/角色名相关的图片只有一页
            print('\033[1;34m总页数为1页\033[0m')
        else:
            last_page = re.search(r'[0-9]{1,}',str(last_page[-1])) #*当所选的tag/作者/角色名只有一页时,匹配不到"last page"标签,会报错:list index out of range(已解决)
            print('\033[1;34m总页数为%s页\033[0m'%(int(int(last_page.group())/40) + 1))
        j = 0
        for i in bs.find_all('span',class_='thumb'): #遍历所有class为thumb的含有图片ID的span标签
            global img_id #定义img_id为全局变量,后面给图片命名会用到
            j += 1
            img_id = re.findall(re.compile(r'id=[0-9]{1,8}'),str(i))[0][3:10] #按照正则表达式匹配图片的ID
            url_2 = 'https://safebooru.org/index.php?page=post&s=view&id=' + img_id #每张图片单独的url
            print('第%s页-第%s张\t'%(order,j) + url_2)
            url2_parse(url_2) #调用url2_parse函数以解析每张图片单独的url
            time.sleep(1)
    except Exception as error:
        print('\t\t\033[0;31;40m出错了:%s\033[0m'%error)
        print('\t\t重试中...')
        url1_parse(url_1,order)

def url2_parse(url_2):
    try:
        req = urllib.request.Request(url = url_2,headers = header)
        response = urllib.request.urlopen(req)
        res = response.read().decode('UTF-8')
        bs = BeautifulSoup(res,'html.parser')
        full_img_url_list = [] #创建一个列表用来存放匹配到的所有的图片url
        for i in bs.find_all('meta'): #遍历所有的meta标签以寻找图片url
            full_img_url_list.append(re.findall(re.compile(r'https://safebooru.org//images/[0-9]{0,4}/[a-z0-9]{10,50}.[a-z]{3,4}'),str(i))) #将匹配到url存入列表中
        full_img_url = full_img_url_list[-1][-1] #取列表最后一个元素的最后一个元素,即字符串形式的最终的url
        print('\t\t' + full_img_url)
        img_resources = requests.get(full_img_url,'html.parser').content #保存图片
        with open(r'./safebooru_photoes/{0}{1}'.format(img_id,re.search(r'.(jpg|png|jpeg|gif|webp|bmp)',full_img_url).group()),'wb') as f: #*.jpeg格式的图片会漏掉.(已解决)
            f.write(img_resources)
    except Exception as error:
        print('\t\t\033[0;31;40m出错了:%s\033[0m'%error)
        print('\t\t重试中...')
        url2_parse(url_2)

def search():
    while True:
        charge = input('\033[1;35m扣1按tag/作者/角色名爬取|扣2按页码爬取|扣3获取总页码数:\033[0m')
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
                print('\033[1;36m扣别的没用!\n\033[0m')
        else:
            print('\033[1;36m扣别的没用!\n\033[0m')

if __name__ == '__main__':
    search()
    print('\033[1;36m爬取完成\033[0m')