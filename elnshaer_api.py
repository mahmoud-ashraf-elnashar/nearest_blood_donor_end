# -*- coding: utf-8 -*-
"""Elnshaer_api.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AZT5hMLM_zBgk0mZ37sHeUbnn7pfuR_a
"""
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import pickle


app = FastAPI()

# Load the KNN model from disk
with open('knn_model (2).sav', 'rb') as file:
    loadded_model = pickle.load(file)
# Load the Label Encoder from the saved file
with open('label_encoder.pkl', 'rb') as file:
    loadded_encoder = pickle.load(file)

from sklearn import preprocessing
  
# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()




class MyObject:
    def __init__(self, Longitude, Latitude, Country,Governorate,First_name,Last_name,Phone,Blood_type,Distance):
        self.Longitude = Longitude
        self.Latitude = Latitude
        self.Country = Country
        self.Governorate = Governorate
        self.First_name = First_name
        self.Last_name = Last_name
        self.Phone = Phone
        self.Blood_type = Blood_type
        self.Distance = Distance


# Define the prediction endpoint
@app.post("/prediction")
def predict(l1: float, l2: float,curr: int,BT:str,DT: int):
    # Make a prediction using the KNN model
    result=loadded_model.predict(np.array([l1,l2]).reshape(1, -1))
    result=loadded_encoder.inverse_transform([result])[0]
    print (result)
    df = pd.read_csv('geocode.csv')
    df_copy = df.copy()
    df_copy.drop([16357, 112805, 20868, 99371, 38292, 10915, 1069, 112757, 51756, 76645, 75828, 89323, 136098, 86223, 14701, 135695, 53006], axis=0, inplace=True)
    df_copy = df_copy.dropna()
    output_knnn = df_copy[df_copy['y'] == result]
    

    if DT ==2:
        if BT == "AP" or BT == "A-" :
            output_knn = output_knnn[~output_knnn['blood type'].isin(["O-", "B-", "B+", "O+"])]
        elif BT == "BP"or BT == "B-" :
            output_knn = output_knnn[~output_knnn['blood type'].isin(["O+", "A-", "A+", "O-"])]
        elif BT == "AB-" or BT == "ABP":
            output_knn = output_knnn[~output_knnn['blood type'].isin(["B+", "A+", "O+", "B-","O-","A-"])]
        else:
            output_knn = output_knnn

    else :
        if BT =="AP":
            output_knn = output_knnn[~output_knnn['blood type'].isin(["AB+", "B-", "B+", "AB-"])]
        elif BT == "BP":
            output_knn = output_knnn[~output_knnn['blood type'].isin(["AB+", "A-", "A+", "AB-"])]
        elif BT == "A-":
            output_knn = output_knnn[~output_knnn['blood type'].isin(["AB+", "B-", "A+", "AB-", "O+", "B+"])]
        elif BT == "B-":
            output_knn = output_knnn[~output_knnn['blood type'].isin(["AB+", "A-", "A+", "AB-", "O+", "B+"])]
        elif BT =="OP":
            output_knn = output_knnn[~output_knnn['blood type'].isin(["AB+", "B-", "A+", "AB-", "A-", "B+"])]
        elif BT == "O-":
            output_knn = output_knnn[~output_knnn['blood type'].isin(["AB+", "B-", "A+", "AB-", "A-", "B+", "O+"])]
        elif BT == "AB-":
            output_knn = output_knnn[~output_knnn['blood type'].isin(["AB+", "A+", "O+", "B+"])]
        else:
            output_knn = output_knnn
     

    
    output_knn['diff'] = ((abs(output_knn['x1'] - l1) + abs(output_knn['x2'] - l2))*60)*1.1515
     output_knn['diff'] = round(output_knn['diff'], 2)
    sorted_df = output_knn.sort_values('diff')
    the_nearst_list=[]
    for index in range(0,len(sorted_df['x1'])):
      nearest_index = sorted_df.index[index]
      nearest_value=list(sorted_df.iloc[index])
      obj = MyObject(nearest_value[0], nearest_value[1], nearest_value[2],nearest_value[3],nearest_value[4],nearest_value[5],nearest_value[6],nearest_value[7],nearest_value[8]+"km") 
      the_nearst_list.append(obj)
      

    return  the_nearst_list[curr]
      








