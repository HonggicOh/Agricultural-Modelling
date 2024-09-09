import numpy as np
import keras.regularizers
import pandas as pd
from sklearn import preprocessing
import sklearn.model_selection
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# Load and process data
raw_data = pd.read_csv('data/Vic_v5.csv', delimiter=',')
areas = ['AUS']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
required_X_columns = []
required_y_columns = []
for month in months:
    required_X_columns.append(month + '_temp')
    required_X_columns.append(month + '_rain')
    required_X_columns.append(month + '_humidity')
    required_X_columns.append(month + '_wind')
    required_X_columns.append(month + '_uva')
    required_X_columns.append(month + '_uvb')
    required_X_columns.append(month + '_eva')
required_X_columns.append('Wheat_Area')
required_X_columns.append('Covid')
required_y_columns.append('Wheat_Production')
raw = raw_data[required_X_columns].applymap(lambda x: x.replace(' ', '') if isinstance(x, str) else x)
raw = raw.applymap(lambda x: x.replace(',', '') if isinstance(x, str) else x)
X = pd.DataFrame(raw, dtype=np.float)
y = pd.DataFrame(raw_data[required_y_columns].applymap(lambda x: x.replace(' ', '') if isinstance(x, str) else x),
                 dtype=np.float).sum(axis=1)
standardize_scaler = preprocessing.MinMaxScaler()
X = standardize_scaler.fit_transform(X)

# build model
model = tf.keras.models.Sequential([
    layers.Dense(32, kernel_initializer='random_normal', input_shape=(X.shape[1],),
                 kernel_regularizer=keras.regularizers.L2(0.001)),
    layers.BatchNormalization(),
    layers.Activation('relu'),
    layers.Dense(8, kernel_initializer='random_normal',kernel_regularizer=keras.regularizers.L2(0.001)),
    layers.Activation('relu'),
    layers.Dense(1),
    layers.Activation('relu')
])
check_points_path = 'checkpoints_wheat_yield/model.ckpt'


# Uncomment this block when retraining the model(do not do this without permission)
# cp_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath=check_points_path, save_weights_only=True,
#                                                             save_best_only=True)
# model.compile(optimizer='adam', loss='mse')
#
# history = model.fit(x=X, y=y.values, batch_size=5, epochs=1000, validation_split=0.05,
#                     callbacks=[cp_checkpoint_callback])

# Show the result
model.load_weights(check_points_path)
re = model.predict(X)
dif = (np.reshape(re, (32,)) - y.values) / y.values
m = np.mean(np.abs(dif))
print('Average margin of error: {m}'.format(m = m))
years = []
for i in range(32):
    years.append(1990 + i)
result = pd.DataFrame({'Year':years,'Prediction value': np.reshape(re, (32,)), 'Actual value': y.values, 'Margin of error(%)': np.abs(dif*100)})
print(result)

#  0.12865284302005192
