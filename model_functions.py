import httpx
import json
import os

api_key = open(f"{os.path.dirname(os.path.abspath(__file__))}/secrets/open_router_key.txt", "r").read().replace("\n", "")

def send_query(api_url, headers, payload):
    with httpx.Client() as client:
        response = client.post(api_url, headers=headers, data=payload, timeout=100)  # Usa await per attendere la risposta
        if response.status_code == 200:
            print(response.json())
            return response.json()["choices"][0]["message"]["content"]
        else:
            return {"error": f"HTTP {response.status_code}: {response}"}

def call_llm(account_key: str, model: str, input_text: str):
  api_url = "https://openrouter.ai/api/v1/chat/completions"
  headers = {"Authorization": "Bearer sk-or-v1-" + account_key}  # Open Router Key
  payload = json.dumps({"model": model, "temperature": 0, "messages": input_text, "transforms": []})
  response = send_query(api_url, headers, payload)
  return response

def format_text_for_LLM(text, context, documents):
    system_prompt = "".join([l for l in open(f"{os.path.dirname(os.path.abspath(__file__))}/prompts/system_prompt.md", "r").readlines()])
    user_prompt = "".join([l for l in open(f"{os.path.dirname(os.path.abspath(__file__))}/prompts/main_prompt.md", "r").readlines()])
    text = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt.replace("{question}", text).replace("{context}", context).replace("{document}", documents)},
    ]
    return text