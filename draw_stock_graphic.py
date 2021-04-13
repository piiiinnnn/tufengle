# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import requests
import time

font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14) 
today = time.strftime("%Y-%m-%d", time.localtime())

conf = {
        'sid':'6039931',
        'ios':1,#plt的交互开关
        'method':1, #数去获取方式，0是从file_path，1是从web_url
        'file_path':r'C:\Users\capta\Desktop\6016181(中国中冶).txt',
        'web_url':""
        }
sid = conf['sid']
conf.update({'web_url':"http://push2ex.eastmoney.com/getStockFenShi?pagesize=1000000&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj&pageindex=0&id=%s&sort=1&ft=1&code=%s&market=%s"%(sid,sid[:-1],sid[-1])})

def get_data():

    def get_data_from_txt(fp):
        '''
        从txt文件(从东方财富web获取的数据转存到txt)里获取数据，并转化成字典，形如{price1：[value1，value2...],price2：[value1，value2...]...}
        :param fp: file_path
        :return:
        '''
        with open(fp) as f:
            content = f.read()
            data = json.loads(content)['data']['data']
            price_vol_table = {}
            for i in data:
                t = i['t']
                p = str(i['p'])
                v = i['v']
                bs = i['bs']
                v = 0-v if bs==1 else v
                if t >= 93000:
                    if p not in price_vol_table.keys():
                        price_vol_table.update({p:[v]})
                    else:
                        price_vol_table[p].append(v)
            return price_vol_table
    def get_data_from_web(url):
        '''
            从东方财富web获取数据，并转化成字典，形如{price1：[value1，value2...],price2：[value1，value2...]...}
            :param fp: web_url3
            :return:
            '''
        content = requests.get(url).text
        data = json.loads(content)['data']['data']
        price_vol_table = {}
        for i in data:
            t = i['t']
            p = str(i['p'])
            v = i['v']
            bs = i['bs']
            v = 0-v if bs==1 else v
            if t >= 93000:
                if p not in price_vol_table.keys():
                    price_vol_table.update({p:[v]})
                else:
                    price_vol_table[p].append(v)
        return price_vol_table            
    if  conf['method']==1:
        return get_data_from_web(conf['web_url'])
    elif conf['method']==0:
        return get_data_from_txt(conf['file_path'])
    else:
        print('wrong method value')

def color(i):
    if i<0:
        return '#00ab69'
    elif i==0:
        return 'gray'
    else:
        return '#f12555'
def plan_a():
    # 交互循环
    history_y = []
    plt.ion()
    while True:
        #清空plt
        plt.clf()

        plt.xticks(rotation=60)#x轴旋转60度
        plt.title(conf['sid'][:-1]+today.join('()'), fontproperties=font)
        price_vol_table = get_data()

        x = [i for i in price_vol_table.keys()]
        x.sort()
        if not history_y:
            history_y = [sum(price_vol_table[i]) for i in x]
        y = [sum(price_vol_table[i]) for i in x]
        maggin = int((max(y)-min(y))*2/600)
        # diff_y  = list(map(lambda x: x[0]-x[1], zip(y, history_y)))
        # history_y = y
        plt.bar(x,y,color = [color(i) for i in y])
        for x,y in zip(x,y):
            text_local_y = y+maggin if y>0 else y-maggin*8
            plt.text(x,text_local_y,y,fontsize=7,ha='center')
        plt.draw()
        
        plt.pause(3)
def plan_b():
    #无交互无循环
    plt.xticks(rotation=60)
    plt.title(sid[:-1]+today.join('()'), fontproperties=font)

    price_vol_table = get_data()

    x = [i for i in price_vol_table.keys()]
    x.sort()
    y = [sum(price_vol_table[i]) for i in x]

    plt.bar(x,y,color = [color(i) for i in y])
    plt.show()
# plan_a()
if __name__ == '__main__':
    if conf['ios']==1:
        plan_a()
    else:
        plan_b()
