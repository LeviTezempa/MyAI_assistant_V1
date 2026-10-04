from groq import Groq


class LocalAssistant:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def run(self, prompt):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("The assistant returned an empty response.")
        return content
