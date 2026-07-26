import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt 
import seaborn as sns
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor


def Evaluate_model(model , X , y):
    tscv = TimeSeriesSplit(n_splits=5)

    mae = []
    rmse = []
    r2 = []

    for train_idx , test_idx in tscv.split(X):
        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]

        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        model.fit(X_train , y_train)

        y_pred = model.predict(X_test)

        mae.append(mean_absolute_error(y_test,y_pred))
        rmse.append(np.sqrt(mean_squared_error(y_test, y_pred)))
        r2.append(r2_score(y_test,y_pred))

    return {
        'MAE' : np.mean(mae),
        'RMSE' : np.mean(rmse),
        'R2' : np.mean(r2)
    }
