# Streamlit UI
from random import choices
import streamlit as st 
# Keras load model
from keras.models import load_model
# Excell
import openpyxl as xl
import numpy as np
# Collections
import collections

model = load_model('./models/newest.model')

st.sidebar.title('Selections')

# load data for the selecets
## loading an existing workbook
wb = xl.load_workbook('Geology Input for Petar Updated April 11th.xlsx')
## Select the worksheet
categorical_items_sheet = wb['Sheet3']
categorical_items = list(categorical_items_sheet.iter_cols(min_row=1, max_row=24, min_col=1, max_col=6,  values_only=True))
categorical_items = [tuple(xi for xi in x if xi is not None) for x in categorical_items]

item_categories_sheet = wb['Sheet4']
terain_property_classes = tuple(item_categories_sheet.iter_rows(min_row=1, max_row=1, min_col=1, max_col=6,  values_only=True))[0]

props_sheet = wb['Sheet1']
terain_properties = list(props_sheet.iter_cols(min_row=1, max_col=1, min_col=1, values_only=True))[0]
terain_properties = list(map(lambda x: x.strip(), terain_properties))

categories_sheet = wb['Sheet5']
categories = list(categories_sheet.iter_cols(min_row=1, max_row=10, min_col=1, max_col=1,  values_only=True))[0]
category_texts = list(categories_sheet.iter_cols(min_row=1, max_row=10, min_col=2, max_col=2,  values_only=True))[0]


def changeHandler():
    l = {}
    choices = st.session_state.choices + st.session_state.mult_choices
    predictions = getPredictions(choices, terain_properties)[0]
    for inx, clas in enumerate(categories):
        l[clas] = predictions[inx]
    new_l = {k: v for k, v in sorted(l.items(), key=lambda item: item[1], reverse=True)}
    top_selection = list(new_l.keys())[0]
    selection_inx = categories.index(top_selection)
    string = category_texts[selection_inx].replace("[user's input strings]", str(choices)).replace("[probability of prediction]", str(new_l[top_selection]))
    st.write(string)
    st.write(new_l)

def getPredictions(predictionArr, properties):
    statements = np.zeros((1, len(properties)))
    for line in statements:
        for prop in predictionArr:
            line[properties.index(prop)] = 1.0
    return model.predict(statements)


st.session_state.choices = []

for inx, clas in enumerate(terain_property_classes):
    st.session_state.choices.append(st.sidebar.selectbox(clas, categorical_items[inx], key=clas))
    if inx >=2:
        st.session_state.mult_choices = st.sidebar.multiselect('Special features', np.concatenate(categorical_items[3:]))
        break

st.sidebar.button('Update', on_click=changeHandler)




