import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('.env'))
api_key = os.environ.get('OPENROUTER_API_KEY')

if not api_key:
    print('[FAIL] ERROR: OPENROUTER_API_KEY not found in .env')
    exit(1)

print('[OK] API Key found')
print(f'     Length: {len(api_key)} chars')
print(f'     Format: {api_key[:10]}...')

# Now test the actual API
from openai import OpenAI

try:
    client = OpenAI(
        base_url='https://openrouter.ai/api/v1',
        api_key=api_key,
    )

    print('\n[TEST] Sending test request to OpenRouter with Gemma 4...')
    response = client.chat.completions.create(
        model='google/gemma-4-31b-it:free',
        messages=[
            {'role': 'user', 'content': 'Say hello in one word.'}
        ],
        max_tokens=10,
    )

    print('[SUCCESS] API WORKS!')
    print(f'          Response: "{response.choices[0].message.content}"')

except Exception as e:
    print(f'[ERROR] API ERROR: {type(e).__name__}')
    print(f'        Message: {str(e)}')
    exit(1)
