"""
抓取所有询盘数据
"""
import time

import pymongo
import redis
import requests
from lxml.etree import HTML

from setting import *


class Get_Demands():
    def __init__(self):
        self.init_mongo_loacl()
        self.init_redis_local()

    def init_mongo_loacl(self):
        self.mongo_local = pymongo.MongoClient(
            host=MONGO_local['host'],
            port=MONGO_local['port']
        )

    def init_redis_local(self):
        self.redis = redis.StrictRedis(host=REDIS_local['host'], port=REDIS_local['port'], db=REDIS_local['db'])

    def request_fun(self, url):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Cookie": "_mt_suid=IjU4MjExOSI%3D--f14d70127cb1b89f1e245974fb4a6b66b14ea017; _mt_sutoken=Ijg3NDVmNzU3NWI3NjllNWM1NTYzOTBmNWFjZGIzNiI%3D--be1f577b85a703907a117122708ee52b882fee54; _mt_uat-v2=eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqRXdORGRtTmpkalpqYzVNR1E1TkdaaVltTTBPVGsyTldKbE9UQmhaV05rWWpZeU16aGpOMll4WWpFd05qa3pNbUZrWkRaaFptTTJZemhsTXpnMVlqRWkiLCJleHAiOiIyMDIzLTAyLTA4VDA2OjAzOjExLjM0MFoiLCJwdXIiOm51bGx9fQ%3D%3D--d40d5d1b35d0d911ba0704af8053a4d3c24de04f; breakpoint=xxlarge; _mt_session=wXxvEcbxS8qetL7IQuOQQFPpNb5h9WWG%2FOJv3RRS9tlc8KZ2UekAwHuOVd3QUvNcVRcTaJfO8M9awx8fUcGlk26mG7OxO%2FD%2Bc%2B1o74HuEntIiYzrFzlgg2UYUaL6AGUtexlTxOsmDw82XcIDTkU%3D--LwuBkNFgEROoOrHA--x1FihepRoQs%2FG39MQYOOSg%3D%3D",
            "Host": "www.machinetools.com",
            "Referer": "https://www.machinetools.com/en/wanteds/recent?_page_size=200&page=2&sort_col=type_name&sort_dir=asc",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
        port = 49794
        proxies = {
            "http": f"http://127.0.0.1:{port}",
            "https": f"http://127.0.0.1:{port}",
        }
        res = requests.get(url, headers=headers, proxies=proxies)
        html_str = res.text
        return self.get_data(html_str)

    def get_data(self, html: str):
        Html = HTML(html)
        div_list = Html.xpath('//div[@class="card"]')
        demands_list = []
        for div in div_list:
            demand_data = {}
            title_list = div.xpath('.//h3//text()')
            title = " ".join(title_list) if title_list else ""
            demand_data["title"] = title
            time_str_list = div.xpath('.//div[@class="time"]/span/span/@data-tip-text')
            demand_data["time"] = time_str_list[0]
            url_lsit = div.xpath('.//h3/a[1]/@href')
            demand_data["url"] = "https://www.machinetools.com/" + url_lsit[0]
            demands_list.append(demand_data)
        return demands_list

    def du_demand(self, demand_url: str):
        return self.redis.sadd(REDIS_local['key_du_demand'], demand_url)

    def save_demand(self, demand_list: list):
        conn = self.mongo_local
        db = conn[MONGO_local['db']]
        coll = db[MONGO_local['coll']]
        for demands in demand_list:
            if self.du_demand(demands['url']):
                print(demands)
                coll.insert_one(demands)

    def get_url(self):
        for page_num in range(1, 3):
            url = f"https://www.machinetools.com/en/wanteds/recent?_page_size=200&page={page_num}&sort_col=type_name&sort_dir=asc"
            yield url

    def main(self):
        for url in self.get_url():
            demands_list = self.request_fun(url)
            if not demands_list:
                print("没有询盘")
                break
            self.save_demand(demands_list)
            time.sleep(10)
        print(f"本次共抓取{len(self.redis.smembers(REDIS_local['key_du_demand']))}询盘")


if __name__ == '__main__':
    Get_Demands().main()
