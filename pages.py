import streamlit as st
from utils.style_utils import format_text
from functions import user_answer
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
