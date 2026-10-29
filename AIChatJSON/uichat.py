
import os
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.title("Movie Information Extractor")

llm = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

class Movie(BaseModel):
    name: str
    release_date: str
    cost: int
    rating: Optional[str] = None
    summary: List[str]

parser = PydanticOutputParser(pydantic_object=Movie)

template = ChatPromptTemplate.from_messages([
    (
        "system",
        "Extract movie information from the provided paragraph.\n"
        "{format_instructions}"
    ),
    ("human", "{paragraph}")
])

para = st.text_area("Enter the movie paragraph:")

if st.button("Extract Information"):
    if para.strip():
        try:
            final_prompt = template.invoke({
                "paragraph": para,
                "format_instructions": parser.get_format_instructions()
            })

            with st.spinner("Extracting information..."):
                res = llm.invoke(final_prompt)

            movie_data = parser.parse(res.content)

            st.subheader("Extracted Movie Information")
            st.code(movie_data.model_dump_json(indent=2), language="json")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a movie paragraph.")
