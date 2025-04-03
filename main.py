import os
import requests
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Configuration class
class Config:
    HOSTED_BASE_URL = os.getenv("HOSTED_BASE_URL")
    HOSTED_API_KEY = os.getenv("HOSTED_API_KEY")
    LOCAL_BASE_URL = os.getenv("LOCAL_BASE_URL")
    
    AVAILABLE_MODELS = [
        "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    ]

# Get API configuration
def get_api_config(model_name):
    if model_name.startswith("meta-llama/"):
        return Config.HOSTED_BASE_URL, Config.HOSTED_API_KEY
    else:
        raise ValueError(f"Invalid model name for hosted API: {model_name}")

# Handle API requests
def handle_hosted_request(client, model_name, messages, container):
    try:
        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True,
        )
        response_placeholder = container.empty()
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)
        return full_response
    except Exception as e:
        error_message = f"API Error: {str(e)}"
        container.error(error_message)
        return None

def stream_response(messages, container, model_name):
    base_url, api_key = get_api_config(model_name)
    client = OpenAI(api_key=api_key, base_url=base_url)
    return handle_hosted_request(client, model_name, messages, container)

# Generate translation prompt
def get_translation_prompt(text, source_lang, target_lang, cultural_context):
    return f"""
    Translate the following text from {source_lang} to {target_lang}, adapting it to a {cultural_context} context:

    "{text}"

    Translation:
    - [Your translated text here]
    """
