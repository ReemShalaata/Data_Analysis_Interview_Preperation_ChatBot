import ast 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
from openai import OpenAI
import pandas as pd

client=OpenAI()
def train_model_to_generate_data(dataset):
    openai_api_key  = os.getenv('OPENAI_API_KEY')
    dataset = pd.read_excel('data_analysis_interview__qa.xlsx')  # Assuming it's an Excel file
    # Create a new question prompt
    new_question_prompt = (
        "As a data analysis interviewer, generate a data analysis interview question and provide its answer. "
        "The answer should be at lest 30 words"
        "The output should explicitly include the interviewer's question and the corresponding answer as a dictionary. "
        "The dictionary should also include the difficulty of the question ['Technical', 'Behavioral']. "
        "The dictionary should also include the category of the question ['Easy', 'Medium', 'Hard']. "
        "The dictionary must have only four keys ['Question', 'Answer', 'Category', 'Difficulty'] with the following pattern: "
        "{'Question': generated question, 'Answer': generated answer, 'Category': question's category, 'Difficulty': question's difficulty}.\n"
    )

    prompt_examples = ""

    # Loop through the dataset
    for index, row in dataset.iterrows():
        question = row['Question']
        answer = row['Answer']
        category = row['Category']
        difficulty = row['Difficulty']
        prompt_examples += (f"Question: {question}\nAnswer: {answer}\nCategory: {category}\nDifficulty: {difficulty}\n\n")

    # Append the new question prompt
    prompt_examples += new_question_prompt

    # Send the prompt to the GPT-3.5 model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[{'role': 'user', 'content': prompt_examples}],
        max_tokens=150
    )

    # Extract and print the response content
    response_text = response.choices[0].message.content
    # Convert the string representation of a dictionary to an actual dictionary
    response_dict = ast.literal_eval(response_text)



    generated_question=response_dict['Question']
    expected_answer=response_dict['Answer']
    return generated_question, expected_answer




def get_feedback(generated_question, user_answer, expected_answer):
    prompt = (f"Question: {generated_question}\n"
              f"Expected Answer: {expected_answer}\n"
              f"User's Answer: {user_answer}\n\n"
              "Provide detailed feedback on the user's answer for the generated quesion, comparing it with the expected answer and pointing out"
              "any inaccuracies, areas of improvement, or aspects that are well addressed."
              "The output feedback should not be more than 50 words")


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=150
    )

    return response.choices[0].message.content
