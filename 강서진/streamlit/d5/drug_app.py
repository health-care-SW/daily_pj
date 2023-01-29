import streamlit as st
import pandas as pd
from streamlit_cropper import st_cropper
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from keras.models import load_model

model = load_model('drug_model.h5')



st.markdown('''
# Drug Classification Dashboard

Data source: [AI hub](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=576)
''')

df = pd.read_csv("drug\\drug2.csv", encoding='utf-8')
df_name = df['dl_name']


# -------------------------
# upload photo & run test
# -------------------------
def load_img(img_file):
  img = Image.open(img_file)
  return img


def preprocess_img(img_file):
  # img = Image.open(img_file)
  img = img_file.convert('RGB')
  img = img.resize((64,64))
  img = np.array(img)
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


def crop():
  uploaded_file = st.file_uploader("Upload your photo of pill/tablet", type=['png','jpg'])

  with st.expander("crop your image"):

    if uploaded_file:
      img = load_img(uploaded_file)
      # Get a cropped image from the frontend
      cropped_img = st_cropper(img, realtime_update=True, box_color="#0000FF",
                              aspect_ratio=None)

      # Manipulate cropped image at will
      st.write("Preview")
      _ = cropped_img.thumbnail((150,150))
      st.image(cropped_img)

      return cropped_img
      
test_img = crop()

cropped = st.button("run")
if cropped:
  test_img = preprocess_img(test_img)
  result = run_model(test_img)
  drug_name, likeliness = prediction(result)
  st.write(f"Your pill is {drug_name}.")
