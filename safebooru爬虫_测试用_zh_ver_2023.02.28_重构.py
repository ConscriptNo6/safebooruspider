import os
import time
import urllib.request
from lxml import etree
import requests
import mimetypes

class sbSpider():

    def __init__(self, path, tag, page, proxy = None,):
        
        self.tag = tag
        self.page = page
        self.path = path
        self.header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/72.0.3626.121 Safari/537.36'} #请求头
                
        if not os.path.exists(path):
            os.mkdir(path)
    
    def page_parse(self, url): # 网页解析
        req = urllib.request.Request(url = url, headers = self.header)
        res = urllib.request.urlopen(req)
        html = res.read().decode('UTF-8')
        result = etree.HTML(html)
        return result
    
    def img_download(self,url, img_id): # 图片下载

        # 获取图片扩展名
        res = requests.get(url)
        content_type = res.headers.get('Content-Type')
        file_extention = mimetypes.guess_extension(content_type)

        # 保存图片
        img = res.content
        img_path = f'{self.path}/{img_id}{file_extention}'
        with open(img_path,'wb') as file:
            file.write(img)

    def url_parse(self, url, page):
        page_result = self.page_parse(url) # 解析初级网页
        img_url = page_result.xpath('/html/body/div[6]/div/div[2]/div[1]/span') # 获取每张图片的url
        for url in img_url:
            img_id = url.xpath('.//@id')[0][1:8] # 获取图片id
            img_url_suffix = url.xpath('.//a/@href')[0] # 获取url后缀
            img_detial_url = 'https://safebooru.org/' + str(img_url_suffix)
            img_result = self.page_parse(img_detial_url) # 解析次级网页

            # 判断图像是否被压缩，以便选择对应的节点
            if img_result.xpath('/html/body/div[5]/div/div/@id="resized_notice"'):
                # print('压缩')
                full_img_url = img_result.xpath('/html/body/div[5]/div/div[2]/div[4]/ul/li[3]/a/@href')[0]
                self.img_download(full_img_url, img_id)
                print(img_id)
            else:
                # print('未压缩')
                full_img_url = img_result.xpath('/html/body/div[5]/div/div[1]/div[4]/ul/li[2]/a/@href')[0]
                self.img_download(full_img_url, img_id)
                print(img_id)
            time.sleep(0.5)

    def get_page(self, tag): # 获取总页码数 Gets the total number of pages
        url = 'https://safebooru.org/index.php?page=post&s=list&tags=' + str(tag)
        page_result = self.page_parse(url)
        print(page_result)
        last_page = page_result.xpath('/html/body/div[6]/div/div[2]/div[2]/div/a/@alt="last page"')
        print(type(last_page))

    def crawl(self):
        if not self.tag :
            print('无tag')
        else:
            for i in range(0, 40*int(self.page),40):
                url = 'https://safebooru.org/index.php?page=post&s=list&tags=' + str(self.tag) + '&pid=' + str(i)
                if i == 0: # 第一页
                    self.url_parse(url, int(i / 40) + 1)
                else:
                    self.url_parse(url , int(i / 40) + 1)

test2 = sbSpider('./archive', proxy=None, tag = 'blue_archive', page = 2)
test2.crawl()
#test2.get_page(tag = 'azur_lane')