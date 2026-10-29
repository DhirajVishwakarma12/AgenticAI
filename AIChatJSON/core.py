
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

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

para = input("Enter the movie paragraph: ")

final_prompt = template.invoke({
    "paragraph": para,
    "format_instructions": parser.get_format_instructions()
})

res = llm.invoke(final_prompt)

movie_data = parser.parse(res.content)

print("\nExtracted Movie Information:")
print(movie_data.model_dump_json(indent=2))
