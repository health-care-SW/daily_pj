import streamlit as st
import pandas as pd
from streamlit_cropper import st_cropper
# import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from keras.models import load_model

model = load_model('bee_health_model.h5')
model2 = load_model("bee_species_model.h5")

st.markdown('''
# Bees Health Classification Dashboard


Data source: [kaggle](https://www.kaggle.com/datasets/jenny18/honey-bee-annotated-images)
''')

bees = pd.read_csv('archive\\bee_data.csv',
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
  img = img_file.convert('RGB')
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



def crop():
  uploaded_file = st.file_uploader("Upload your own bee photo!", type=['png','jpg'])

  with st.expander("crop your image"):

    if uploaded_file:
      img = load_img(uploaded_file)
      # Get a cropped image from the frontend
      cropped_img = st_cropper(img, realtime_update=True, box_color="#B5FF53",
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
  result = run_health(test_img)
  result2 = run_species(test_img)
  health_status = hprediction(result[0].argmax())
  species = sprediction(result2[0].argmax())
  st.write("Your {}'s health status is: {}.".format(species.upper(), health_status.upper()))

  




