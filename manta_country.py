import redis
import pymongo
import requests
from lxml import etree
import redis
from settings import *
import json
from selenium.webdriver.chrome.options import Options
import time


class Manta():
    def __init__(self):
        self.init_mongo()
        self.init_redis()

    def init_redis(self):
        self.redis = redis.StrictRedis(
            host=REDIS['host'],
            port=REDIS['port'],
            db=REDIS['db'],
            password=REDIS['password'],
        )
        print('》》》》》radis连接成功')

    def init_mongo(self):
        self.mongo_client = pymongo.MongoClient(host=MONGO['host'], port=MONGO['port'])
        if MONGO['auth']:
            auth = self.mongo_client[MONGO['auth']]
            auth.authenticate(MONGO['username'], MONGO['password'])
        self.mongo_db = self.mongo_client[MONGO['db']]
        self.mongo_coll = self.mongo_db[MONGO['coll']]
        print('>> Connect Mongo Success')

    def request_industry(self, url, berause1):
        try:
            req_data = session.get(url=url, headers=headers, proxies=proxies).text
            data_res = json.loads(req_data)
            result = data_res["companies"]['list']
            print(result, len(result))
            time.sleep(6)
            self.save_data(result, berause1)
        except:
            pass

    def save_data(self, result, berause1):
        for da in result:
            self.mongo_coll.insert_one(da)
        if execution_time >= data:
            self.redis.srem(REDIS['manta_comp'], berause1)
            self.redis.sadd(REDIS['manta_comp_move'], berause1)


if __name__ == '__main__':
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'refer_id=0000; cust_id=cd44336d-a6e1-41d2-b2d5-3ac05375a707; _gcl_au=1.1.88735228.1686307806; _gd_visitor=6903621e-adee-491a-8eae-2e8653a49c19; _fbp=fb.1.1686307809458.1478275707; _tt_enable_cookie=1; _ttp=B8HYAUYVh84zx-UAoHYirtbmpsZ; cb_user_id=null; cb_group_id=null; cb_anonymous_id=%221d4c7a2d-fdfe-4158-8a79-31391722c5da%22; hubspotutk=39da165b291bf8e7124e34619f558c0a; intercom-id-udror2wm=85c25c39-db36-44a2-95db-afede817ece1; intercom-device-id-udror2wm=18de34af-f391-4d92-90bd-c075ea6358b5; _hjSessionUser_1528605=eyJpZCI6ImQ3NDllMDJhLTdjNTgtNTkxOS05Y2I1LTcwZGY4NDY1YTFiZCIsImNyZWF0ZWQiOjE2ODYzMDc4MTAxMjYsImV4aXN0aW5nIjp0cnVlfQ==; _gd_svisitor=dfac30178f991f00e10383641e03000003ea0900; usprivacy=1---; ad_clicker=false; _cc_id=38674d783fd0e2ca1961845d5fa05c7c; _pbjs_userid_consent_data=3524755945110770; _pw_fingerprint=%229322707da30a08e802ab13bb6d46ef3d%22; _lr_env_src_ats=false; intercom-session-udror2wm=; id5id.1st_123_nb=1; mako_fpc_id=52565470-f672-4f77-835a-aa1dd1f0e58d; __hstc=138579948.39da165b291bf8e7124e34619f558c0a.1686307824863.1688537262294.1688695746946.3; cto_bundle=1PrmHV9uWW9BZlQ3Y1U3WFVpZzBSUGQ3WkVQNmpxNSUyRjdpSlZMS2Vmdm1iVW83Mm42UDQ4N3pvelIlMkJXRkhTNFlZZUQweUM2b1dTTkNhUzVleDJGJTJGY3pjbzZOJTJCTEZXRGdva2xGVWsxRE1WcjdJandvQiUyQjlTR0dpJTJCUHM2UEc4ZzlHdjJ2UWJLRTVYR09ZZG5qcUslMkI2dlpublBvdyUzRCUzRA; _awl=2.1688699418.5-db7a018398e8794dd6c7899809905ab9-6763652d617369612d6561737431-0; FCNEC=%5B%5B%22AKsRol96CuYlmU9WB80n7L8HRuGrIPyYL9lEsuoK3qJip2Yoxc7D_kJ5tZCdUGKF3u8S6eaUNSXM2QQLQGky3bhI53XkxXBTQ8L9N0FxxvIIWcYT1yne2HscBNachrnp55Ojfzvf526ScwScUFVEdq_1_yZCat6qNg%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; _ga=GA1.1.781759093.1686307809; __gads=ID=c7fe979f6efcb6f1-227783cca3b40045:T=1686307914:RT=1688705937:S=ALNI_MZxrw6JvEhxobxeDeOsQyiTUqtMUA; __gpi=UID=00000c45fb002778:T=1686307914:RT=1688705937:S=ALNI_MZH_maag0Wn-52REGlPRw9C6IKmeg; _ga_E1F369F24C=GS1.1.1688706935.13.1.1688706935.0.0.0; _ga_B0C8Y3EM2T=GS1.1.1688695740.11.1.1688706935.60.0.0; cf_chl_2=48943f9d8b04961; cf_clearance=4cjU8eLIRcBolZ7irwwMP67NgQcPAd4jDkL0BUrTLMk-1689063324-0-250; city=San%20Jose; state=California; stateAbbrv=CA; lat=37.1835; lon=-121.7714; ipContinent=NA; country=United%20States; ipCountry=US; sess_refer=1; __cf_bm=qEB4QgcBFCkpzkZlqqXGdKpKYaxg5R3jCYXxDGt3C_A-1689063341-0-AWsr+exPzWZYUMC89WEheoYiKiVqZT+0OhmCdgh1XuIvfRWl0KXqAMeveia26BxqpisFEYSHJtZOpazKDT1N3M4WZ/Ha1cJ3gKLVFP0+yFGe',
        # 'refer_id=0000; cust_id=cd44336d-a6e1-41d2-b2d5-3ac05375a707; _gcl_au=1.1.88735228.1686307806; _gd_visitor=6903621e-adee-491a-8eae-2e8653a49c19; _fbp=fb.1.1686307809458.1478275707; _tt_enable_cookie=1; _ttp=B8HYAUYVh84zx-UAoHYirtbmpsZ; cb_user_id=null; cb_group_id=null; cb_anonymous_id=%221d4c7a2d-fdfe-4158-8a79-31391722c5da%22; hubspotutk=39da165b291bf8e7124e34619f558c0a; intercom-id-udror2wm=85c25c39-db36-44a2-95db-afede817ece1; intercom-device-id-udror2wm=18de34af-f391-4d92-90bd-c075ea6358b5; _hjSessionUser_1528605=eyJpZCI6ImQ3NDllMDJhLTdjNTgtNTkxOS05Y2I1LTcwZGY4NDY1YTFiZCIsImNyZWF0ZWQiOjE2ODYzMDc4MTAxMjYsImV4aXN0aW5nIjp0cnVlfQ==; _gd_svisitor=dfac30178f991f00e10383641e03000003ea0900; usprivacy=1---; ad_clicker=false; _cc_id=38674d783fd0e2ca1961845d5fa05c7c; _pbjs_userid_consent_data=3524755945110770; _sharedid=9b855c85-218a-4de7-9c40-9d12c3da60d6; _pw_fingerprint=%229322707da30a08e802ab13bb6d46ef3d%22; _gid=GA1.2.1977951578.1688537257; __hstc=138579948.39da165b291bf8e7124e34619f558c0a.1686307824863.1686307824863.1688537262294.2; _lr_env_src_ats=false; intercom-session-udror2wm=; cto_bundle=vlmjkV9uWW9BZlQ3Y1U3WFVpZzBSUGQ3WkVKalBRbyUyQkRlMWlpYnhpeFpsT1FGMHlhVjRseHNJMk04UUtITlE4eUM2ajFnc2RMM0NUTE12a2FEZnB0QUw5YjMlMkJaWHJNTFRmYmhNYkx5VDJHWTh5U0wybHJWZWt2OTBicW02OXBEbDlNUFlpWCUyRlV0akElMkJQRndCUXlzVVUwbDFFQSUzRCUzRA; sess_refer=1; panoramaId_expiry=1688718841403; panoramaId=eb23cab644410b21add0002ed8e2a9fb927afe24da5e9b6272a9b0f3d920a4a2; _lr_geo_location=SG; _lr_sampling_rate=100; id5id.1st=%20%7B%20%22created_at%22%3A%20%222023-05-22T03%3A33%3A37.291Z%22%2C%20%22id5_consent%22%3A%20true%2C%20%22original_uid%22%3A%20%22ID5*x9AW87r8IV-ej8gNjt6gwlWjRlEBAYURR1Sg3H9feytTx-eIwNPj3dzSPgIvfMPyU8hoUp3g0xQhNmdEpkdx3w%22%2C%20%22universal_uid%22%3A%20%22ID5*eItfM_ba9CFp_dE5bkrZFmi7DPitMk62Kbd3CJIlNHxTxyfgeMOOhKyuoycP7QcuU8j_uX4Pqn26SwyXN170Dw%22%2C%20%22signature%22%3A%20%22ID5_AlQaXrm40v19zMtjR0efX4lOAS2yQKXVPZNdOj0xuRuHHEi5JmALOX7e_-qhOuN8pSpsVXjIdI-rMWNenptb-3NVz-jZIRl8rclbkSu8CefkH6CY7hgTWbm-%22%2C%20%22link_type%22%3A%202%2C%20%22cascade_needed%22%3A%20false%2C%20%22privacy%22%3A%20%7B%20%22jurisdiction%22%3A%20%22other%22%2C%20%22id5_consent%22%3A%20true%7D%2C%20%22ext%22%3A%20%7B%20%22linkType%22%3A%202%7D%2C%20%22cache_control%22%3A%20%7B%20%22max_age_sec%22%3A%207200%20%7D%7D; id5id.1st_last=1688637811193; id5id.1st_123_nb=1; id5id.1st_483_nb=1; mako_fpc_id=52565470-f672-4f77-835a-aa1dd1f0e58d; cf_clearance=FwAkM4qAO.XNCKaCkVz.JWI1awcAfnf9uUDIFvIsj7g-1688638291-0-250; _ga_E1F369F24C=GS1.1.1688632439.10.1.1688638418.0.0.0; pageDepth=18; _ga=GA1.1.781759093.1686307809; _awl=2.1688638422.5-db7a018398e8794dd6c7899809905ab9-6763652d617369612d6561737431-0; FCNEC=%5B%5B%22AKsRol_Me6t8XiR6vFBTEh5tp7EaPNqh9fQ_5Mrm-ILpNypMFdIyOjL9NOhZfAUv3SU9LVxLu7tj85UIOIeRshkLoDNFThcMkdrhagzSmK-X7OImwxF8Rit6-ewnBR7wGYgsVFCbB-0OG01D3ng7vfYVASyN4OWi4g%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; _ga_B0C8Y3EM2T=GS1.1.1688645901.10.0.1688647563.60.0.0; __gads=ID=c7fe979f6efcb6f1-227783cca3b40045:T=1686307914:RT=1688649664:S=ALNI_MZxrw6JvEhxobxeDeOsQyiTUqtMUA; __gpi=UID=00000c45fb002778:T=1686307914:RT=1688649664:S=ALNI_MZH_maag0Wn-52REGlPRw9C6IKmeg; __cf_bm=mg3t_tIJcLM6MzszcwGy04oLPB1UflCjASa.kRl_FC4-1688695599-0-ASh77fMT5TrX3hRxmTBKxMkCisqm2saGeaMXReivTlKhZZ8P6qsHp0OmQ+iRbSdV70hSxMM21NW8O+Tw1E5XmI9SL3mBOPVvfooO2vxEs46c; cf_chl_2=f721ca48c25bd95',
        'Host': 'www.manta.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.manta.com/seo-industry-guide/seo-for-dentists',
        'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "Windows",
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    proxies = {
        'https': 'http://127.0.0.1:7890',
        'http': 'http://127.0.0.1:7890',
    }
    # input('fff')
    manta = Manta()
    # options = Options()
    # # options.binary_location = r'D:\爬虫课件\chromedriver.exe'   # chrome.exe --remote-debugging-port=9526 --user-data-dir="D:\AutomationProfile"
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9526")
    # # C:\Program Files\Google\Chrome\Application\chrome.exe
    # driver = webdriver.Chrome(executable_path=r'D:\爬虫课件\chromedriver.exe', options=options)
    session = requests.session()
    while True:
        berause1 = manta.redis.srandmember(REDIS['manta_comp'])
        if berause1:
            execution_time = 1
            auto = berause1.decode('utf-8')
            data = int(auto.split(',')[-1])
            argument = auto.split(',')[0]
            for i in range(data):
                url_data = 'https://www.manta.com/more-results/{}?pg={}'.format(argument, i + 1)
                manta.request_industry(url_data, berause1)
                execution_time += 1
        else:
            pass
