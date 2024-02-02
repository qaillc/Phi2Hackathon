# tools created using Phi2

import json
import os

import requests
from langchain.tools import tool

import spaces
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from threading import Thread
device = "cpu"
if torch.cuda.is_available():
    device = "cuda"
if torch.backends.mps.is_available():
    device = "mps"


tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    trust_remote_code=True,
).to(device)


#@spaces.GPU(enable_queue=True)
class Phi2SearchTools():
  @tool("Phi2 Normal")
  def phi2_search(text, temperature=.75, maxLen=2048):
    """
    Searches for content based on the provided query using the Gemini model.
    Handles DeadlineExceeded exceptions from the Google API.
    Args:
        query (str): The search query.
    Returns:
        str: The response text from the Gemini model or an error message.
    """
    inputs = tokenizer([text], return_tensors="pt").to(device)
    streamer = TextIteratorStreamer(tokenizer)
    generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=maxLen, temperature=temperature)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    t = ""
    toks = 0
    for out in streamer:
        t += out
        yield t


 