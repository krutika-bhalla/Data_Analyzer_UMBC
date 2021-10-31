import os
import streamlit as st
import numpy as np
from PIL import Image
from multipage import MultiPage
from pages import data_upload, machine_learning, metadata, data_visualize, redundant
 
app = MultiPage()
 
display = Image.open('logo1.png')
display = np.array(display)
col1, col2 = st.beta_columns(2)
col1.image(display)
 
 
app.add_page("Upload Data", data_upload.app)
app.add_page("Changing Metadata", metadata.app)
app.add_page("Machine Learning Algorithm", machine_learning.app)
app.add_page("Analysis of Data", data_visualize.app)
app.add_page("Y-Parameter Optimization", redundant.app)
 
app.run()
 

