# tools created using gemini

import json
import os

import google.generativeai as genai
from google.api_core import exceptions

# Retrieve API Key from Environment Variable
GOOGLE_AI_STUDIO = os.environ.get('GOOGLE_API_KEY')

# Ensure the API key is available
if not GOOGLE_AI_STUDIO:
    raise ValueError("API key not found. Please set the GOOGLE_AI_STUDIO2 environment variable.")

import requests
from langchain.tools import tool

# Rest of your code remains the same
genai.configure(api_key=GOOGLE_AI_STUDIO)
model = genai.GenerativeModel('gemini-pro')

class GeminiSearchTools():
  @tool("Gemini search the internet")
  def gemini_search(query):
    """
    Searches for content based on the provided query using the Gemini model.
    Handles DeadlineExceeded exceptions from the Google API.
    Args:
        query (str): The search query.
    Returns:
        str: The response text from the Gemini model or an error message.
    """
    try:
        response = model.generate_content(query)
        return response.text
    except exceptions.DeadlineExceeded as e:
        # Handle the DeadlineExceeded exception here
        print("Error: Deadline Exceeded -", str(e))
        # You can return a custom message or take other appropriate actions
        return "Error: The request timed out. Please try again later."

        

  @tool("Gemini search news on the internet")
  def gemini_search_news(query):
    """
    Searches for content based on the provided query using the Gemini model.
    Handles DeadlineExceeded exceptions from the Google API.
    Args:
        query (str): The search query.
    Returns:
        str: The response text from the Gemini model or an error message.
    """
    try:
        response = model.generate_content(query)
        return response.text
    except exceptions.DeadlineExceeded as e:
        # Handle the DeadlineExceeded exception here
        print("Error: Deadline Exceeded -", str(e))
        # You can return a custom message or take other appropriate actions
        return "Error: The request timed out. Please try again later."