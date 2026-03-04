# Monday.com Business Intelligence Agent

This project implements an AI agent capable of answering business intelligence questions using live data from monday.com boards.

## Features

- Natural language business questions
- Live monday.com API integration
- Robust data cleaning
- Business analytics engine
- LLM-powered query interpretation
- Action trace showing agent steps

## Example Questions

Show top deals  
What is the pipeline in mining sector?  
Which sector has the biggest pipeline?  
How many deals are in each stage?  
Show work order status

## Architecture

User Question
→ LLM Interpreter (Groq Llama 3.1)
→ Agent Tool Selection
→ monday.com API
→ Data Cleaning
→ Analytics
→ Response

## Tech Stack

Python  
Streamlit  
Groq LLM API  
Pandas  
Monday.com API

## Setup

1. Install dependencies

pip install -r requirements.txt

2. Add environment variable

GROQ_API_KEY=your_api_key

3. Run the app

streamlit run app.py
