import requests
from openai import OpenAI
from utilities.constants import (
    TOGETHERAI_API_CHAT_ENDPOINT,
    TOGETHER_AI_API_KEY,
    TOGETHER_AI_MODEL_NAME,
    TOGETHERAI_API_IMAGE_ENDPOINT,
)

print(TOGETHERAI_API_IMAGE_ENDPOINT)

def together_api_call(prompt, temperature=0.2, max_tokens=4000):
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
    }
    payload = {
        "model": TOGETHER_AI_MODEL_NAME,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "system",
                "content": "You are a J.LEAGUE and football specialist.",
            },
            {"role": "user", "content": prompt},
        ],
    }

    try:
        req = requests.post(TOGETHERAI_API_CHAT_ENDPOINT, headers=headers, json=payload)
        req.raise_for_status()
        res = req.json()
        return None, res["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as error:
        return error, None


def openai_api_call(messages, temperature=0.5):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o", messages=messages, temperature=temperature
    )
    return completion.choices[0].message.content


def generate_image_dalle(prompt):
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url


def generate_image_together(prompt, model_string):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
    }
    payload = {
        "model": model_string,
        "prompt": prompt,
        "steps": 20,
        "n": 1,
        "height": 1024,
        "width": 1024
    }

    try:
        req = requests.post(TOGETHERAI_API_IMAGE_ENDPOINT, headers=headers, json=payload)
        req.raise_for_status()
        res = req.json()
        return res["data"][0]["url"]
    except requests.exceptions.RequestException as error:
        print(f"Error generating image with Together AI: {error}")
        return None
