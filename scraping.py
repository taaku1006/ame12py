import re
import time
import numpy as np
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


def search_data(url):
  html = urllib.request.urlopen(url)
  time.sleep(1)
  soup = BeautifulSoup(html, 'html.parser')
  element = soup.find_all('tr', attrs={'class':'mtx', 'style':'text-align:right;'})
  out = [list(map(lambda x: x.text, ele)) for ele in element]
  return out

class Get_amedas_data:
  def __init__(self,area_name,station_name):
    self.st_name = station_name
    self.a_name = area_name
    amedas_url_list = pd.read_csv('amedas_url_list.csv',encoding='utf_8_sig')
    df = amedas_url_list[(amedas_url_list['area']==self.a_name) & (amedas_url_list['station']==self.st_name)]
    amedas_url = df.iat[0,2]
    pattern=r'([+-]?[0-9]+\.?[0-9]*)'
    id_list=re.findall(pattern, amedas_url)
    self.pre_id = id_list[0]
    self.s_id = id_list[1]


  def set_date1(self, startmonth, endmonth):
    self.start = startmonth
    self.end = endmonth
    strdt = dt.strptime(self.start, '%Y%m')
    enddt = dt.strptime(self.end, '%Y%m')
    months_num = (enddt.year - strdt.year)*12 + enddt.month - strdt.month + 1
    # 開始月〜終了月までの月をリスト化
    self.datelist = map(lambda x, y=strdt: y + relativedelta(months=x), range(months_num))

  # 取得したい時間スケールを指定（type）
  def dl_data(self, type):
  # def dl_data(self):
    # dailyデータに関する空のデータフレーム
    data1  = pd.DataFrame(columns=['年','月','日','平均現地気圧','平均海面気圧','日降水量','最大1時間降水量','最大10分間降水量','平均気温','最高気温','最低気温','平均湿度','最小湿度','平均風速','最大風速','最大風向','最大瞬間風速','最大瞬間風向','日照時間','降雪','最深積雪','天気概況（昼）','天気概況（夜）'])
    data1_ = pd.DataFrame(columns=['年','月','日','日降水量','最大1時間降水量','最大10分間降水量','平均気温','最高気温','最低気温','平均風速','最大風速','最大風向','最大瞬間風速','最大瞬間風向','最多風向','日照時間','降雪','最深積雪'])

    for dt in self.datelist:
      d = dt.strftime("%Y%m%d")
      yyyy = d[0:4]
      mm = d[4:6]
      dd = d[6:8]

      # if type=='daily':
        # 気象台のある地点のblock_noは5桁の番号
      if len(self.s_id) == 5:
        pattern = 's1'
        url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/{type}_{pattern}.php?prec_no={self.pre_id}&block_no={self.s_id}&year={yyyy}&month={mm}&day={dd}&view=p1'
        out = search_data(url)
        df = (pd.DataFrame(out, columns=['日','平均現地気圧','平均海面気圧','日降水量','最大1時間降水量','最大10分間降水量','平均気温','最高気温','最低気温','平均湿度','最小湿度','平均風速','最大風速','最大風向','最大瞬間風速','最大瞬間風向','日照時間','降雪','最深積雪','天気概況（昼）','天気概況（夜）'])).assign(年=f'{yyyy}',月=f'{mm}')
        df = df.loc[:,['年','月','日','平均現地気圧','平均海面気圧','日降水量','最大1時間降水量','最大10分間降水量','平均気温','最高気温','最低気温','平均湿度','最小湿度','平均風速','最大風速','最大風向','最大瞬間風速','最大瞬間風向','日照時間','降雪','最深積雪','天気概況（昼）','天気概況（夜）']]
        data1 = pd.concat([data1, df])
        data1.to_csv(f'data.csv',index=None, encoding='utf_8_sig')
      else:
        pattern = 'a1'
        url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/{type}_{pattern}.php?prec_no={self.pre_id}&block_no={self.s_id}&year={yyyy}&month={mm}&day={dd}&view=p1'
        out = search_data(url)
        df = (pd.DataFrame(out, columns=['日','日降水量','最大1時間降水量','最大10分間降水量','平均気温','最高気温','最低気温','平均風速','最大風速','最大風向','最大瞬間風速','最大瞬間風向','最多風向','日照時間','降雪','最深積雪'])).assign(年=f'{yyyy}',月=f'{mm}')
        df = df.loc[:,['年','月','日','日降水量','最大1時間降水量','最大10分間降水量','平均気温','最高気温','最低気温','平均風速','最大風速','最大風向','最大瞬間風速','最大瞬間風向','最多風向','日照時間','降雪','最深積雪']]
        data1_ = pd.concat([data1_, df])
        data1_.to_csv(f'data.csv',index=None, encoding='utf_8_sig')



      print(f'{self.a_name}_{self.st_name}_{yyyy}-{mm}-{dd}_{type}')
    print(f'{self.a_name}_{self.st_name}における{self.start}〜{self.end}の{type}データをダウンロードしました。')


# if __name__ == '__main__':
  # a_name = input('ダウンロードしたい地域を入力してください：')
  # st_name = input('ダウンロードしたい地点を入力してください：')
  # amedas = Get_amedas_data(a_name,st_name)
  # type = input('daily：')
  # if type == 'daily':
    # start= input('取得したい開始月(yyyymm)を入力してください：')
    # end = input('取得したい終了月(yyyymm)を入力してください：')
    # amedas.set_date1(start,end)
  # else:
  #   start= input('取得したい開始日(yyyymmdd)を入力してください：')
  #   end = input('取得したい終了日(yyyymmdd)を入力してください：')
  #   amedas.set_date2(start,end)

  # amedas.dl_data(type)
