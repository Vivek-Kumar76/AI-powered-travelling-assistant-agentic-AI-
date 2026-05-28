from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from typing import TypedDict
from pydantic import BaseModel


load_dotenv()

parser = StrOutputParser()

model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash",
    temperature=1,
)


class travelState(TypedDict):
    user_input: str
    budget: float
    climatic_recommendation: str
    visiting_places: list
    total_expenses: float
    history: list
    final_recommendation: str
    save_recommendation: str

def llm_input(state:travelState):
    prompt= state["user_input"]


def climatic_recommendation(state:travelState):
    


def visiting_places(state:travelState):


def total_expenses(state:travelState):


def history(state:travelState):



def final_recommendation(state:travelState):


def save_recommendation(state:travelState):
    
    dwxqx

graph = StateGraph()
graph.add_node("llm_input",llm_input)
graph.add_node("climatic_recommendation", climatic_recommendation)
graph.add_node("visiting_places", visiting_places)
graph.add_node("total_expenses", total_expenses)
graph.add_node("history", history)
graph.add_node("final_recommendation", final_recommendation)
graph.add_node("save_recommendation", save_recommendation)


graph.add_edge(START, "llm_input")
graph.add_edge("llm_input", "climatic_recommendation")



