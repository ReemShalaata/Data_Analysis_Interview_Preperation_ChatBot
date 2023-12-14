import streamlit as st
from utils.style_utils import format_text
from utils.style_utils import user_answer_input
import random 
import os
import pandas as pd
from utils.style_utils import changeradiotfontsize
from models.functions import provide_feedback


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
    return difficulty

# Content of the question pages
def question_page(question_num,categorty_list,questions_list,):

    question=f"{questions_list[question_num-1]}"
    question_category =f"{categorty_list[question_num-1]}"  


    # Question Number ---Using st.markdown with custom styling  
    formatted_title = format_text(text=f"Question {question_num}",
                                    alignment='left', size=30, color="#5fb93f", 
                                    font_family="Copperplate", font_weight="Bold", emoji="<br>")
    st.markdown(formatted_title, unsafe_allow_html=True)


     # Question content ---Using st.markdown with custom styling
    formatted_title = format_text(text=f"* {question_category}",
                                    alignment='left', size=16, color="red", 
                                    font_family="Copperplate", font_weight="Bold", emoji="<br><br>")
    st.markdown(formatted_title, unsafe_allow_html=True)

     # Question content ---Using st.markdown with custom styling
    formatted_question = format_text(text=f"{question}",
                                    alignment='left', size=16, color="black", 
                                    font_family="Arial", font_weight="normal", emoji="<br>")

    st.markdown(formatted_question, unsafe_allow_html=True)      

    user_answer=user_answer_input(st.session_state.question_number,st.session_state.max_question_reached)

    return user_answer

# Content of the final page
def final_page(questions_list,user_answers_list,expected_answers_list):
    # Title
    st.markdown(
        format_text(
            text="Quiz Results \n\n\n",
            alignment="center",
            size=50,
            color="#1E90FF",
            font_family="Copperplate",
            font_weight="Bold",
            emoji="",
        ),
        unsafe_allow_html=True,
    )

    # Summary Introduction
    st.markdown(
        format_text(
            text="Thank you for completing the quiz. Here is a summary of your performance ",
            alignment="center",
            size=16,
            color="black",
            font_family="Arial",
            font_weight="normal",
            emoji="<br><br><br>",
        ),
        unsafe_allow_html=True,
    )


    # Feedback
    feedback_list, stars_list = provide_feedback(
        questions_list, user_answers_list, expected_answers_list
    )

    for index, item in enumerate(questions_list):
        # Display Question
        formatted_question = format_text(
            text=f"Question {index+1}: {questions_list[index]}",
            alignment="left",
            size=16,
            color="black",
            font_family="Copperplate",
            font_weight="Bold",
            emoji="",
        )
        st.markdown(formatted_question, unsafe_allow_html=True)

        # Display User Answer
        formatted_user_answer = format_text(
            text=f"Your Answer: {user_answers_list[index]}",
            alignment="left",
            size=16,
            color="black",
            font_family="Copperplate",
            font_weight="Bold",
            emoji="<br>",
        )
        st.markdown(formatted_user_answer, unsafe_allow_html=True)

        # Display Stars Feedback

        formatted_stars_feedback = format_text(
            text=f"{stars_list[index]}  ",
            alignment="center",
            size=30,
            color="#FFBF00",
            font_family="Copperplate",
            font_weight="Bold",
            emoji="",
        )
        st.markdown(formatted_stars_feedback, unsafe_allow_html=True)

        # Display Words Feedback
        formatted_words_feedback = format_text(
            text=f"{feedback_list[index]} ",
            alignment="center",
            size=16,
            color="#b93f5f",
            font_family="Copperplate",
            font_weight="Bold",
            emoji="<br><br><br><br><br>",
        )
        st.markdown(formatted_words_feedback, unsafe_allow_html=True)