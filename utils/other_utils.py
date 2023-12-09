import ast 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
from openai import OpenAI
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd 
import random
from models.functions import train_model_to_generate_data
def check_database_exists():
    #check if the generated data exists before
    for file_name in ['Easy','Medium','Difficult']:
        if not os.path.exists(os.path.join('data',file_name)):
            train_model_to_generate_data(file_name)

# Callback functions
def increment_question_number():
    st.session_state.question_number += 1

def decrement_question_number():
    if st.session_state.question_number > 0:
        st.session_state.question_number -= 1

def sample_data(dataset,samples_indices):
    questions=[]
    categories=[]
    answers=[]
    for i in range(len(samples_indices)):
        questions.append(f"{dataset.iloc[samples_indices[i]]['Question']}")
        categories.append(f"{dataset.iloc[samples_indices[i]]['Category']}")
        answers.append(f"{dataset.iloc[samples_indices[i]]['Answer']}")
    return categories,questions,answers

def suggest_question(generated_dataset,category,difficulty_level):
    filtered_dataset = generated_dataset[(generated_dataset['Category']==category) & (generated_dataset['Difficulty'] == difficulty_level)] 
    single_data_point=filtered_dataset.sample().iloc[0]
    question,answer=single_data_point['Question'],single_data_point['Answer']
    return question,answer


def encode(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(text, convert_to_tensor=True,device='cuda')

def evaluate_answer(expected_answer,user_answer):
    # Encoding
    expected_answer_vec = encode(expected_answer).unsqueeze(0).cpu()
    user_answer_vec = encode(user_answer).unsqueeze(0).cpu()

    similarity = cosine_similarity(expected_answer_vec, user_answer_vec)

    print(f"Expected Answer: {user_answer}")
    print(f"User's Answer: {expected_answer}")
    print(f"Cosine similarity score: {similarity[0][0]}")
