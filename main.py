import streamlit as st
import streamlit.components.v1 as components
import pandas as pd 
import random
from models.functions import train_model_to_generate_data,provide_feedback
from utils.other_utils import increment_question_number,decrement_question_number,check_database_exists,sample_data
from utils.style_utils import set_background, changewidgetfontstyle
from pages import home_page,choose_difficulty_page,question_page,final_page
from static.styles import custom_css
import numpy as np
import os 

choosen_num_of_question=5
generated_data_length=10
# Function to load data with caching
@st.cache_data()
def load_data( choosen_num_of_question = choosen_num_of_question):
    # Sample random indices for questions
    samples_indices = random.sample(range(generated_data_length), choosen_num_of_question)
    return samples_indices

# Load the data and variables
samples_indices= load_data()
st.markdown(custom_css(),unsafe_allow_html=True)

# Initialize session state for question number
if 'question_number' not in st.session_state:
    st.session_state.question_number = -1
    st.session_state.user_answers_list=['']*choosen_num_of_question
    st.session_state.max_question_reached=0   

        
# Page rendering logic
if st.session_state.question_number == -1:
    set_background("##F5F5F5")  # Replace with your desired colors
    home_page()
elif st.session_state.question_number == 0:
    set_background("white")
    difficulty=choose_difficulty_page()
    # Get data for the sampled indices
    st.session_state.category_list, st.session_state.questions_list, st.session_state.expected_answers_list = sample_data(difficulty,samples_indices)

elif 1 <= st.session_state.question_number <= 5 :
        if st.session_state.max_question_reached<st.session_state.question_number:
            st.session_state.max_question_reached=st.session_state.question_number
        user_answer=question_page(st.session_state.question_number,st.session_state.category_list,st.session_state.questions_list)
        st.session_state.user_answers_list[st.session_state.question_number-1]=user_answer

else:
    final_page(st.session_state.questions_list,st.session_state.user_answers_list,st.session_state.expected_answers_list)

col1, col2, col3 = st.columns(3)
with col1:
    if 1 < st.session_state.question_number <= 5:
        st.button("Back", on_click=decrement_question_number, key="back")
        changewidgetfontstyle(wgt_txt="Back",font_size='20px', font_family='Arial', font_weight='normal', text_align='center')
    elif st.session_state.question_number == 0:
        st.button("Confirm", on_click=increment_question_number, key="confirm")
        changewidgetfontstyle(wgt_txt="Confirm",font_size='20px', font_family='Arial', font_weight='normal', text_align='center')

with col2:
    if st.session_state.question_number == -1:
        st.button("Start", on_click=increment_question_number, key="start")
        changewidgetfontstyle(wgt_txt="Start",font_size='28px', font_family='Arial', font_weight='normal', text_align='center')

with col3:
    if 1 <= st.session_state.question_number < 5:
        st.button("Next", on_click=increment_question_number, key="next")
        changewidgetfontstyle(wgt_txt="Next",font_size='20px', font_family='Arial', font_weight='normal', text_align='center')



    elif st.session_state.question_number == 5:        
        st.button("Submit 👍", on_click=increment_question_number, key="submit",)
        changewidgetfontstyle(wgt_txt="Submit 👍",font_size='20px', font_family='Arial', font_weight='bold', text_align='center')
