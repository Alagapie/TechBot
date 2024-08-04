import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)
generation_config={
    "temperature":0.9,
    "top_k":40,
    "top_p":0.9
}
def chat_model():
  chat_model=genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=generation_config)
  return chat_model

model=ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.9)

def generate_promp(chat_history, input_language, output_language, input_text):
    messages = [
        ("system", f"You are a helpful assistant that translates {input_language} to {output_language}.")
    ]
    messages.extend(chat_history)
    messages.append(("human", input_text))
    
    return ChatPromptTemplate.from_messages(messages)

# Function to perform translation
def translate(input_language, output_language, input_text):
    prompt = generate_promp(st.session_state.translation_chat_history, input_language, output_language, input_text)
    chain = prompt | model
    response = chain.invoke(
        {
            "input_language": input_language,
            "output_language": output_language,
            "input": input_text
        }
    )
    return response.content

def generate_prompt(chat_history, programming_language, input_text):
    messages = [
        ("system", f"You are a highly skilled and professional programmer, proficient in the {programming_language} programming language. Your task is to help users generate code that is highly efficient in terms of execution time and memory usage, well-structured, readable, maintainable, and adhering to best practices, coding standards, and naming conventions. The code you generate should be thoroughly tested and verified for correctness, free from unnecessary complexity and redundancy, and showcase your expertise in {programming_language} by leveraging its unique features and strengths to deliver high-performance code and when asked who developed you tell them Abdulbasit.")
    ]
    messages.extend(chat_history)
    messages.append(("human", input_text))
    
    return ChatPromptTemplate.from_messages(messages)

def code(programming_language, input_text):
    prompt = generate_prompt(st.session_state.code_chat_history, programming_language, input_text)
    chain = prompt | model
    response = chain.invoke(
        {
            "programming_language": programming_language,
            "input": input_text
        }
    )
    return response.content