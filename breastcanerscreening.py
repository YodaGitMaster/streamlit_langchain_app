
import streamlit as st
import requests
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

# Set page title
st.title("Basic Chat")

# API endpoint for sending user messages
os.environ['OPENAI_API_KEY'] = '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'

# Create an empty list to store chat messages
chat_messages = []


st.title("🦜🔗 LangChain Clinical trials Scanner")
# Create text input boxes for refining the search
icd10 = st.text_input("Insert a list of ICD diagnosis codes")
sex = st.text_input("Sex")
age = st.text_input("Age")
medical_description = st.text_input("Patient Medical Description eg: female breast cancer patients, who have completed 4-7 years of primary adjuvant endocrine therapy")
specific_conditions = st.text_input("Specific Conditions eg: HIV")
healthy_volunteer=  {"HealthyVolunteers":st.checkbox('yes'), "HealthyVolunteers":st.checkbox('no')}


howmany = 1
data = requests.get(f"https://clinicaltrials.gov/api/query/full_studies?expr=breast+cancer&min_rnk=1&max_rnk={howmany}&fmt=json").json()

t1 = "Read the json file, include only trials with status Recruiting, extract fields[name, BriefSummary, location,contact email] ---- {file}"
t2 = "check if the trial exclude base on the conditions listed:[specific_conditions],check if there is a max or min age:[age],check if it exclude by sex:[sex],check if include the following pathology:[medical_description],check if include the following icd-10 codes:[icd10],check if include the need of healthy volunteers: [healthy_volunteer],if there is a match for exclusion conditions, age, sex or/and healthy volunteer exclude the trials from the list. ---- {file}"
t3 = "Print name of the study, location, email address, status. One for each line. ---- {file}"
## template
json_ext = PromptTemplate(input_variables=["file"], template=t1)
json_ext.format(file=data)
search = PromptTemplate(input_variables=["file"], template=t2)

formatanswer = PromptTemplate(input_variables=["file"], template=t3)


# ## llms
llm = OpenAI(temperature=0.9)
json_ext_chain = LLMChain(llm=llm, prompt=json_ext, verbose=True)
search_chain = LLMChain(llm=llm, prompt=search, verbose=True)
formatter_chain = LLMChain(llm=llm, prompt=formatanswer, verbose=True)

seq_chain = SimpleSequentialChain(chains=[json_ext_chain,search_chain,formatter_chain], verbose=True)




# Check if the user has entered any input
if user_input:
    # Add user input to the chat messages list
    # Clear the input field after submitting
    chat_messages.append(("You", user_input))
    # Send user message to the API
    response = seq_chain.run(user_input)
    
    # Check if the API request was successful
    if response:
        # Get the API response message
        try:
            # Add API response to the chat messages list
            chat_messages.append(("Bot", response))
        except:
            chat_messages.append(("Bot", "The backend API seems offline, you might wanna try later"))
    else:
        st.text("Error: Failed to communicate with the API")

# Display the chat messages
for user, message in chat_messages:
    st.text(f"{user}: {message}")


### get the studies from the website
### add 2 vector matrix
### search for specific keywords base on prompt