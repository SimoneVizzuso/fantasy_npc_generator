from langchain.llms import Ollama
from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# Access the environment variable
ollama_model = os.getenv('OLLAMA_MODEL')

ollama = Ollama(model=ollama_model)
