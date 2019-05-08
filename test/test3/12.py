# coding = utf-8
import re
import requests
from lxml import etree
import time
x = 0
k = 1
class Baiduimg(object):
    def __init__(self):
        # 这里填写你想要爬取的图片的关键字
        self.search_item = "苍井空"

        self.url = "http://image.baidu.com/search/flip?tn=baiduimage&istype=2&ie=utf-8&word={}".format(self.search_item)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
        }

    def get_page_from_url(self,url):
        response = requests.get(url,headers=self.headers)

        return response.content.decode(encoding="utf8")

    def get_data_from_page(self,page):
        """提取页面的数据"""

        #page 转化为element对象
        html = etree.HTML(page)



        p = re.compile(r'"objURL":"http.*?jp[e]?g"')
        b = re.compile(r'"http.*?jpg"')
        result = p.findall(page)

        for i in result:
            img_url = i.replace('"objURL":', "")
            img_urls = b.findall(img_url)

            # print(img_urls)
            if 1 >= len(img_urls) > 0:

                a = img_urls[0]

                if "png" not in a and "fromURL" not in a:
                    a = eval(a)

                    print(a)
                    print("1111")
                    try:

                        response = requests.get(a, headers=self.headers)
                    except:
                        pass
                    global x
                    x += 1
                    print(response)
                    with open(('2/' + '{}.jpg'.format(x)), 'wb') as f:
                        f.write(response.content)
        next_url = html.xpath('//a[contains(text(),"下一页")]/@href')
        if next_url:
            global k
            k+=1
            next_url = 'http://image.baidu.com' + next_url[0]

            print("888888888")
            print("这是第{}页".format(k))
            time.sleep(600)
        else:
            next_url = None
        return next_url

    def run(self):
        # 准备url

        url = self.url
        # 发送请求，获取响应数据
        while url:
            page = self.get_page_from_url(url)

            # 解释数据
            url =self.get_data_from_page(page)

if __name__=='__main__':
    tb = Baiduimg()

    tb.run()
