import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyecharts.charts import *
from pyecharts.components import Table
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
import random
import datetime
from pyecharts.globals import CurrentConfig

CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"

def islabel(df,label):
    res = df.apply(lambda x: label in x['达人标签'],axis = 1)
    return res
def authProcess(df):
    df['认证信息']=df['认证信息'].replace('优质作者 | 美妆博主','美妆博主')
    df['认证信息']=df['认证信息'].replace('优质作者 | 美食博主','美食博主')
    df['认证信息']=df['认证信息'].replace('优质作者 | 时尚博主','时尚博主')
    df['认证信息']=df['认证信息'].replace('优质作者 | 护肤博主','护肤博主')
    df['认证信息']=df['认证信息'].replace('优质作者 | 宠物博主','宠物博主')
    return df
def datInfo(df):
    print('共有数据条数:',len(df))
    print("重复数据条数：",df.duplicated().sum())
    print("缺失数据条数：",df.isnull().sum())
if __name__ == '__main__':
    # 数据读入
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.max_columns',500)
    # pd.set_option('display.width',1000)
    daRen=pd.read_csv('./达人列表_小红书.csv')
    fanseMore=pd.read_csv('./涨粉榜_2021-10.csv')
    mcnList=pd.read_csv('./MCN列表_小红书.csv')
    # print("daRen-------", daRen)
    # print("fanseMore------", fanseMore)
    # print('mcnList--------', mcnList)
    # daRen.info()
    # fanseMore.info()
    # mcnList.info()
    print(daRen.describe())
    print(fanseMore.describe())
    print(mcnList.describe())
#各性别达人占比
    genderDf=daRen.groupby('性别')['小红书号'].count()
    cate = genderDf.index
    data = genderDf.values.tolist()
    pie = (Pie()
           .add('', [list(z) for z in zip(cate, data)])
           .set_global_opts(title_opts=opts.TitleOpts(title="各性别达人占比", subtitle=''))
           .set_global_opts(legend_opts=opts.LegendOpts(is_show=True,
                                                        pos_left='20%',
                                                        pos_bottom='90%'))
           )
    pie.render()
    #各标签达人占比情况,所有标签中 美妆个护的达人最多，其次是无标签达人
    daRen['赞藏粉丝比'] = daRen['赞藏总数'] / daRen['粉丝数']
    daRen['达人标签'].fillna('无',inplace=True)
    labelCount=daRen['达人标签'].value_counts()
    label5=labelCount[labelCount>5]

    pie1 = (Pie()
           .add('', [list(z) for z in zip(label5.index, label5.values.tolist())])
            .set_global_opts(title_opts=opts.TitleOpts(title="各领域达人占比",  pos_left='right',subtitle=''))
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False,
                                                         pos_left='50%',
                                                         pos_bottom='90%'))
           )
    pie1.render()
    #各领域达人粉丝情况，复合标签没有拆分
    fanSum=daRen.groupby('达人标签').agg({'粉丝数':'sum','小红书号':'count','赞藏粉丝比':'mean'})
    fanSum.columns=['总粉丝数','总达人数','赞藏比']
    fanSum['平均粉丝数']=fanSum['总粉丝数']/fanSum['总达人数']
    fanSum=fanSum[fanSum['总达人数']>5].sort_values(by='平均粉丝数',ascending=False)
    fanSum['平均粉丝数']=fanSum['平均粉丝数']
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.max_columns',500)
    pd.set_option('display.width',1000)
    # print(fanSum.head())
    bar = (
        Bar(init_opts=opts.InitOpts(width='1620px',height='400px',theme='dark'))
            .add_xaxis(fanSum.index.tolist())
            .add_yaxis('平均粉丝数', fanSum['平均粉丝数'].tolist())
    )
    bar.render()
    # # 拆分复合标签，拆分开的坏处在于增加了某些复合标签的假粉丝数,singCount是所有的复合标签拆分后label count
    # #小红书中达人最多的三个领域分别是美妆个护、时尚和美食
    singleLabel=set("".join(labelCount.index.tolist()).split(" "))
    singleLabel.remove("")
    singCount=pd.Series()
    for label in singleLabel:
        singCount[label]=daRen[islabel(daRen,label)]['小红书号'].count()
    singCountDF=pd.DataFrame()
    singCountDF['达人标签']=list(singCount.index)
    singCountDF['达人数']=singCount.values
    singCountDF['人数占比']=singCountDF['达人数']/len(daRen)
    for label in singleLabel:
        singCount[label] = daRen[islabel(daRen, label)]['粉丝数'].sum()
    singCountDF['粉丝总数'] = singCount.values
    singCountDF.sort_values(by='人数占比',ascending=False,inplace=True)
    singCountDF5=singCountDF[singCountDF['达人数']>5]
    bar1=(
        Bar(init_opts=opts.InitOpts(width='1950px',height='440px'))
        .add_xaxis(singCountDF5['达人标签'].tolist())
        .add_yaxis('各类别博主数',singCountDF5['达人数'].tolist())
        .add_yaxis('各类别粉丝总数',singCountDF5['粉丝总数'].tolist())
    )
    bar1.render()












