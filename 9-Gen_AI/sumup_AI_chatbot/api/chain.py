import os
import sys

sys.path.append(os.path.abspath(".."))
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from api.prompts import P_SUMMARIZE

load_dotenv


def sumup(input_txt: str) -> str:
    prompt_template = P_SUMMARIZE
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["MODEL_ID"],
        temperature=0.17,
    )
    chain = prompt | llm | StrOutputParser()

    return chain.invoke(input_txt)
