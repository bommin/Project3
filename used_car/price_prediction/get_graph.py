import pandas as pd
import numpy as np
import sqlite3
import math
import json
import mpld3
import os
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
from matplotlib import font_manager, rc

import warnings
warnings.filterwarnings(action='ignore')

# font_path = "C:/Windows/Fonts/나눔고딕/NanumGothic"
# font = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font)


def get_graph(simple, fuel, year):
    print(os.getcwd())
    # bs로 받아오는 부분

    con = sqlite3.connect('./car_info_final_0614.db')
    df = pd.read_sql('SELECT * FROM df_car_info_final', con)
    con.close()

    df['내용연수'] = (2022 - df['year'])

    for i in range(0, len(df['내용연수'])):
        if df['내용연수'][i] > 15:
            df['내용연수'][i] = 15

    models = df['simple_model'].unique()

    col = df.columns

    df_model_sal = pd.DataFrame(columns=col)
    for i in models:
        tmp_df = df[df['simple_model'] == i]
        tmp_df['연평균_감가상각비'] = (
            ((tmp_df['og_price'] - tmp_df['price']) / tmp_df['og_price']) * 100) / (tmp_df['내용연수'])
        tmp_df = tmp_df.replace([np.inf, -np.inf], np.nan)
        tmp_df = tmp_df.fillna(0)
        df_model_sal = df_model_sal.append(tmp_df)

    df_model_sal.set_index(np.arange(0, len(df['model'])), inplace=True)

    # 연료별

    df_petrol = df_model_sal[df_model_sal['fuel'] == '가솔린']
    df_diesel = df_model_sal[df_model_sal['fuel'] == '디젤']
    df_lpg = df_model_sal[df_model_sal['fuel'] == 'LPG']
    df_hev = df_model_sal[df_model_sal['fuel'] == "하이브리드"]

    # ================================================================= 휘발유 =========================================================

    df_sal_petrol = pd.DataFrame(columns=['model', '2021', '2020', '2019'])

    for i in df_petrol['simple_model'].unique():
        tmp_model = df_petrol[df_petrol['simple_model'] == i]

        globals()['list_' + str(i)] = []

        tmp_model_2021 = tmp_model[tmp_model['year'] == 2021]
        a = tmp_model_2021['연평균_감가상각비'].mean()

        tmp_model_2020 = tmp_model[tmp_model['year'] == 2020]
        b = tmp_model_2020['연평균_감가상각비'].mean() * 2

        tmp_model_2019 = tmp_model[tmp_model['year'] == 2019]
        c = tmp_model_2019['연평균_감가상각비'].mean() * 3

        tmp_models = [[i, a, b, c]]

        tmp_df_models = pd.DataFrame(
            tmp_models, columns=['model', '2021', '2020', '2019'])
        tmp_mean = df_petrol['연평균_감가상각비'].mean()
        tmp_df_models['2021'] = tmp_df_models['2021'].fillna(tmp_mean)
        tmp_df_models['2020'] = tmp_df_models['2020'].fillna(tmp_mean * 2)
        tmp_df_models['2019'] = tmp_df_models['2019'].fillna(tmp_mean * 3)

        # df_sal_petrol = df_sal_petrol.append(pd.Series(tmp_models, index = df_sal_petrol.columns), ignore_index = True)
        df_sal_petrol = pd.concat([df_sal_petrol, tmp_df_models], axis=0)

    # =================================================================== 디젤===============================================================

    df_sal_diesel = pd.DataFrame(columns=['model', '2021', '2020', '2019'])

    for i in df_diesel['simple_model'].unique():
        tmp_model = df_diesel[df_diesel['simple_model'] == i]

        globals()['list_' + str(i)] = []

        tmp_model_2021 = tmp_model[tmp_model['year'] == 2021]
        a = tmp_model_2021['연평균_감가상각비'].mean()

        tmp_model_2020 = tmp_model[tmp_model['year'] == 2020]
        b = tmp_model_2020['연평균_감가상각비'].mean() * 2

        tmp_model_2019 = tmp_model[tmp_model['year'] == 2019]
        c = tmp_model_2019['연평균_감가상각비'].mean() * 3

        tmp_models = [[i, a, b, c]]

        tmp_df_models = pd.DataFrame(
            tmp_models, columns=['model', '2021', '2020', '2019'])
        tmp_mean = df_diesel['연평균_감가상각비'].mean()
        tmp_df_models['2021'] = tmp_df_models['2021'].fillna(tmp_mean)
        tmp_df_models['2020'] = tmp_df_models['2020'].fillna(tmp_mean * 2)
        tmp_df_models['2019'] = tmp_df_models['2019'].fillna(tmp_mean * 3)

        # df_sal_petrol = df_sal_petrol.append(pd.Series(tmp_models, index = df_sal_petrol.columns), ignore_index = True)
        df_sal_diesel = pd.concat([df_sal_diesel, tmp_df_models], axis=0)

    # ============================================================= LPG ========================================================

    df_sal_lpg = pd.DataFrame(columns=['model', '2021', '2020', '2019'])

    for i in df_lpg['simple_model'].unique():
        tmp_model = df_lpg[df_lpg['simple_model'] == i]

        globals()['list_' + str(i)] = []

        tmp_model_2021 = tmp_model[tmp_model['year'] == 2021]
        a = tmp_model_2021['연평균_감가상각비'].mean()

        tmp_model_2020 = tmp_model[tmp_model['year'] == 2020]
        b = tmp_model_2020['연평균_감가상각비'].mean() * 2

        tmp_model_2019 = tmp_model[tmp_model['year'] == 2019]
        c = tmp_model_2019['연평균_감가상각비'].mean() * 3

        tmp_models = [[i, a, b, c]]

        tmp_df_models = pd.DataFrame(
            tmp_models, columns=['model', '2021', '2020', '2019'])
        tmp_mean = df_lpg['연평균_감가상각비'].mean()
        tmp_df_models['2021'] = tmp_df_models['2021'].fillna(tmp_mean)
        tmp_df_models['2020'] = tmp_df_models['2020'].fillna(tmp_mean * 2)
        tmp_df_models['2019'] = tmp_df_models['2019'].fillna(tmp_mean * 3)

        # df_sal_petrol = df_sal_petrol.append(pd.Series(tmp_models, index = df_sal_petrol.columns), ignore_index = True)
        df_sal_lpg = pd.concat([df_sal_lpg, tmp_df_models], axis=0)

    # ================================================== HEV========================================================

    df_sal_hev = pd.DataFrame(columns=['model', '2021', '2020', '2019'])

    for i in df_hev['simple_model'].unique():
        tmp_model = df_hev[df_hev['simple_model'] == i]

        globals()['list_' + str(i)] = []

        tmp_model_2021 = tmp_model[tmp_model['year'] == 2021]
        a = tmp_model_2021['연평균_감가상각비'].mean()

        tmp_model_2020 = tmp_model[tmp_model['year'] == 2020]
        b = tmp_model_2020['연평균_감가상각비'].mean() * 2

        tmp_model_2019 = tmp_model[tmp_model['year'] == 2019]
        c = tmp_model_2019['연평균_감가상각비'].mean() * 3

        tmp_models = [[i, a, b, c]]

        tmp_df_models = pd.DataFrame(
            tmp_models, columns=['model', '2021', '2020', '2019'])
        tmp_mean = df_hev['연평균_감가상각비'].mean()
        tmp_df_models['2021'] = tmp_df_models['2021'].fillna(tmp_mean)
        tmp_df_models['2020'] = tmp_df_models['2020'].fillna(tmp_mean * 2)
        tmp_df_models['2019'] = tmp_df_models['2019'].fillna(tmp_mean * 3)

        # df_sal_petrol = df_sal_petrol.append(pd.Series(tmp_models, index = df_sal_petrol.columns), ignore_index = True)
        df_sal_hev = pd.concat([df_sal_hev, tmp_df_models], axis=0)

    # ========================================================== 그래프==================================================================

    # input_model = str(input('모델을 입력하세요 : >>>') )
    # input_year = int(input('연식을 입력하세요 : >>>'))
    # input_fuel = str(input('원하는 연료의 숫자를 선택하세요 (가솔린, 디젤, ,LPG, 하이브리드) : >>>'))

    # input_model = '쏘렌토'
    # input_year = 2020
    # input_fuel = "디젤"

    input_model = str(simple)
    input_year = int(year)
    input_fuel = str(fuel)

    # if input_fuel == 0:
    #     str_fuel = '가솔린'
    # elif input_fuel == 1:
    #     str_fuel = '디젤'
    # elif input_fuel == 2:
    #     str_fuel = 'LPg'
    # else :
    #     str_fuel = '하이브리드'

    try:
        tmp_search_1 = df[df['simple_model'] == input_model]
        tmp_search_2 = tmp_search_1[tmp_search_1['year'] == input_year]
        tmp_search_3 = tmp_search_2[tmp_search_2['fuel'] == input_fuel]

        model_price_max = int(tmp_search_3['og_price'].max())
        model_price_min = int(tmp_search_3['og_price'].min())

        if input_fuel == '가솔린':
            df_rate = df_sal_petrol
        elif input_fuel == '디젤':
            df_rate = df_sal_diesel
        elif input_fuel == 'LPG':
            df_rate = df_sal_lpg
        else:
            df_rate = df_sal_hev

        year_price_rate = df_rate[df_rate['model'] == input_model]
        year_price_rate_1 = int(100 - year_price_rate['2021'][0])
        year_price_rate_2 = int(100 - year_price_rate['2020'][0])
        year_price_rate_3 = int(100 - year_price_rate['2019'][0])

        x = [2022, 2023, 2024, 2025]

        y_1 = [model_price_max,
               model_price_max * year_price_rate_1 / 100,
               model_price_max * year_price_rate_2 / 100,
               model_price_max * year_price_rate_3 / 100]

        y_2 = [model_price_min,
               model_price_min * year_price_rate_1 / 100,
               model_price_min * year_price_rate_2 / 100,
               model_price_min * year_price_rate_3 / 100]

        model_price_mean = (model_price_max + model_price_min) / 2

        y = [model_price_mean,
             model_price_mean * year_price_rate_1 / 100,
             model_price_mean * year_price_rate_2 / 100,
             model_price_mean * year_price_rate_3 / 100]

        mean_price_rate = year_price_rate.iloc[0][1:4].mean()

        f = plt.figure(figsize=(5, 3))
        plt.plot(x, y_1, color='blue', marker='o',
                 markerfacecolor='blue', markersize=6)
        plt.plot(x, y_2, color='dodgerblue', marker='o',
                 markerfacecolor='dodgerblue', markersize=6)
        # plt.axis([xmin, xmax, y_1min * 1.5, y_1max * 1.5])
        # plt.xlabel('차량 시세 예측')
        plt.ylabel(input_model)
        plt.legend(['Max_Price', 'Min_Price'])

        plt.fill_between(x[0:2], y_2[0:2], color='skyblue', alpha=0.5)
        plt.fill_between(x[1:3], y_2[1:3], color='steelblue', alpha=0.5)
        plt.fill_between(x[2:], y_2[2:], color='steelblue', alpha=0.5)
        plt.fill_between(x[0:], y_2[0:], y_1[0:], color='lightpink', alpha = 0.5)

        for i in range(len(x)):
            height = y_1[i]
            plt.text(x[i], height + 0.25, '%.0f' %
                     height, ha='center', va='bottom', size=12)
        for i in range(len(x)):
            height = y_2[i]
            plt.text(x[i], height + 0.25, '%.0f' %
                     height, ha='center', va='bottom', size=12)

        ax = plt.subplot()
        ax.set_xticks(x)
        # ax.set_yticks([ymax, ymin])

        print(f)

        print(
            f'{input_model} 차량의 {input_year} 년형 {input_fuel} 모델의 예상 최고가 : {model_price_max} 만원')
        print(
            f'{input_model} 차량의 {input_year} 년형 {input_fuel} 모델의 예상 최저가 : {model_price_min} 만원')
        print(f'{input_model} 차량의 {input_year} 년형 {input_fuel} 모델의 3년간 연도별 평균 감가율 : {mean_price_rate:.2f} %')
        print(1)
        tmpfile = BytesIO()
        print(2)
        plt.savefig(tmpfile, format='png')
        print(3)
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        print(4)
        html = '<html><head> </head> <body>' + '<img src=\'data:image/png;base64,{}\', height = "700px", width = "1300px">'.format(encoded) + '</body></html>'
        print(5)

        gg = open('./price_prediction/templates/graph.html', 'w')
        print(6)
        gg.write(html)
        print(7)
        gg.close()
        print(8)
        # ggg = mpld3.fig_to_html(f, figid = '3_year_graph.html')
        print(10)

    except:
        print("====================================================================================================================")
        print('====================================== 검색한 차량의 정보가 없습니다. ===============================================')
        print("====================================================================================================================")

    return
