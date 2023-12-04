import streamlit as st
import streamlit.components.v1 as components
import pandas as pd 
import random
from utils.other_utils import use

dataset = pd.read_excel('training_dataset.xlsx') 
num_samples=5
st.session_state.samples_indices = random.sample(range(dataset.shape[0]), num_samples)

def user_answer_input(question_num):
    user_answer= st.text_area(key=f"user_answer{question_num}")
    return user_answer

# Callback functions
def increment_question_number():
    st.session_state.question_number += 1

def decrement_question_number():
    if st.session_state.question_number > 0:
        st.session_state.question_number -= 1


# Custom CSS to set the full-page, two-tone background
def set_background(color):
    # Using the provided color
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Content of the home page
def home_page():
    st.markdown(format_text(text="<br>Wlecome ",
                            alignment='center',size=40,color="#b93f5f",font_family="Papyrus", font_weight="Bold", emoji="😀<br><br><br>"),unsafe_allow_html=True)
    
    st.markdown(format_text(text="Practice Technical & Behavioural Interview Questions<br><br><br>",

                            alignment='center',size=30,color="#5fb93f",font_family="Courier New", font_weight="Bold", emoji="<br><br>"),unsafe_allow_html=True)
    
# Content of the difficulty page
def choose_difficulty_page():
    st.title("Choose the Difficulty Level")
    difficulty = st.radio("Select Difficulty", ["Easy", "Medium", "Hard"])
    st.session_state.difficulty = difficulty

# Content of the question pages
def question_page(question_num):
    st.title(f"Question {question_num}:")
    st.write(f"{dataset.iloc[st.session_state.samples_indices[question_num-1]]['Question']}")
    user_answer=user_answer_input(question_num)

    return user_answer

# Content of the final page
def final_page():
    st.title("End of the Guide")
    st.write("You have completed the guide!")




# Initialize session state for question number
if 'question_number' not in st.session_state:
    st.session_state.question_number = -1
    
# Page rendering logic
if st.session_state.question_number == -1:
    set_background("black")  # Replace with your desired colors
    home_page()
elif st.session_state.question_number == 0:
    set_background("white")
    choose_difficulty_page()
elif 1 <= st.session_state.question_number <= 5:
    question_page(st.session_state.question_number)
else:
    final_page()

col1, col2, col3 = st.columns(3)
with col1:
    if 1 < st.session_state.question_number <= 5:
        st.button(label="Back", on_click=decrement_question_number, key="back")
with col2:
    if st.session_state.question_number == -1:
        st.button("Start Practicing", on_click=increment_question_number, key="start")
    elif st.session_state.question_number == 0:
        st.button("Confirm", on_click=increment_question_number, key="confirm")


with col3:
    if 1 <= st.session_state.question_number < 5:
        st.button("Next", on_click=increment_question_number, key="next")

    elif st.session_state.question_number == 5:        
        st.button("Submit", on_click=increment_question_number, key="submit",)

st.markdown(
    unsafe_allow_html=True,
)
ChangeWidgetFontStyle('Start Practicing','24px','Arial','bold','white')

ChangeWidgetFontStyle("Confirm",'24px','Arial','bold','white')
