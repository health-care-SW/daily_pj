import streamlit as st
import pandas as pd
# import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from keras.models import load_model

model = load_model('drug_model2.h5')



st.markdown('''
# Drug Classification Dashboard

Data source: [AI hub](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=576)
''')

df = pd.read_csv("drug\\drug.csv", encoding='utf-8')
df_name = df['dl_name']


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

def run_model(img_file):
  result = model.predict(np.array([img_file]))
  return result

def prediction(result):
  result = result[0]
  highest_likely = max(result)
  hl_idx = list(result).index(highest_likely)
  drug_name = df_name.iloc[hl_idx]
  likeliness = highest_likely * 100
  return drug_name, likeliness

uploaded_file = st.file_uploader("Upload your photo of pill/tablet", type=['png','jpg'])

uploaded = st.button("upload")

if uploaded:
  test_img = load_img(uploaded_file)
  st.image(test_img, width=200)
  test_img = preprocess_img(uploaded_file)
  result = run_model(test_img)
  drug_name, likeliness = prediction(result)
  st.write(f"Your pill is {drug_name} by {likeliness}%.")

