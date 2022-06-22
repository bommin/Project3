import sqlite3
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings(action='ignore')

# keras 
from keras.models import Sequential, load_model
from keras.layers import Dense
from sklearn.model_selection import train_test_split

# sklearn
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

# 회귀 모델 
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.svm import SVR

import seaborn as sns
import matplotlib.pyplot as plt
import mpld3

# train_test_split 
from sklearn.model_selection import train_test_split

con = sqlite3.connect('./car_info_final_0614.db')
df = pd.read_sql("SELECT * FROM 'df_car_info_final';", con)
con.close()

## 칼럼 삭제. model, color, accident
df.drop('color', axis=1, inplace=True)
df.drop('accident', axis=1, inplace=True)
df.drop('model',axis=1, inplace=True)

###
y = df['price']
X = df.drop('price',axis=1)

oh_features = ['manufacturer','fuel','simple_model']
ct = make_column_transformer((OneHotEncoder(),oh_features))
ct.fit(X)

mm_features = ['year','km', 'cc','og_price']
scaler = make_column_transformer((MinMaxScaler(),mm_features))
scaler.fit(X)

# 레이블, minmax 인코딩 처리 함수 

def minmaxencode_features_x(dataDF):
    newfeatures = scaler.transform(dataDF)
    dataDF = pd.concat([dataDF.drop(mm_features, axis=1),pd.DataFrame(newfeatures)],axis=1)
    dataDF.columns = ['manufacturer','fuel','simple_model','year','km', 'cc','og_price']
    return dataDF[['manufacturer','year','km','fuel', 'cc','simple_model','og_price']]

def minmaxencode_features_y(Series):
    series_max = max(Series)
    series_min = min(Series)
    result = (Series - series_min) / (series_max - series_min)
    return result

def onehotencode_features(dataDF):
    newfeatures = ct.transform(dataDF).toarray()
    dataDF = pd.concat([pd.DataFrame(newfeatures),dataDF],axis=1)
    return dataDF

# X 데이터 min-max, one_hot 인코딩 
df1 = minmaxencode_features_x(X)
X = onehotencode_features(df1)

# train_test split 

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                   test_size=0.2)

# y 데이터 min-max인코딩 

global_min = min(y_train)
global_max = max(y_train)
y_train = minmaxencode_features_y(y_train)

# index reset 
X_train.reset_index(drop=True, inplace=True)
y_train.reset_index(inplace=True,drop=True)
X_test.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)

# 칼럼 제거 
selected_features = ['manufacturer','fuel','simple_model']
X_train.drop(selected_features,axis=1,inplace=True)
X_test.drop(selected_features,axis=1,inplace=True)

# RandomForestRegressor 모델 실행
randomforest_reg = RandomForestRegressor()
randomforest_reg.fit(X_train, y_train)
randomforest_pred = randomforest_reg.predict(X_test)

# 예측치 반환 
y_predict = randomforest_reg.predict(X_test)
decoded_y_predict= y_predict*(global_max-global_min)+global_min

def predict_response(manufacturer,fuel,simple, year,cc,km,og):
    input_value = pd.DataFrame({'manufacturer':manufacturer,'fuel':fuel,'simple_model':simple,'year':year,'km':km,'cc':cc,'og_price':og}, index =[0])
    input_value = minmaxencode_features_x(input_value)
    input_value = onehotencode_features(input_value)
    selected_features = ['manufacturer','fuel','simple_model']
    input_value.drop(selected_features,axis=1,inplace=True)
    result = randomforest_reg.predict(input_value)
    result = int(result * (global_max - global_min) + global_min)
    return result


def deeplearning_response(manufacturer,fuel,simple, year,cc,km,og):
    input_value = pd.DataFrame({'manufacturer':manufacturer,'fuel':fuel,'simple_model':simple,'year':year,'km':km,'cc':cc,'og_price':og}, index =[0])
    input_value = minmaxencode_features_x(input_value)
    input_value = onehotencode_features(input_value)
    selected_features = ['manufacturer','fuel','simple_model']
    input_value.drop(selected_features,axis=1,inplace=True)
    input_X = np.asarray(input_value,dtype='float32')
    model = load_model('used_car_model.h5')
    result = int(model.predict(input_X) * (global_max - global_min) + global_min)
    return result




