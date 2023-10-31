# 姓名：郭紫照
import requests
from lxml import etree
import redis
from settings import *

redis_save = redis.StrictRedis(
    host=REDIS['host'],
    port=REDIS['port'],
    db=REDIS['db'],
    password=REDIS['password'],
)


def save_url(url_list):
    redis_save.sadd(REDIS['manta_comp'], url_list)


def function1(string):
    strings = ''.join(string)
    lists = []
    for i in strings:
        j = i
        try:
            if type(int(j)) == int:
                lists.append(i)
        except:
            continue
    return int(''.join(lists))


def requ(url):
    req_data = requests.get(url=url, headers=headers, proxies=proxies).text
    page = etree.HTML(req_data)
    list_result = page.xpath("//*[@class='md:flex md:flex-wrap md:justify-evenly']/a")
    for li in list_result:
        list_need = li.xpath('./@href')[0]
        url_real = 'https://www.manta.com' + list_need
        url_lest.append(url_real)


def requ_first(da, url):
    req_data = requests.get(url=url, headers=headers, proxies=proxies).text
    page = etree.HTML(req_data)
    list_result = page.xpath("//*[@class='py-2']")
    for li in list_result:
        list_need = li.xpath('./a/@href')[0]
        num_data = li.xpath('./text()')
        num_data_real = function1(num_data)
        if da == 1:
            if num_data_real > 10000:
                url_real = 'https://www.manta.com' + list_need
                url_first_list.append(url_real)
            else:
                num = num_data_real // 35 + 1
                url_real = list_need.split('/')[1].replace('mb_', '')
                url_req.append(url_real + ',' + str(num))
        else:
            url_real = list_need.split('/')[1].replace('mb_', '')
            if num_data_real > 10000:
                num = 285
                url_req.append(url_real + ',' + str(num))
            else:
                num = num_data_real // 35 + 1
                url_req.append(url_real + ',' + str(num))


if __name__ == '__main__':
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'refer_id=0000; cust_id=cd44336d-a6e1-41d2-b2d5-3ac05375a707; _gcl_au=1.1.88735228.1686307806; _gd_visitor=6903621e-adee-491a-8eae-2e8653a49c19; _fbp=fb.1.1686307809458.1478275707; _tt_enable_cookie=1; _ttp=B8HYAUYVh84zx-UAoHYirtbmpsZ; cb_user_id=null; cb_group_id=null; cb_anonymous_id=%221d4c7a2d-fdfe-4158-8a79-31391722c5da%22; hubspotutk=39da165b291bf8e7124e34619f558c0a; intercom-id-udror2wm=85c25c39-db36-44a2-95db-afede817ece1; intercom-device-id-udror2wm=18de34af-f391-4d92-90bd-c075ea6358b5; _hjSessionUser_1528605=eyJpZCI6ImQ3NDllMDJhLTdjNTgtNTkxOS05Y2I1LTcwZGY4NDY1YTFiZCIsImNyZWF0ZWQiOjE2ODYzMDc4MTAxMjYsImV4aXN0aW5nIjp0cnVlfQ==; _gd_svisitor=dfac30178f991f00e10383641e03000003ea0900; usprivacy=1---; ad_clicker=false; _cc_id=38674d783fd0e2ca1961845d5fa05c7c; _pbjs_userid_consent_data=3524755945110770; _sharedid=9b855c85-218a-4de7-9c40-9d12c3da60d6; _pw_fingerprint=%229322707da30a08e802ab13bb6d46ef3d%22; _gid=GA1.2.1977951578.1688537257; _lr_env_src_ats=false; intercom-session-udror2wm=; sess_refer=1; panoramaId_expiry=1688718841403; panoramaId=eb23cab644410b21add0002ed8e2a9fb927afe24da5e9b6272a9b0f3d920a4a2; _lr_geo_location=SG; _lr_sampling_rate=100; id5id.1st_123_nb=1; mako_fpc_id=52565470-f672-4f77-835a-aa1dd1f0e58d; cf_clearance=D5.Vwekp3EfFbd_XgQNnjiQs341rXnsnHiBAMlASPzw-1688695599-0-250; _hjIncludedInSessionSample_1528605=1; _hjSession_1528605=eyJpZCI6IjE3ODIwOTUwLTg4ODQtNGI2OS1hYzQ4LTZjNTA2NTM2OWU2YyIsImNyZWF0ZWQiOjE2ODg2OTU3NDIzODksImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; _gd_session=66e154c3-5f6c-4775-85cf-0961916451d6; __hstc=138579948.39da165b291bf8e7124e34619f558c0a.1686307824863.1688537262294.1688695746946.3; __hssrc=1; _ga_E1F369F24C=GS1.1.1688695966.11.0.1688695966.0.0.0; pageDepth=22; _ga=GA1.1.781759093.1686307809; _awl=2.1688695969.5-db7a018398e8794dd6c7899809905ab9-6763652d617369612d6561737431-0; _lr_retry_request=true; FCNEC=%5B%5B%22AKsRol_ySHoyJHixVTPrftE72ABdIaY32GtpzLofyFRZbUTw8-gq2Yz-csJos8KdYcI2VehIwVCqQnfJEfyGo6b6VY593SAwCNgWhU5nOiU5cJo-z9CXrkiigMq2NPvHSjralJ3sgLuA-sQcPEL7qOq0x0Ct3O7p9g%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; cto_bundle=1PrmHV9uWW9BZlQ3Y1U3WFVpZzBSUGQ3WkVQNmpxNSUyRjdpSlZMS2Vmdm1iVW83Mm42UDQ4N3pvelIlMkJXRkhTNFlZZUQweUM2b1dTTkNhUzVleDJGJTJGY3pjbzZOJTJCTEZXRGdva2xGVWsxRE1WcjdJandvQiUyQjlTR0dpJTJCUHM2UEc4ZzlHdjJ2UWJLRTVYR09ZZG5qcUslMkI2dlpublBvdyUzRCUzRA; _ga_B0C8Y3EM2T=GS1.1.1688695740.11.1.1688698461.60.0.0; __gads=ID=c7fe979f6efcb6f1-227783cca3b40045:T=1686307914:RT=1688699325:S=ALNI_MZxrw6JvEhxobxeDeOsQyiTUqtMUA; __gpi=UID=00000c45fb002778:T=1686307914:RT=1688699325:S=ALNI_MZH_maag0Wn-52REGlPRw9C6IKmeg; __cf_bm=Pf4geE.NmO.Et4il5btbvllHW.Z6nU3psSjpzj20Mbw-1688699400-0-AZbjWGkl64EdXUxWY6N5uTXYpSXxb2Nn1xTthZyjRirX3qavuMXWdzwtjxQpn+5igBVw0OXqEF6St9q633ATymKFByQoY5w7hE8CeE7Az3Xs; cf_chl_2=d6d136c7437d081',
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
    url = 'https://www.manta.com/business-directory'
    url_lest = []
    url_first_list = []
    url_req = []
    requ(url)
    print(url_lest)
    for url_first in url_lest:
        requ_first(1, url_first)

    print(url_first_list)
    for j in url_first_list:
        requ_first(2, j)

    print(url_req)
    for data_list in url_req:
        save_url(data_list)
