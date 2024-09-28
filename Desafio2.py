# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ngEx85ev9yGvGBmrlqhrBd-eqhWAOCMw
"""

import tensorflow as tf

import pandas as pd

data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/imports-85.csv')

data_enum = pd.get_dummies(data).drop('normalized-losses', axis=1).fillna(0)
data_enum

dados = data_enum.drop(columns=['price'])
target = data_enum['price']

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(-1, 1))
dados = scaler.fit_transform(dados)
dados

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(dados, target, test_size=0.10, random_state=42)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation=tf.nn.relu),
    tf.keras.layers.Dense(32),
    tf.keras.layers.Dense(16),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.MeanSquaredError(),
              metrics=[tf.keras.metrics.R2Score])

model.fit(x_train, y_train, epochs=200)

#data_enum.isnull().sum()

model.evaluate(x_test, y_test)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

y_pred_train = model.predict(x_train)
y_pred_test = model.predict(x_test)

plt.subplot(1, 2, 1)
plt.scatter(y_train, y_pred_train, color='blue', label='Dados Reais (Treinamento) x previsão')
plt.scatter(y_test, y_pred_test, color='green', label='Dados Reais (Teste)')
plt.plot(y_train, y_train, color='red', linewidth=2, label='Linha de Regressão')
plt.legend()

plt.tight_layout()
plt.show()