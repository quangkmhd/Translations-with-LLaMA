import requests
import json
from openai import OpenAI
from config.config import Config

def get_api_config(model_name):
    """
    Get API base URL and API key based on the model name.
    This version only supports hosted models.
    """
    if model_name.startswith("meta-llama/"):
        return Config.HOSTED_BASE_URL, Config.HOSTED_API_KEY
    else:
        raise ValueError(f"Invalid model name for hosted API: {model_name}")

def handle_hosted_request(client, model_name, messages, container):
    """
    Handles the hosted Llama model requests via OpenAI's API.
    """
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
    """
    This function handles the API request for the hosted model and streams the response.
    """
    base_url, api_key = get_api_config(model_name)

    # Use OpenAI client to send request for hosted models
    client = OpenAI(api_key=api_key, base_url=base_url)
    return handle_hosted_request(client, model_name, messages, container)
