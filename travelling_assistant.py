from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from typing import TypedDict
from pydantic import BaseModel
import requests


load_dotenv()

parser = StrOutputParser()

model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash",
    temperature=1,
)


class travelState(TypedDict):
    user_input: str
    location: str
    budget: float
    climate : str
    visiting_places: list
    total_expenses: float
    history: list
    final_recommendation: str
    save_recommendation: str

def llm_input(state:travelState):
    prompt = PromptTemplate(
        template="On the basis of {user_input}. Extract the city name and budget in json format" ,
        input_variables=["user_input"])
    
    response = model.invoke(prompt)

    return {
        location : response["location"],
        budget : response["budget"]
    }

def climatic_recommendation(state:travelState):
    city_text = state["location"]

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_text}&appid={API_KEY}&units=metric"
    weather_response = requests.get(url)

    data = weather_response.json()
    climate = []
    climate.append(data["main"])
    climate.append(data["weather"][0]["description"])

    return{climate : climate}

    
def visiting_places(state:travelState):


def total_expenses(state:travelState):

def hotels(state:travelState):


def history(state:travelState):



def final_recommendation(state:travelState):


def save_recommendation(state:travelState):
    
    

graph = StateGraph(travelState)
graph.add_node("llm_input",llm_input)
graph.add_node("climatic_recommendation", climatic_recommendation)
graph.add_node("visiting_places", visiting_places)
graph.add_node("hotels", hotels)
graph.add_node("total_expenses", total_expenses)
graph.add_node("history", history)
graph.add_node("final_recommendation", final_recommendation)
graph.add_node("save_recommendation", save_recommendation)


graph.add_edge(START, "llm_input")
graph.add_edge("llm_input", "climatic_recommendation")
graph.add_edge("llm_input","visiting_places")



