import json
import joblib
 
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
 
from .utils import isNumerical
import os
 
def app():
   """This application helps in running machine learning models without having to write explicit code
   by the user. It runs some basic models and let's the user select the X and y variables.
   """
 
   if 'main_data.csv' not in os.listdir('data'):
       st.markdown("Please upload data through `Upload Data` page!")
   else:
       data = pd.read_csv('data/main_data.csv')
       params = {}
       col1, col2 = st.beta_columns(2)
       y_var = col1.radio("Select the variable to be predicted (y)", options=data.columns)
       X_var = col2.multiselect("Select the variables to be used for prediction (X)", options=data.columns)
 
       if len(X_var) == 0:
           st.error("You have to put in some X variable and it cannot be left empty.")
 
       if y_var in X_var:
           st.error("Warning! Y variable cannot be present in your X-variable.")
 
       pred_type = st.radio("Select the type of process you want to run.",
                           options=["Regression", "Classification"],
                           help="Write about reg and classification")
 
       params = {
               'X': X_var,
               'y': y_var,
               'pred_type': pred_type,
       }
 
       st.write(f"**Variable to be predicted:** {y_var}")
       st.write(f"**Variable to be used for prediction:** {X_var}")
 
       X = data[X_var]
       y = data[y_var]
       X = pd.get_dummies(X)
 
       if not isNumerical(y):
           le = LabelEncoder()
           y = le.fit_transform(y)
 
           st.write("The classes and the class allotted to them is the following:-")
           classes = list(le.classes_)
           for i in range(len(classes)):
               st.write(f"{classes[i]} --> {i}")
 
       st.markdown("#### Train Test Splitting")
       size = st.slider("Percentage of value division",
                           min_value=0.1,
                           max_value=0.9,
                           step = 0.1,
                           value=0.8,
                           help="This is the value which will be used to divide the data for training and testing. Default = 80%")
 
       X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=size, random_state=42)
       st.write("Number of training samples:", X_train.shape[0])
       st.write("Number of testing samples:", X_test.shape[0])
 
       with open('data/metadata/model_params.json', 'w') as json_file:
           json.dump(params, json_file)
 
       ''' RUNNING THE MACHINE LEARNING MODELS '''
       if pred_type == "Regression":
           st.write("Running Regression Models on Sample")
 
           model_r2 = []
           lr_model = LinearRegression()
           lr_model.fit(X_train, y_train)
           lr_r2 = lr_model.score(X_test, y_test)
           model_r2.append(['Linear Regression', lr_r2])
 
           dt_model = DecisionTreeRegressor()
           dt_model.fit(X_train, y_train)
           dt_r2 = dt_model.score(X_test, y_test)
           model_r2.append(['Decision Tree Regression', dt_r2])
 
           if dt_r2 > lr_r2:
               joblib.dump(dt_model, 'data/metadata/model_reg.sav')
           else:
               joblib.dump(lr_model, 'data/metadata/model_reg.sav')
           results = pd.DataFrame(model_r2, columns=['Models', 'R2 Score']).sort_values(by='R2 Score', ascending=False)
           st.dataframe(results)
      
       if pred_type == "Classification":
           st.write("Running Classfication Models on Sample")
 
           model_acc = []
           lc_model = LogisticRegression()
           lc_model.fit(X_train, y_train)
           lc_acc = lc_model.score(X_test, y_test)
           model_acc.append(['Linear Regression', lc_acc])
 
           dtc_model = DecisionTreeClassifier()
           dtc_model.fit(X_train, y_train)
           dtc_acc = dtc_model.score(X_test, y_test)
           model_acc.append(['Decision Tree Regression', dtc_acc])
           if dtc_acc > lc_acc:
 
               joblib.dump(dtc_model, 'data/metadata/model_classification.sav')
           else:
               joblib.dump(lc_model, 'data/metadata/model_classificaton.sav')
 
           results = pd.DataFrame(model_acc, columns=['Models', 'Accuracy']).sort_values(by='Accuracy', ascending=False)
           st.dataframe(results)

