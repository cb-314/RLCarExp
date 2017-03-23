import numpy as np
import matplotlib.pyplot as plt
import cPickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

if __name__ == "__main__":
  data = {}
  with open("log.pick", "rb") as in_file:
    data = cPickle.load(in_file)
  log = np.array(data["log"])
  rewards = np.array(data["rewards"])
  rewards = rewards.reshape(-1, 1)

  kf = KFold(n_splits=10, shuffle=True)
  for train_index, test_index in kf.split(log):
    x_train, x_test = log[train_index], log[test_index]
    y_train, y_test = rewards[train_index], rewards[test_index]

    x_scaler = StandardScaler()
    y_scaler = StandardScaler()
   
    x_scaler.fit(x_train)
    y_scaler.fit(y_train)

    xx_train = x_scaler.transform(x_train)
    xx_test = x_scaler.transform(x_test)
    yy_train = y_scaler.transform(y_train)
    yy_test = y_scaler.transform(y_test)

    model = KNeighborsRegressor()
    model.fit(xx_train, yy_train)

    yy_predicted = model.predict(xx_test)

    print mean_squared_error(yy_test, yy_predicted)
