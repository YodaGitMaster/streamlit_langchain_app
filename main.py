
import streamlit as st
import requests
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

# Set page title
st.title("Basic Chat")

# API endpoint for sending user messages
os.environ['OPENAI_API_KEY'] = ''

# Create an empty list to store chat messages
chat_messages = []


st.title("🦜🔗 LangChain Describe your Symptoms and find which medicine caused it")
# Create a text input field for user input
user_input = st.text_input("Insert your prompt")

ret = requests.get(f"https://api.fda.gov/drug/event.json?api_key=YLWkK4uU1d5jees3kdGLBK7aJCQDlgeQlpY0phTk&search=patient.reaction.reactionmeddrapt:{user_input}&limit=1").json()


template = """Read the json file and find the most likely medicine to have caused the symptoms. reactionmeddrapt is the symptom, reactionmeddraversionpt is the probability of the adversion, medicinalproduct is the name of the product. ---- {json}"""

## template

prompt = PromptTemplate(
    input_variables=["json"],
    template=template,
)
prompt.format(json=ret)

llm = OpenAI(temperature=0.9)
json_ext_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
seq_chain = SimpleSequentialChain(chains=[json_ext_chain], verbose=True)
