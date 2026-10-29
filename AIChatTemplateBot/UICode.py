
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(page_title="Movie Summarizer", page_icon="🎬")

st.title("🎬 Movie Summarizer")
st.write("Enter a movie paragraph to generate a summary.")

template = ChatPromptTemplate.from_messages([
    ("system", """
    You are a movie summarizer AI.
    Summarize the given movie paragraph in simple English.
    Include the movie name, director, genre, main characters, and storyline.
    Do not invent information.
    """),
    ("human", "Summarize this movie paragraph:\n{paragraph}")
])

para = st.text_area("Enter the movie paragraph:")

if st.button("Summarize"):
    if not para.strip():
        st.warning("Please enter a movie paragraph.")
    else:
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            st.error("OPENROUTER_API_KEY is missing from your .env file.")
        else:
            llm = ChatOpenAI(
                model="openrouter/free",
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )

            try:
                with st.spinner("Summarizing movie..."):
                    final_prompt = template.invoke({"paragraph": para})
                    res = llm.invoke(final_prompt)

                st.subheader("Movie Summary")
                st.write(res.content)

            except Exception as e:
                st.error(f"Error: {e}")
