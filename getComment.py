import requests
import re
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen, quote
import pandas as pd
import numpy as np
from pylab import *


def getHTMLText(url,page):
    params={
    "appKey" : 'xxxxxxx',
    "dfpId ": 'xxxxxxx',
    'limit': 32, # 每页的店铺信息数
    'offset': 32 * (page-1), # 当前偏移量，第1页为0，第2页为(2-1)*limit
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
        "Cookie": "lt=xxxxxxxx;__mta=xxxxxxx; _lxsdk_cuid=xxxxxxx; ci=1; rvct=1; mtcdn=K; uuid=xxxxxxx;token2=xxxxxxx; iuuid=xxxxxxx; logintype=normal; cityname=%E5%A4%AA%E5%8E%9F; _lxsdk=xxxxxxx; webp=1; i_extend=H__a100002__b1; latlng=xxxxxxx; __utma=xxxxx; __utmz=74597006.1678781794.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; u=539153339; n=y%E7%9C%9F%E5%B7%A7; token2=AgH9Is4Pa_P4URgDbQAKAN1Cbwo0OGKGspXiKziTnyaJXdtpZG2vLYf7wsCIEn-PGMRQJw-Xy1i9KAAAAAAdFwAAJnPo8y2p6-dyDdlngbFyqR_qZsvWBwGT0tm5rbuLxDGcuEktXgeIaENicWKikGfw; unc=y%E7%9C%9F%E5%B7%A7; __mta=150911625.1678803053661.1678803053661.1678803053661.1; firstTime=1678803194415; _lxsdk_s=186e06ba035-d61-088-e2b%7C%7C21"}
    try:
        r = requests.get(url, headers=headers, timeout=100,params=params)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  # 对文本中使用的编码替换整体的编码
        return r.text
    except:
        return "失败"


# 将数据写入csv文件中
def file_data(path,df):
    df.to_csv(path, index=False, sep=',')


def main():


    goods = '九月时光馆（茂业店）'  # 检索词
    depth = 2 # 设置爬取的深度
    start_url = 'https://ty.meituan.com/s/' + goods
    # 以下采用for循环对每个页面URL进行访问
    data={
        '店铺名称':[],
        '店铺地址':[],
        "人均消费":[],
        "店铺评分":[],
        "评价人数":[]
    }
    for i in range(depth):
        try:
            url = start_url + '&offset=' + str(32 * i)
            # url = start_url +  str(32*i)
            html = getHTMLText(url,i)

            id=re.findall(',"avgprice":(.*?),',html)

            # 将每个店铺的信息通过循环写入文件
            for j in range(len(titles)):
                data['店铺名称'].append(titles[j])
                data['店铺地址'].append(addresses[j])
                data['人均消费'].append(avgprices[j])
                data['店铺评分'].append(avgscores[j])
                data['评价人数'].append(comments[j])

        except:
            continue
    df= pd.DataFrame(data=data)
    path='./'+goods+'.csv'
    # file_data(path,df)

if __name__ == '__main__':

    main()
