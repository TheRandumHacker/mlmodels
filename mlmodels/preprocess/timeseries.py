"""

  Ensemble of preprocessor for time series



https://docs-time.giotto.ai/


https://pypi.org/project/tslearn/#documentation


https://pypi.org/project/skits/



Gluon TS



"""

from mlmodels.util import path_norm
import pandas as pd




import numpy as np
from sklearn.preprocessing import MinMaxScaler
from collections import OrderedDict

def glutonts_to_pandas(dataset_name_list):
    from gluonts.dataset.repository.datasets import get_dataset
    # datasets = ["m4_hourly", "m4_daily", "m4_weekly", "m4_monthly", "m4_quarterly", "m4_yearly", ]
    ds_dict = OrderedDict()
    for t in dataset_name_list :
      ds = get_dataset(t)

      ####  convert
      ds1 = ds.to_pandas()

      ds1 = 0
      ds_dict[t] = ds1

    return ds_dict





class Preprocess_nbeats:

    def __init__(self,backcast_length, forecast_length):
        self.backcast_length = backcast_length
        self.forecast_length = forecast_length
    def compute(self,df):
        df = df.values  # just keep np array here for simplicity.
        norm_constant = np.max(df)
        df = df / norm_constant
        
        x_train_batch, y = [], []
        for i in range(self.backcast_length, len(df) - self.forecast_length):
            x_train_batch.append(df[i - self.backcast_length:i])
            y.append(df[i:i + self.forecast_length])
    
        x_train_batch = np.array(x_train_batch)[..., 0]
        y = np.array(y)[..., 0]
        self.data = x_train_batch,y
        
    def get_data(self):
        return self.data
        
class SklearnMinMaxScaler:

    def __init__(self, **args):
        self.preprocessor = MinMaxScaler(**args)
    def compute(self,df):
        self.preprocessor.fit(df)
        self.data = self.preprocessor.transform(df)
        
    def get_data(self):
        return self.data



def pd_load(path) :
   return pd.read_csv(path_norm(path ))




def pd_clean(df,  pars={}) :
  df = df.fillna(0)
  return df

def pd_fillna(df,**args):
    return df.fillna(**args)


def pd_reshape(test, features, target, pred_len, m_feat) :
    x_test = test[features]
    x_test = x_test.values.reshape(-1, pred_len, m_feat)
    y_test = test[target]
    y_test = y_test.values.reshape(-1, pred_len, 1)        
    return x_test, y_test



def time_train_test_split(data_pars):
    """
       train_data_path
       test_data_path
       predict_only

    """
    d = data_pars
    pred_len = d["prediction_length"]
    features = d["col_Xinput"]
    target   = d["col_ytarget"]
    m_feat   = len(features)


    # when train and test both are provided
    if d["test_data_path"]:
        test   = pd_load(d["test_data_path"])
        test   = pd_clean(test)
        x_test, y_test = pd_reshape(test, features, target, pred_len, m_feat) 
        if d["predict_only"]:
            return x_test, y_test


        train   = pd_load( d["train_data_path"])
        train   = pd_clean(train)
        x_train, y_train = pd_reshape(train, features, target, pred_len, m_feat) 

        return x_train, y_train, x_test, y_test
    


    # for when only train is provided
    df      = pd_load(d["train_data_path"])
    train   = df.iloc[:-pred_len]
    train   = pd_clean(train)
    x_train, y_train = pd_reshape(train, features, target, pred_len, m_feat) 


    test   = df.iloc[-pred_len:]
    test   = pd_clean(test)
    x_test, y_test = pd_reshape(test, features, target, pred_len, m_feat) 
    if d["predict_only"]:
        return x_test, y_test

    return x_train, y_train, x_test, y_test


