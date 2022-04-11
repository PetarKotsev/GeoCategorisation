# Streamlit UI
import streamlit as st 
# Keras load model
from keras.models import load_model
# Excell
import openpyxl as xl
import numpy as np

st.sidebar.title('TEST')

# load data for the selecets
## loading an existing workbook
wb = xl.load_workbook('Geology Input for Petar Updated April 8th.xlsx')
## Select the worksheet
categorical_items_sheet = wb['Sheet3']
categorical_items = list(categorical_items_sheet.iter_cols(min_row=1, max_row=22, min_col=1, max_col=6,  values_only=True))
categorical_items = [tuple(xi for xi in x if xi is not None) for x in categorical_items]

item_categories_sheet = wb['Sheet4']
terain_property_classes = tuple(item_categories_sheet.iter_rows(min_row=1, max_row=1, min_col=1, max_col=6,  values_only=True))[0]

props_sheet = wb['Sheet1']
terain_properties = list(props_sheet.iter_cols(min_row=1, max_col=2, min_col=2, values_only=True))[0]
terain_properties = list(map(lambda x: x.strip(), terain_properties))

def sortByActivation():
    pass

def changeHandler():
    pass

choices = []
for inx, clas in enumerate(terain_property_classes):
    choices.append(st.sidebar.selectbox(clas, categorical_items[inx], key=clas))


model = load_model('./models/newest.model')

def getPredictions(predictionArr, properties):
    statements = np.zeros((len(predictionArr), len(properties)))
    for line in statements:
        for prop in predictionArr:
            line[properties.index(prop)] = 1.0
    return model.predict(statements)

lines = getPredictions(choices, terain_properties)


