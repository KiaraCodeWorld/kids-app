import os
import hashlib
from django.core.cache import cache
from openai import OpenAI

class LLMHelper:
    def __init__(self):
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def _get_cache_key(self, content_type, identifier):
        """Generate cache key for explanations"""
        key_string = f"{content_type}:{identifier}"
        return f"llm_explanation:{hashlib.md5(key_string.encode()).hexdigest()}"

    def explain_spelling_rule(self, word, rule_type):
        """Get explanation for spelling rule with caching"""
        cache_key = self._get_cache_key('spelling_rule', f"{word}_{rule_type}")
        cached = cache.get(cache_key)

        if cached:
            return cached

        prompt = f"""Explain the spelling of the word '{word}' using this exact format:

**Pronunciation:** How to say it (phonetic guide).
**Spelling Rule:** The key rule that applies (one sentence).
**Common Mistakes:** 2-3 errors people make, as a bullet list.
**Memory Trick:** One catchy way to remember the spelling.
**Similar Words:** word1, word2, word3

Be concise. No extra commentary."""

        try:
            response = self.client.chat.completions.create(
                model="google/gemma-4-31b-it:free",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
            )

            explanation = response.choices[0].message.content
            cache.set(cache_key, explanation, 60 * 60 * 24)  # Cache for 24 hours
            return explanation
        except Exception as e:
            return f"Explanation: {word} follows standard spelling rules. Please check a dictionary for details."

    def get_spelling_hint(self, word, hint_type='general'):
        """Get hint for spelling a word"""
        cache_key = self._get_cache_key('spelling_hint', f"{word}_{hint_type}")
        cached = cache.get(cache_key)

        if cached:
            return cached

        hints = {
            'pronunciation': f"Hint: Say the word slowly: {' - '.join(word)}",
            'etymology': f"This word comes from...",
            'general': f"Remember: {word[0].upper()} is the first letter"
        }

        if hint_type in hints:
            hint = hints[hint_type]
        else:
            prompt = f"Give a short, helpful hint for spelling the word '{word}'. Just one sentence."
            try:
                response = self.client.chat.completions.create(
                    model="google/gemma-4-31b-it:free",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                )
                hint = response.choices[0].message.content
            except:
                hint = f"Try spelling it syllable by syllable"

        cache.set(cache_key, hint, 60 * 60 * 24)
        return hint

    def get_explanation_safe(self, word, rule_type):
        """Get explanation with fallback for errors"""
        try:
            return self.explain_spelling_rule(word, rule_type)
        except Exception as e:
            return f"Spelling tip for '{word}': Break it into syllables and sound each one out slowly."

    def explain_word_for_tier(self, word, tier, context=''):
        """Age-adaptive explanation for Word Explorer Academy."""
        cache_key = self._get_cache_key('we_tier', f"{word}_{tier}")
        cached = cache.get(cache_key)
        if cached:
            return cached

        prompts = {
            '5-7': f"""You are a friendly teacher talking to a 5-7 year old.
Explain the word "{word}" in a super simple, fun way.
Use short sentences and words a kindergartner knows.

Format (use these exact emoji labels):
🌟 **What it means:** One simple sentence (imagine talking to a 6-year-old).
📖 **For example:** One fun example sentence with this word.
🎯 **Remember it by:** One silly or cute trick to remember it.

No big words. Be warm, fun, and encouraging!""",

            '8-10': f"""Explain the word "{word}" for a 9-10 year old student.
Where they see it: {context}

Format:
**Meaning:** Clear, practical definition in 1-2 sentences.
**Where you'll use it:** One real-life scenario (school, gaming, sports, social media).
**Example:** One strong example sentence.
**Memory Trick:** One catchy way to remember it.

Keep it friendly, relatable, and practical.""",

            '11-13': f"""Explain the word "{word}" for a smart 12-13 year old student.
Context where it appears: {context}

Format (plain markdown, no ### headers):
**Definition:** Precise, complete definition.
**Word Origin:** One sentence on etymology or root words.
**In the Real World:** How this word appears in news, debates, or real life.
**Examples:**
* Strong example sentence in one context.
* Second example in a different context.
**Synonyms:** word1, word2, word3

Be intelligent and treat them as capable thinkers.""",
        }

        prompt = prompts.get(tier, prompts['8-10'])
        try:
            response = self.client.chat.completions.create(
                model="google/gemma-4-31b-it:free",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            explanation = response.choices[0].message.content
            cache.set(cache_key, explanation, 60 * 60 * 24)
            return explanation
        except Exception:
            return f'"{word}" is a great word to learn! Try using it in a sentence today.'

    def _call_llm(self, prompt, max_tokens=400):
        """Raw LLM call — used by Daily Discovery news and AI-expand."""
        try:
            response = self.client.chat.completions.create(
                model="google/gemma-4-31b-it:free",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception:
            return ''

    def explain_discovery_item(self, title, category, body_excerpt):
        """Expand a Daily Discovery item with deeper AI context for curious kids."""
        cache_key = self._get_cache_key('dd_expand', f"{category}_{title}")
        cached = cache.get(cache_key)
        if cached:
            return cached

        cat_personas = {
            'space':    'an excited astronomer talking to a curious 12-year-old',
            'manners':  'a thoughtful life coach talking to a teenager',
            'funfact':  'an enthusiastic science teacher',
            'hack':     'a practical productivity coach',
            'game':     'a game designer and educator',
            'trending': 'a media-savvy guide for teens',
            'news':     'a kids journalist',
        }
        persona = cat_personas.get(category, 'an enthusiastic educator')

        prompt = (
            f"You are {persona}.\n"
            f"Topic: {title}\n"
            f"Context: {body_excerpt[:300]}\n\n"
            "Give 3-4 sentences that go DEEPER — add a surprising related fact, "
            "a real-world connection, or a question that sparks further thinking. "
            "Write in simple, engaging language for a curious 10-13 year old. "
            "No repeating what was already said above."
        )
        result = self._call_llm(prompt, max_tokens=250)
        if result:
            cache.set(cache_key, result, 60 * 60 * 24)
        return result or "Fascinating topic! Try searching for more about this — you will be amazed at what you find."

    def explain_math_question(self, question: str, topic: str, grade: int,
                              user_answer: str | None = None) -> str:
        """Grade-adaptive step-by-step math explanation."""
        cache_key = self._get_cache_key('math_explain', f"g{grade}_{question[:60]}")
        cached = cache.get(cache_key)
        if cached:
            return cached

        age_map = {3: '8-9', 4: '9-10', 5: '10-11', 6: '11-12', 7: '12-13'}
        age_desc = age_map.get(grade, '9-11')

        wrong_note = ''
        if user_answer:
            wrong_note = f'\nThe student answered: "{user_answer}". Acknowledge their attempt kindly, then explain the correct approach.'

        prompt = f"""You are a patient, encouraging math tutor for a Grade {grade} student (age {age_desc}).

Topic: {topic}
Question: {question}{wrong_note}

Explain how to solve this step by step. Use this format:
🧠 **Understanding the problem:** What is this question really asking? (1-2 sentences)
📝 **Step 1:** [first step with calculation]
📝 **Step 2:** [next step]
📝 **Step 3:** [continue as needed]
✅ **Answer:** [final answer, clearly stated]
💡 **Tip to remember:** One sentence memory trick for this type of problem.

Keep language simple and encouraging for a {age_desc}-year-old. Use relatable examples."""

        result = self._call_llm(prompt, max_tokens=500)
        if result:
            cache.set(cache_key, result, 60 * 60 * 24)
        return result or "Let's work through this step by step! Try breaking the problem into smaller parts."

    def get_math_hint(self, question: str, topic: str, grade: int) -> str:
        """Give a gentle hint without revealing the full answer."""
        cache_key = self._get_cache_key('math_hint', f"g{grade}_{question[:60]}")
        cached = cache.get(cache_key)
        if cached:
            return cached

        prompt = f"""Give a helpful hint (NOT the answer) for this Grade {grade} math question.
Topic: {topic}
Question: {question}

Write just 1-2 sentences. Point them in the right direction without giving it away.
Start with an encouraging phrase like "Think about..." or "Remember that..." or "Try..."."""

        result = self._call_llm(prompt, max_tokens=120)
        if result:
            cache.set(cache_key, result, 60 * 60 * 6)
        return result or f"Think about what you know about {topic}. What information does the question give you?"


# Global instance
_llm_helper = None

def get_llm_helper():
    global _llm_helper
    if _llm_helper is None:
        try:
            _llm_helper = LLMHelper()
        except ValueError:
            _llm_helper = None
    return _llm_helper
