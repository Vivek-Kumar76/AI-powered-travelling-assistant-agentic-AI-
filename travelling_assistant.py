from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from typing import TypedDict
import requests
import json
import os


load_dotenv()

parser = StrOutputParser()

model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash",
    temperature=1,
)

API_KEY = os.getenv("OPENTRIPMAP_API_KEY")
WEATHER_KEY  = os.getenv("WEATHER_API_KEY")


class travelState(TypedDict):
    user_input: str
    location: str
    budget: float
    climate : str
    visiting_places: list
    hotels:list
    history: list
    final_recommendation: str
    save_recommendation: str

def llm_input(state:travelState):
    prompt = PromptTemplate(
        template=""" Extract the city name and budget from the user input. Return ONLY valid JSON.Example:{{"location": "Manali", "budget": 15000}}
          User_input{user_input}""" ,
        input_variables=["user_input"])
    
    chain    = prompt | model | parser
    response = chain.invoke({"user_input": state["user_input"]})
    print(response)
    data = json.loads(response)

    return {
        "location" : data["location"],
        "budget" : data["budget"]
    }

def climatic_recommendation(state:travelState):
    city_text = state["location"]

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_text}&appid={WEATHER_KEY}&units=metric"
    weather_response = requests.get(url)

    data = weather_response.json()
    climate = []
    climate.append(data["main"])
    climate.append(data["weather"][0]["description"])

    return{"climate": climate}

    
def visiting_places(state:travelState):
    city = state["location"]

    geo = requests.get(
        "https://api.opentripmap.com/0.1/en/places/geoname",
        params={"name": city, "apikey": API_KEY}).json()

    print(geo)
    lat = geo["lat"]
    lon = geo["lon"]

    places = requests.get(
        "https://api.opentripmap.com/0.1/en/places/radius",
        params={
            "radius": 15000,
            "lat": lat,
            "lon": lon,
            "limit": 30,
            "format": "json",
            "apikey": API_KEY
        }
    ).json()

    return {"visiting_places":places}




def hotels(state:travelState):
    city= state["location"]
    budget = state["budget"]
    geo = requests.get("https://api.opentripmap.com/0.1/en/places/geoname",params={"name": city, "apikey": API_KEY}).json()

    lat = geo["lat"]
    lon = geo["lon"]

    hotels = requests.get("https://api.opentripmap.com/0.1/en/places/radius",
                          params={
                              "radius":5000,
                              "lat":lat,
                              "lon":lon,
                              "limit": 10,
                              "format":"json",
                              "apikey":API_KEY
                          })
    
    raw_hotels = hotels.json()
    print(raw_hotels)
    #print(type(raw_hotels))


    hotels_list =[]
    for h in raw_hotels:
        xid= h.get("xid")
        name= h.get("name","").strip()


        if not name or not xid:
            continue

        details = requests.get(f"https://api.opentripmap.com/0.1/en/places/xid/{xid}",
                               params={"apikey":API_KEY},
                               timeout=8).json()
        

        if budget <= 10000:
            price_range = "₹500-₹1200/night  (budget)"
        elif budget <= 25000:
            price_range = "₹1200-₹2500/night  (mid-range)"
        else:
            price_range = "₹2500-₹5000/night  (premium)"
        

        hotels_list.append({
            "name":name,
            "address":details.get("address",{}).get("road", "Address not available"),
            "price_range":price_range,
            "within_budget":True
        })


    return {"hotels": hotels_list}




#def history(state:travelState):




def final_recommendation(state:travelState):
    prompt= f"On the the basis of {state}, prepare a budget friendly travelling plan to visit {state['location']}"

    response= model.invoke(prompt)
    result= parser.invoke(response)
    
    return{"final_recommendation":result}


#def save_recommendation(state:travelState):
    
    

graph = StateGraph(travelState)
graph.add_node("llm_input",llm_input)
graph.add_node("climatic_recommendation", climatic_recommendation)
graph.add_node("visiting_places", visiting_places)
graph.add_node("hotels", hotels)

#graph.add_node("history", history)
graph.add_node("final_recommendation", final_recommendation)
#graph.add_node("save_recommendation", save_recommendation)


graph.add_edge(START, "llm_input")
graph.add_edge("llm_input", "climatic_recommendation")
graph.add_edge("llm_input","visiting_places")
graph.add_edge("llm_input","hotels")

graph.add_edge("climatic_recommendation","final_recommendation")
graph.add_edge("visiting_places","final_recommendation")
graph.add_edge("hotels","final_recommendation")
graph.add_edge("final_recommendation",END)

workflow=graph.compile()

user_input ="I want to visit Manali, Himachal Pradesh . My budget is 10000"

result = workflow.invoke({"user_input":user_input})

print(result["final_recommendation"])





