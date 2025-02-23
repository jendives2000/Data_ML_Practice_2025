import os
import sys

sys.path.append(os.path.abspath(".."))
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState

from api.prompts import P_SUMMARIZE

load_dotenv


class State(MessagesState):
    history: str


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


def call_model(state: State, conversation_summary: str) -> dict:
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["MODEL_ID"],
        temperature=os.environ["TEMPERATURE"],
    )
    # if a summary exists, it is added to the system message:
    history = state.get("history", "")
    if history:
        system_message = f"Summary of previous conversation: {history}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        system_message = SYSTEM_PROMPT.format(conversation=conversation_summary)
        messages = [SystemMessage(content=system_message)] + state["messages"]
    response = llm.invoke(messages)
    # returning a list, because this will get added to the existing list:
    return {"messages": [response]}


def summarize_hist(state: State) -> dict:
    llm_summarize = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["MODEL_ID"],
        temperature=os.environ["TEMPERATURE"],
    )

    history = state.get("history", "")
    if history:
        history_message = f"Summary of previous conversation: {history}"
    else:
        history_message = "No history for this conversation"
    message = state["message"] + [HumanMessage(content=history_message)]
    response = llm_summarize.invoke(message)
    delete_message = [RemoveMessage(id=m.id) for m in state["messages"][:2]]
    return {"history": response.content, "messages": delete_message}


def print_update(update: dict) -> None:
    for k, v in update.items():
        m.pretty_print()
    if "history" in v:
        print(v["history"])
