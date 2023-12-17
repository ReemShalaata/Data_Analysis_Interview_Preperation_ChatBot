import ast 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import openai
from openai import OpenAI
import pandas as pd
client=OpenAI()
def train_model_to_generate_data(difficulty_level,num_generated_samples=10):
    openai_api_key  = os.getenv('OPENAI_API_KEY')
    openai.api_key = openai_api_key
    difficulty=difficulty_level.capitalize()
    dataset = pd.read_excel(os.path.join('data','training_dataset.xlsx'))
    # Create a new question prompt
    new_question_prompt =(
    f"As a data analysis interviewer, generate f'{difficulty}' level data analysis interview questions, each covering a different topic. "
    "Provide answers for each question. Structure the output as follows:"

    "- A list containing 6 dictionaries. containing half andd half 'Technical' and 'Behavioural' questions\n"
    f"- The output should be a list containing a total of {num_generated_samples} dictionaries.\n"
    "The dictionaries are evenly divided between 'Technical' and 'Behavioral' questions.ie the number of technichal and behavioural questions is the same\n"
    "- Each dictionary should have exactly three keys: 'Question', 'Answer', 'Category'.\n"
    "- 'Question' key: The question text, not exceeding 20 words. 'Question' should be unique and covering a different topic in each dictionary.\n"
    "- 'Answer' key: A detailed answer, ranging from 50 to 200 words, simple and clear.\n"
    "- 'Category' key: Specify whether the question is 'Technical' or 'Behavioral'.\n"
    "- For 'Behavioral' questions:\n"
    "1. The 'Answer' should be divided into two distinct sections."
    " 2. The first section of the 'Answer' should be structured generically, outlining the expected response approach." 
    "It should explain the specific traits, skills, and keywords that the interviewer is looking for, based on the nature of the 'Question'."
    "This section aims to guide candidates on how to effectively structure their answers in alignment with the interviewer's expectations."
    " 3. The second section of the 'Answer' should provide real-world scenarios and practical examples that directly relate to the 'Question'."
    "This part should illustrate how the candidate might realistically encounter and handle situations relevant to the question,"
    "showcasing their application of skills"
    )

    prompt_examples = ""

    # Loop through the dataset
    for index, row in dataset.iterrows():
        if ( row['Difficulty'] == difficulty):
            question = row['Question']
            answer = row['Answer']
            category = row['Category']
            prompt_examples += (f"Question: {question}\nAnswer: {answer}\nCategory: {category}\nDifficulty: {difficulty}\n\n")

    # Append the new question prompt
    prompt_examples += new_question_prompt

    # Send the prompt to the GPT-3.5 model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[{'role': 'user', 'content': prompt_examples}],
    )

    # Extract and print the response content
    response_text = response.choices[0].message.content
    # Convert the string representation of a dictionary to an actual dictionary
    response_list = ast.literal_eval(response_text)
    generated_dataset=pd.DataFrame(response_list)
    generated_dataset.to_excel(os.path.join('data',f'{difficulty}_level_generated_dataset.xlsx'), index=False)
    return



def encode(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(text, convert_to_tensor=True,device='cpu')

def provide_feedback(questions_list,user_answers_list,expected_answers_list):
    feedback_list=[]
    stars_list=[]
    feedback=""
    for index,item in enumerate(questions_list):
        # Encoding
        expected_answer_vec = encode(expected_answers_list[index]).unsqueeze(0).cpu()
        user_answer_vec = encode(user_answers_list[index]).unsqueeze(0).cpu()
        similarity = abs(cosine_similarity(expected_answer_vec, user_answer_vec)[0][0])
        if similarity>0.7:
            feedback="Good job!"
        else:
            feedback=f"Your answer is a bit brief. It can be improved by providing more details\n Check the hint {expected_answers_list[index]}"
        feedback_list.append(feedback)
        stars_list.append(rating_to_stars(similarity))

    return feedback_list,stars_list
            

def rating_to_stars(rating):
    max_stars = 5  # Maximum number of stars in the rating
    filled_stars = int(round(rating*max_stars))  # Round the rating to the nearest whole number
    empty_stars = max_stars - filled_stars

    # Create a string representation of the stars
    stars = '★' * filled_stars + '☆' * empty_stars
    print(stars)

    return stars