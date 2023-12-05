import ast 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import openai
from openai import OpenAI
import pandas as pd
client=OpenAI()
def train_model_to_generate_data(difficulty_level,num_generated_samples=2):
    openai_api_key  = os.getenv('OPENAI_API_KEY')
    openai.api_key = openai_api_key
    difficulty=difficulty_level.capitalize()
    dataset = pd.read_excel(os.path.join('data','training_dataset.xlsx'))
    # Create a new question prompt
    new_question_prompt = (
    f"As a data analysis interviewer, generate 10 unique data analysis interview questions, each covering a different topic. "
    "Provide answers for each question. Structure the output as follows:"

    "- A list containing 6 dictionaries. containing half andd half 'Technical' and 'Behaviioural' questions\n"
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

train_model_to_generate_data('EaSy')
#     for _ in range(num_batches):
#         prompt_examples = ""
#         for _, row in dataset.sample(min(len(dataset), questions_per_batch)).iterrows():
#             prompt_examples += f"Question: {row['Question']}\nAnswer: {row['Answer']}\nCategory: {row['Category']}\nDifficulty: {row['Difficulty']}\n\n"

#         new_question_prompt = (
#             "As a data analysis interviewer, generate data analysis interview questions and provide their answers. "
#             "The answers should be at least 30 words. "
#             "The output should explicitly include the interviewer's question and the corresponding answer as a dictionary. "
#             "The dictionary should also include the difficulty of the question ['Technical', 'Behavioral']. "
#             "The dictionary should also include the category of the question ['Easy', 'Medium', 'Hard']. "
#             "The dictionary must have only four keys ['Question', 'Answer', 'Category', 'Difficulty'].\n"
#         )

#         prompt_examples += new_question_prompt

#         response = openai.Completion.create(
#             model="gpt-3.5-turbo-16k",
#             prompt=prompt_examples,
#             max_tokens=150 * questions_per_batch  # Adjust based on your needs
#         )

#         response_text = response.choices[0].text.strip()
#         response_dicts = ast.literal_eval("[" + response_text + "]")  # Assuming the output is a list of dictionaries

#         for resp_dict in response_dicts:
#             all_questions = all_questions.append(resp_dict, ignore_index=True)

#         if len(all_questions) >= 50:
#             break

#     all_questions.to_excel("data_analysis_questions.xlsx")
#     return "Excel file with questions generated successfully."

# # Example usage
# batch_generate_questions('data_analysis_interview__qa.xlsx', 10, 5)

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
