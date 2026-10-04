import requests

def chat_with_llm(prompt, model="llama3.1:8b"):
    response = requests.post('http://localhost:11434/api/generate', json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']

print(chat_with_llm(""))