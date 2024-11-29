import os
import requests
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate


api_key=os.environ.get('API_KEY')
model='llama-3.1-sonar-small-128k-online'
chat = ChatPerplexity(pplx_api_key=api_key, model=model)


def perplexity_chat(message):
    prompt = ChatPromptTemplate.from_messages([
        ('system', os.environ.get('SYSTEM')),
        ('human', message)
    ])

    chain = prompt | chat
    response = chain.invoke({'question': message})
    return response.content


def lambda_handler(event, context):
    print(event)
    text_input = event['text_input']
    callback_url = event['callback_url']

    result = perplexity_chat(text_input)
    print(result)

    requests.post(
        callback_url,
        json={
            'version': '2.0',
            'useCallback': False,
            'template': {'outputs': [{'simpleText': {'text': f'{result}'}}]}
        }
    )
    return True