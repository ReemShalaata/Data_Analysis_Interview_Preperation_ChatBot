import streamlit as st
from utils.style_utils import format_text
from utils.style_utils import user_answer_input
import random 
import os
import pandas as pd
from utils.style_utils import changeradiotfontsize


# Content of the home page
def home_page():
    st.markdown(format_text(text="<br>Wlecome ",
                            alignment='center',size=40,color="#b93f5f",font_family="Papyrus", font_weight="Bold", emoji="😀<br><br>"),unsafe_allow_html=True)
    
    st.markdown(format_text(text="Practice Technical & Behavioural Interview Questions<br><br>",

                            alignment='center',size=30,color="#5fb93f",font_family="Courier New", font_weight="Bold", emoji="<br><br>"),unsafe_allow_html=True)
    
# Content of the difficulty page
def choose_difficulty_page():
    st.markdown(format_text(text="<br>Select Difficulty",

                            alignment='left',size=30,color="#5fb93f",font_family="Copperplate", font_weight="Bold", emoji="<br>"),unsafe_allow_html=True)
    
    difficulty = st.radio("", ["Easy", "Medium", "Hard"])
    st.markdown("<br><br><br><br>",unsafe_allow_html=True)
    
 
    st.session_state.difficulty = difficulty

# Content of the question pages
def question_page(dataset,question_num,samples_indices):

    # Using st.markdown with custom styling
    formatted_title = format_text(text=f"Question {question_num}",
                                    alignment='left', size=30, color="#5fb93f", 
                                    font_family="Copperplate", font_weight="Bold", emoji="<br><br>")
    st.markdown(formatted_title, unsafe_allow_html=True)

    questin=f"{dataset.iloc[samples_indices[question_num-1]]['Question']}"
     # Using st.markdown with custom styling
    formatted_question = format_text(text=f"{questin}",
                                    alignment='left', size=16, color="black", 
                                    font_family="Arial", font_weight="normal", emoji="<br>")
    st.markdown(formatted_question, unsafe_allow_html=True)
       

    user_answer=user_answer_input()

    return user_answer

# Content of the final page
def final_page():
    st.title("End of the Guide")
    st.write("You have completed the guide!")
