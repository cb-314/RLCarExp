import numpy as np
import matplotlib.pyplot as plt
import cPickle
import sys
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

def cv(model, x, y):
  errors = []
  kf = KFold(n_splits=10, shuffle=True)
  for train_index, test_index in kf.split(log):
    x_train, x_test = x[train_index], log[test_index]
    y_train, y_test = y[train_index], rewards[test_index]

    x_scaler = StandardScaler()
    y_scaler = StandardScaler()
   
    x_scaler.fit(x_train)
    y_scaler.fit(y_train)

    xx_train = x_scaler.transform(x_train)
    xx_test = x_scaler.transform(x_test)
    yy_train = y_scaler.transform(y_train)
    yy_test = y_scaler.transform(y_test)

    model.fit(xx_train, yy_train)

    yy_predicted = model.predict(xx_test)

    error = mean_squared_error(yy_test, yy_predicted)
    errors.append(error)
  return errors

if __name__ == "__main__":
  file_name = "log.pick"
  if ".pick" in sys.argv[1]:
    file_name = sys.argv[1]
  data = {}
  with open(file_name, "rb") as in_file:
    data = cPickle.load(in_file)
  log = np.array(data["log"])
  rewards = np.array(data["rewards"])
  rewards = rewards.reshape(-1, 1)

  errors = cv(KNeighborsRegressor(), log, rewards)

  print errors, np.mean(errors), np.std(errors)
