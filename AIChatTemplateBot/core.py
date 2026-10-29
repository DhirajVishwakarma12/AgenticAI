import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

template = ChatPromptTemplate.from_messages([
    ("system", """
    You are a movie summarizer AI.
    Summarize the given movie paragraph in simple English.
    Include the movie name, director, genre, main characters, and storyline.
    Do not invent information.
    """),
    ("human", "Summarize this movie paragraph:\n{paragraph}")
])

para = input("enter the movie: ")

final_prompt = template.invoke({"paragraph":para})

res = llm.invoke(final_prompt)
print(res.content)
