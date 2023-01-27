import streamlit as st
import pandas as pd
# import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from keras.models import load_model

model = load_model('bee_health_model.h5', compile=False)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model2 = load_model("bee_species_model.h5", compile=False)
model2.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

st.markdown('''
# Bees Health Classification Dashboard


Data source: [kaggle](https://www.kaggle.com/datasets/jenny18/honey-bee-annotated-images)
''')

bees = pd.read_csv('bee_data.csv',
                    index_col=False, parse_dates={'datetime':[1,2]},
                    dtype={"subspecies":'category',"health":'category',"caste":'category'})
bees = bees.replace({'location':'Athens, Georgia, USA'}, 'Athens, GA, USA')


# -------------------------
# show dataframe & graph
# -------------------------
with st.expander("See Details"):
  st.dataframe(bees)

  col = st.selectbox(label="Column",options=['location','subspecies','health','caste'])
  submitted = st.button("submit")
  if submitted:
      fig, ax = plt.subplots(figsize=(20,10))
      x = bees[col].value_counts().index
      y = bees[col].value_counts().values
      ax.bar(x,y)
      ax.set_xlabel=col
      ax.set_ylabel="Count"
      st.pyplot(fig)

# -------------------------
# upload photo & run test
# -------------------------
def load_img(img_file):
  img = Image.open(img_file)
  return img

def preprocess_img(img_file):
  img = Image.open(img_file)
  img = img.convert('RGB')
  img = img.resize((64,64))
  img = np.array(img)
  img = img/255.0
  return img

def run_health(img_file):
  result = model.predict(np.array([img_file]))
  return result

def run_species(img_file):
  result = model2.predict(np.array([img_file]))
  return result

def hprediction(idx):
  if idx == 0:
    return 'healthy'
  elif idx == 1:
    return 'few varrao, hive beetles'
  elif idx == 2:
    return 'Varroa, Small Hive Beetles'
  elif idx == 3:
    return 'ant problems'
  elif idx == 4:
    return 'hive being robbed'
  else:
    return 'missing queen'

def sprediction(idx):
  if idx == 0:
    return 'Italian honey bee'
  elif idx == 1:
    return 'Russian honey bee'
  elif idx == 2:
    return 'Carniolan honey bee'
  elif idx == 3:
    return 'Unspecified/Mixed local stock bee'
  elif idx == 4:
    return 'VSH Italian honey bee'
  else:
    return 'Western honey bee'

uploaded_file = st.file_uploader("Upload your own bee photo!", type=['png','jpg'])

uploaded = st.button("upload")

if uploaded:
  test_img = load_img(uploaded_file)
  st.image(test_img, width=200)
  test_img = preprocess_img(uploaded_file)
  result = run_health(test_img)
  result2 = run_species(test_img)
  health_status = hprediction(result[0].argmax())
  species = sprediction(result2[0].argmax())
  st.write("Your {}'s health status is: {}.".format(species.upper(), health_status.upper()))




