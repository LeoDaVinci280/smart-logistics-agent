"""
Basic OpenAI connection test.
"""

from openai import OpenAI

from src.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

response = client.chat.completions.create(
    model=settings.OPENAI_MODEL,
    messages=[
        {
            "role": "user",
            "content": "Say hello"
        }
    ]
)

print(response.choices[0].message.content)