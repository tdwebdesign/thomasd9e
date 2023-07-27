from django.http import HttpResponse
from django.shortcuts import render

import ast
import openai
import pandas as pd
import tiktoken
from scipy import spatial

EMBEDDING_MODEL = "text-embedding-ada-002"
DF = pd.read_csv("./website/ncaa2022.csv", names=['game_id', 'game_date', 'game_recap_title', 'text', 'embedding'])
DF['embedding'] = DF['embedding'].apply(ast.literal_eval)

def index(request):
    return render(request, 'index.html')

def process_question(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        response = generate_response(question, DF, print_message=False)
        return HttpResponse(response)

def cfb_assistant(request):
    return render(request, 'cfb_assistant.html')


def generate_response(query, df, model="gpt-3.5-turbo", token_budget=3000, print_message=False):
    """
    Generates a response for a given query using GPT and a dataframe of relevant texts and embeddings.
    """
    message = create_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You answer questions about the 2022 College Football seaon (last year)."},
            {"role": "user", "content": message},
        ],
        temperature=0
    )
    return response["choices"][0]["message"]["content"]

def create_message(query, df, model, token_budget):
    """
    Creates a message for GPT, with relevant source texts pulled from a dataframe.
    """
    strings = get_related_strings(query, df)
    introduction = 'Use the below articles on the 2022 College Football season (last year) to answer the subsequent question. If the answer cannot be found in the articles, write "I could not find an answer."'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'\n\nESPN game recap:\n"""\n{string}\n"""'
        if (count_tokens(message + next_article + question, model=model) > token_budget):
            break
        else:
            message += next_article
    return message + question

def count_tokens(text, model="gpt-3.5-turbo"):
    """
    Counts the number of tokens in a string.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def get_related_strings(question, df, top_n=10):
    """
    Returns a list of related strings based on question and dataframe.
    """
    query_embedding_response = openai.Embedding.create(model=EMBEDDING_MODEL, input=question)
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [(row["text"], calculate_relatedness(query_embedding, row["embedding"])) for i, row in df.iterrows()]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n]

def calculate_relatedness(x, y):
    """
    Calculates the relatedness between two embeddings.
    """
    return 1 - spatial.distance.cosine(x, y)
