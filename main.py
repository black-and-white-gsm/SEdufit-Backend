import os
import requests
import logging
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate


logger = logging.getLogger()
api_key=os.environ.get('API_KEY')
model='llama-3.1-sonar-small-128k-online'
chat = ChatPerplexity(pplx_api_key=api_key, model=model)

def perplexity_chat(message):
    prompt = ChatPromptTemplate.from_messages([
        ('system', os.environ.get('SYSTEM')),
        ('human', message)
    ])

    try:
        chain = prompt | chat
    except Exception as e:
        logger.error(f'perplexity 오류: {e}')

    response = chain.invoke({'question': message})
    return response.content


def lambda_handler(event, context):
    text_input = event['text_input']
    callback_url = event['callback_url']

    result = perplexity_chat(text_input)
    try:
        requests.post(
            callback_url,
            json={
                'version': '2.0',
                'useCallback': False,
                'template': {'outputs': [{'simpleText': {'text': f'{result}'}}]}
            }
        )
    except Exception as e:
        logger.error(f'콜백 전송 실패: {e}')

    return True