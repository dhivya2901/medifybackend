import os
import sqlite3
import requests
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# Load security keys from your .env file
load_dotenv()

# Setup Database (Agent 4)
def init_db():
    conn = sqlite3.connect("meetings.db")
    conn.execute("CREATE TABLE IF NOT EXISTS meetings (id INTEGER PRIMARY KEY, title TEXT, time TEXT)")
    conn.close()

init_db()

# Define Tools

@tool
def weather_agent(location: str):
    """Agent 1: Checks live weather. Use this for any location/weather queries."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        data = requests.get(url).json()
        return f"Weather in {location}: {data['main']['temp']}°C, {data['weather'][0]['description']}."
    except:
        return "Weather service is currently offline."

@tool
def resume_agent(query: str):
    """Agent 2: Document Intelligence. MANDATORY tool for questions about the user, 
    their name, education, or skills. Reads the local 'resume.pdf' file."""
    try:
        
        with open("resume.pdf", "rb") as f:
            reader = PdfReader(f, strict=False)
            text = ""
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content
            
            if len(text.strip()) < 5:
                return "The resume file exists but appears to be empty or unreadable."
                
            return f"The following information was found in the user's resume: {text[:3000]}"
            
    except FileNotFoundError:
        return "Error: I cannot find 'resume.pdf'. Please ensure the file is in C:\\backend."
    except Exception as e:
        return f"Technical Error reading PDF: {str(e)}. Try re-saving your resume as a standard PDF."

@tool
def google_search_agent(query: str):
    """Agent 3: Web Search. Use ONLY if the information is NOT in the resume."""
    return f"Simulated Web Search for '{query}': Information not found in local documents."

@tool
def database_agent(action: str, title: str = None, time: str = None):
    """Agent 4: Database Manager. Actions: 'add' (needs title/time) or 'view'."""
    conn = sqlite3.connect("meetings.db")
    cursor = conn.cursor()
    if action == "add":
        cursor.execute("INSERT INTO meetings (title, time) VALUES (?, ?)", (title, time))
        conn.commit()
        return f"Meeting '{title}' successfully saved to the database for {time}."
    else:
        cursor.execute("SELECT * FROM meetings")
        rows = cursor.fetchall()
        return f"Meetings in Database: {rows}"


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [weather_agent, resume_agent, google_search_agent, database_agent]
system_agent = create_react_agent(llm, tools)

# Execution Loop
if __name__ == "__main__":
    print("\n--- AI Multi-Agent System (v2.0) Online ---")
    print("Commands: 'exit' to quit. Ask about your resume, weather, or schedule.")
    
    while True:
        user_msg = input("\nYou: ")
        if user_msg.lower() in ["exit", "quit"]: break
        
        try:
            result = system_agent.invoke({"messages": [("user", user_msg)]})
            print(f"AI: {result['messages'][-1].content}")
        except Exception as e:
            print(f"AI: I encountered a logic error: {e}")