import time
import requests
from requests.exceptions import RequestException
import re
import json
def get_one_page(url):
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
             'Cookie': '__mta=121577271.1592811794557.1593236405572.1593236421267.10; uuid_n_v=v1; uuid=070D6250B45C11EAB787AF911C0DA1B78F65D33D5D8146AB99E59E5BF7F44DB9; _lxsdk_cuid=172dafb2b03c8-0f4ce97d09025-f7d1d38-e1000-172dafb2b04c8; _lxsdk=070D6250B45C11EAB787AF911C0DA1B78F65D33D5D8146AB99E59E5BF7F44DB9; mojo-uuid=e9819b9002aabe323c917cecc03d6955; _csrf=327730935398b142dd32ad44ad3c208d4a919e1a7b078f81343582b0060aff98; mojo-session-id={"id":"eb9735fa3257d1cb6c1713762dd78327","time":1593236351462}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592811793,1593236351; mojo-trace-id=10; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593236421; _lxsdk_s=172f4496e4c-bb4-d86-ad5%7C%7C12'}
             #可以先拿到Cookie,不然只能爬取一部分,可能是其中会出现身份验证
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None
def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                        + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                        + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    for item in re.findall(pattern,html):
        yield{                                          #yield生成器：在main函数中for每次循环迭代出一个作品的相关信息进行后续处理
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }
def write_to_file(text):
    with open('ret.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(text,ensure_ascii=False)+'\n')   #json.dumps()方法把字典序列化,不然无法写入文件
                                                            #ensure_ascii=False保证能写入中文
def main(offset):
    url='https://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    for text in parse_one_page(html):
        print(text)
        write_to_file(text)
if __name__=='__main__':
    for i in range(10):
        main(i*10)
        time.sleep(1)       #防反爬虫