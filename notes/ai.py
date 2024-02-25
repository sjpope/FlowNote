import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_response(prompt):

    response = get_response(prompt)
    # Format and return the response
    return format_response(response)

def get_response(prompt):
    # Construct the system prompt
    system_prompt = f"""You are a helpful assistant for college students that are
    taking notes in class. You are to answer questions whatever school or class
    related question the user asks you. The question is: {prompt}.
    Do not go beyond one paragraph."""

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": system_prompt
        }],
        temperature=0.1,
        max_tokens=100
    )

    # Return API response
    return response

def format_response(response):
    answer = response.choices[0].message.content
    answer = answer.strip()
    return answer

print(generate_response("what is the mitochondria?"))
print("hi")