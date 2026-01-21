# Medify Backend - Multi-Agent AI System 🚀

This project is a sophisticated AI backend powered by **LangGraph** and **OpenAI**. It utilizes a multi-agent orchestration pattern where a central LLM decides which specialized tool to use based on user intent.

## 🤖 The 4-Agent Architecture
The system is composed of four distinct agents that handle specific logic:

1. **Document Agent (PDF RAG)**: 
   - Uses `PyPDF2` to read and parse `resume.pdf`. 
   - Extracts personal information (like your name, Dhivya) to provide context for subsequent tasks.

2. **Weather Agent (Real-time API)**: 
   - Connects to the **OpenWeatherMap API**.
   - Fetches current temperature and conditions (e.g., checking weather in Salem) to determine if conditions are "good" for scheduling.

3. **Database Agent (SQLite)**: 
   - Manages a persistent `meetings.db` file.
   - Handles SQL commands to log "Project Completion" meetings and other appointments.

4. **Web Search Agent (Reasoning Fallback)**: 
   - Acts as a fallback reasoning tool for information not found in the local PDF or via specific APIs.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Orchestration:** LangChain / LangGraph
* **LLM:** GPT-4o-mini
* **Storage:** SQLite3
* **Environment:** Virtual Environment (venv) with `.env` for secure API management.

## 📂 Project Structure
* `main.py`: The core logic and agent definitions.
* `resume.pdf`: The source data for the Document Agent.
* `meetings.db`: The persistent database for scheduled events.
* `requirements.txt`: List of dependencies (LangChain, OpenAI, etc.).
* `.gitignore`: Configured to protect sensitive `.env` keys.

## 🚀 How to Run
1. Clone the repo.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Create a `.env` file and add your API keys:
   ```text
   OPENAI_API_KEY=your_openai_key
   OPENWEATHER_API_KEY=your_weather_key
4. python main.py
