# Pakistan Tax & Freelancer FAQ Bot

A chatbot that answers common questions about tax and freelancing in Pakistan. You can ask in English or Roman Urdu, and it replies in the language you choose.

**Live app:** https://ai-tax-faq-chatbot.streamlit.app/

> General information only, not tax advice. Check current rates and deadlines on fbr.gov.pk.

## What it covers

- NTN (National Tax Number)
- Filing tax returns
- PSEB registration
- Receiving foreign payments as a freelancer

## How it works

1. Every FAQ has several ways of asking the same question, stored in `faqs_new.csv`.
2. The questions are cleaned: lowercased, split into words, stopwords removed (English and Roman Urdu), and words reduced to their base form.
3. A TF-IDF model built on character n-grams (3 to 5 characters) turns each question into numbers. Character n-grams help with spelling differences common in Roman Urdu.
4. When you ask something, the bot compares your question with all stored questions using cosine similarity and returns the answer of the closest match.
5. If the best match scores below 0.3, the bot replies "Bot is not sure about this!" instead of guessing.

## Accuracy

Tested on 181 questions (paraphrases, Roman Urdu, and out-of-scope questions): **about 97.8%** correct. A question the bot correctly refuses to answer counts as correct.

## Tech stack

Python, pandas, scikit-learn, NLTK, Streamlit

## Project structure

```
project/
  matcher.py              loads data, trains the model, finds answers
  user_interface.py       Streamlit web app
  faqs_new.csv            FAQ data (English and Urdu answers)
  faq_test_questions.csv  test questions used for the accuracy check
requirements.txt
```

## Run it on your computer

1. Install the requirements: `pip install -r requirements.txt`
2. From the repo root, run: `streamlit run project/user_interface.py`

## Author

Aafia Aftab, Software Engineering student

Built as part of the CodeAlpha internship.
