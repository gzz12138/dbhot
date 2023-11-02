"""
获取询盘详请
"""
import datetime
import time
from datetime import timedelta

import pymysql
from selenium import webdriver
import pymongo, redis
from selenium.webdriver.common.by import By

from get_all_demands import Get_Demands
from setting import *
from lxml.etree import HTML


class Get_Detaiuls():
    num = 0

    def __init__(self):
        self.init_mysql()
        self.init_redis()
        self.init_mongo_loacl()
        self.get_bro()

    def init_redis(self):
        self.redis = redis.StrictRedis(host=REDIS_local['host'], port=REDIS_local["port"], db=REDIS_local["db"])

    def init_mysql(self):
        self.mysql = pymysql.Connection(host=Mysql_local["host"], port=Mysql_local["port"], user=Mysql_local["user"],
                                        password=Mysql_local["password"], database=Mysql_local["database"],
                                        cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.mysql.cursor()

    def init_mongo_loacl(self):
        self.mongo_local = pymongo.MongoClient(
            host=MONGO_local['host'],
            port=MONGO_local['port']
        )

    def get_bro(self):
        self.bro = webdriver.Chrome()
        self.bro.get("https://www.machinetools.com/")
        self.bro.execute_script(
            'document.querySelector("body > div.off-canvas-wrapper > div > div.off-canvas-content > header > section.top-banner > div > nav > div > a:nth-child(1)").click()')
        time.sleep(3)
        self.bro.find_element(By.ID, "email").send_keys("1505903739@qq.com")
        self.bro.find_element(By.ID, "password").send_keys("qaz741852")
        self.bro.find_element(By.ID, "remember_me").click()

        self.bro.execute_script('document.querySelector("#login-button").click()')
        time.sleep(5)
        if "您好, qingling" in self.bro.page_source:
            print("登录成功")
        else:
            input("手动登录，登录后输入任意字符继续")

    def requests_fun(self, url: str):
        self.bro.get(url)
        phone_button = self.bro.find_elements(by=By.XPATH, value='//*[@id="tid-phone-request"]')
        if phone_button:
            phone_button[0].click()
        time.sleep(1)
        self.get_html_data(self.bro.page_source)

    def get_html_data(self, html_str: str):
        html = HTML(html_str)
        field_list = html.xpath('*//div[@class="field"]')
        data = {}
        for field in field_list:
            title_list = field.xpath('.//div[@class="label"]//text()')
            value_list = field.xpath('.//div[@class="value"]//text()')
            data[title_list[0]] = value_list[0]
        content_desc = html.xpath('.//div[@class="text-block"]//text()')
        data["content_desc"] = ''.join(content_desc)
        product_name = html.xpath('/html/body/div[1]/div/div[5]/div[1]/div/div[1]/h1/text()')[0]
        data["product_name"] = product_name
        print(data)
        data.pop("ID #")
        data.pop("Posted")
        demands = {
            "comp_name": data.pop("Company", ""),
            "comp_addr": data.pop("Location", ""),
            "cont_name": data.pop("Name", ""),
            "cont_post": "",
            "comp_tel": data.pop("Phone", ""),
            "cont_homepage": "",
            "comp_email": "",
            "product_name": data.pop("product_name", ""),
            "product_category": "",
            "product_count": "",
            "quantity_unit": "",
            "shipment_condition": "",
            "payment_method": "",
            "content_desc": data.pop("content_desc"),
            "product_desc": "\n".join([f"""{key}: {data[key]}""" for key in data]),
            "additional_requirements": "",
            "delivery_time": "",
            "image_url": "",
            "country": "",
            "updatedAt": datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'),
            "createdAt": datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'),
            "source": "machinetools",
        }
        demands['product_category'] = demands['product_name']
        demands['country'] = demands['comp_addr']

        self.save_data(demands)

    def save_data(self, details: dict):
        comp_tel = details['comp_tel']
        if "+86" in comp_tel or not comp_tel:
            return None
        values_list = []
        key_list = []
        for key, value in details.items():
            if value:
                key_list.append(key)
                values_list.append(value)
        sql = f"""insert into demands ({",".join(key_list)}) VALUES ({",".join(["%s"] * len(key_list))});"""
        self.cur.execute(sql, values_list)
        self.mysql.commit()
        self.num += 1

    def get_url(self):
        conn = self.mongo_local
        db = conn[MONGO_local['db']]
        coll = db[MONGO_local['coll']]
        all_demand = coll.find({"time": {"$regex": (datetime.datetime.now() - timedelta(0)).strftime("%m/%d/22")}})
        for demand in all_demand:
            print(demand)
            yield demand

    def main(self):
        print("采集machinetools最新的询盘")
        Get_Demands().main()
        print("获取今天询盘的url")
        for demand in self.get_url():
            try:
                self.requests_fun(demand["url"])
            except Exception as e:
                print("获取询盘出错")
                print(e)
                if input("是否继续") == "yes":
                    continue
                else:
                    break
        print(f"成功入库{self.num}个询盘")


if __name__ == '__main__':
    # print(Get_Detaiuls().requests_fun("https://www.machinetools.com/en/wanteds/118505-tos-fuq-150-wr-slash-9"))
    Get_Detaiuls().main()
