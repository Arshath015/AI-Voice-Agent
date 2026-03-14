from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_AOI_KEY"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Hello, who are you?"}
    ],
    temperature=0.7
)

print("\nGroq Response:\n")
print(response.choices[0].message.content)