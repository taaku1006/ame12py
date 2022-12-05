import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import time




def draw_graph(fileName):
    print("グラフの描画を開始します。")

    df = pd.read_csv(
        fileName,
    )

    df2 = pd.to_datetime({
        "year":df['年'],
        "month":df['月'],
        "day":df['日'],

    })

    dt=pd.DataFrame({
        '日付':df2,
    })
    d_f=df.drop(['年','月','日'],axis=1)

    df3 = pd.concat([dt, d_f],axis=1)

    n_temparacture=df3['平均気温'].values

    date=df3['日付'].values

    # グラフ
    matplotlib.use('agg')
    plt.plot(date, n_temparacture, color="red")

    plt.gcf().autofmt_xdate()

    # x軸ラベル名
    plt.xlabel("Date")
    # y軸ラベル名
    plt.ylabel("")

    # グリッド線
    plt.grid()

    # グラフ画像の保存
    plt.savefig("temp.png")

    # グラフの表示
    # plt.show()

    print("グラフの描画が完了しました。")
