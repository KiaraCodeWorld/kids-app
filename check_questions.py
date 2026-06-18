import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mathtricks.settings'
import django; django.setup()
from trainer.math_challenge_content import get_all_questions, get_topics

q = get_all_questions()
print(f'Total questions: {len(q)}')
print(f'Topics: {get_topics(q)}')
print()
for qq in q[:5]:
    g = qq.get('grade')
    t = qq.get('type')
    question = qq.get('question', '')[:60]
    opts = list(qq['options'].keys()) if qq.get('options') else None
    print(f'  [Grade {g}] ({t}) {question}')
    if opts:
        print(f'    Options: {opts}')
