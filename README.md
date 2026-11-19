# Pakistan Tax & Freelancer FAQ Bot

A bilingual (English and Roman Urdu) FAQ chatbot that answers common questions about NTN registration, filing tax returns, PSEB registration and receiving foreign payments as a freelancer in Pakistan. Every answer shows its source and verification status, and the bot says so when it isn't sure.

Built for the **CodeAlpha Artificial Intelligence Internship** (Task 2: Chatbot for FAQs).

**Live demo:** https://ai-tax-faq-chatbot.streamlit.app/

> **Disclaimer:** This bot gives general information only, not tax advice. Tax rules change with each Finance Act. Always confirm current rates and deadlines on [fbr.gov.pk](https://fbr.gov.pk).

![Confident answer](screenshots/answer.png)
![Closest match, not fully sure](screenshots/closest_match.png)
![Refusal with suggested topics](screenshots/refusal.png)

---

## Contents
1. [Overview](#overview)
   - [What I built](#what-i-built)
   - [Where I used AI](#where-i-used-ai)
2. [Features](#features)
3. [How it works](#how-it-works)
4. [The FAQ data](#the-faq-data)
5. [Evaluation](#evaluation)
6. [Limitations](#limitations)
7. [Run it locally](#run-it-locally)
8. [Project structure](#project-structure)
9. [Future improvements](#future-improvements)
10. [What I learned](#what-i-learned)

---

## Overview

Many Pakistani freelancers struggle to find clear answers to basic tax questions: *What is an NTN? Do I have to file a return? How do I receive money from Upwork legally?* The information is scattered across long pages, and most of it is only in English.

This is a **retrieval-based** chatbot. It takes a question in English, Roman Urdu or a mix (for example *"Freelancing par tax kitna lagta hai?"*), finds the closest FAQ using NLP, TF-IDF and cosine similarity, and replies with the answer in the language you choose.

There is no generative AI in the bot. Every answer is a pre-written FAQ entry, so the bot cannot invent tax rules. How well each answer was checked varies, and each answer shows its own label (see [The FAQ data](#the-faq-data)).

### What I built

I designed and built this chatbot myself. I wrote all of the code (`matcher.py`, `user_interface.py`, `evaluate.py`).

- Designed the matching pipeline: preprocessing, TF-IDF vectorization, cosine similarity and the confidence threshold
- Chose character n-grams to handle inconsistent Roman Urdu spelling, and wrote the Roman Urdu stopword list
- Built the Streamlit chat interface and the off-topic refusal logic
- Wrote the evaluation script, and found that my first 96% score was misleading

### Where I used AI

AI was used only for the CSV data files (the FAQ answers, their verification labels and the test questions). None of the code was written by AI.

## Features

- **Two answer languages:** English or Roman Urdu, chosen in the sidebar.
- **Code-mixed input:** handles Roman Urdu, English, short keyword queries and typos.
- **Source and status on every answer:** a source line and a verification label.
- **Confidence labels:** "High match" or "Closest match, not fully sure".
- **"Why this answer?" expander:** shows the matched FAQ question and the similarity score.
- **Off-topic refusal:** weather, cricket, passports and similar questions are refused politely, with suggested topics.
- **Developer settings:** an adjustable confidence threshold (default 0.4), closed by default.
- **One-click example questions** and a **Clear chat** button.
- **Evaluation script** with accuracy by threshold, test type and language.

## How it works

```
User question
     │
     ▼
1. Preprocessing      lowercase → tokenize → remove English + Roman Urdu stopwords → lemmatize
     ▼
2. Vectorization      TF-IDF on character n-grams (3 to 5, char_wb)
     ▼
3. Similarity         cosine similarity against every FAQ phrasing (about 1,500)
     ▼
4. Decision           best score ≥ threshold (default 0.4) and best match is not the "out of scope" entry?
     │ yes                                  │ no
     ▼                                      ▼
Answer in English or Roman Urdu     "Can't help with this" + suggested topics
+ source + verification label
```

### Design decisions

**Character n-grams instead of words.** Roman Urdu has no standard spelling (*kaise / kese / kaisay*, *karein / karain*). Character n-grams (3 to 5) match partial overlaps between spellings and typos, which word-level TF-IDF would miss.

**Many phrasings per FAQ.** Each FAQ has between 22 and 59 alternative phrasings (about 37 on average, 1,485 in total): English questions, Roman Urdu questions, keywords and short forms. The bot compares the user's question with all of them and maps the best one back to its FAQ id.

**An explicit "out of scope" entry (id 0).** Instead of relying only on a score cutoff, the data has an entry (id 0) with 42 off-topic phrases such as cricket, weather and passport. If the nearest match is this entry, the bot refuses. This acts as a second line of defence against off-topic questions.

**A small Roman Urdu stopword list.** NLTK has no Roman Urdu stopwords, so I wrote a short set (*kya, hai, ka, ki, mein, kaise, mujhe, ...*) so filler words don't dominate the similarity score.

**Loading once.** The vectorizer and matrix are built once with `st.cache_resource`, so the app doesn't rebuild them on every message.

## The FAQ data

`faqs_new_updated.csv` has **40 rows: 39 FAQs (ids 1 to 39) and one out-of-scope entry (id 0)**.

| Category | FAQ ids | Examples |
|---|---|---|
| Registration | 1 to 8 | What is an NTN? How do I reset my IRIS password? |
| Filing returns | 9 to 16 | Who must file a return? What is the deadline? |
| Freelancer income | 17 to 24 | Is freelance income taxable? What are PSEB benefits? |
| Receiving payments | 25 to 32 | How do I receive money from Upwork? Is Payoneer allowed? |
| Common problems | 33 to 39 | What if I miss the deadline? What if I get an FBR notice? |

| Column | Description |
|---|---|
| `id` | FAQ id (`0` is reserved for out-of-scope) |
| `category` | Topic group |
| `question` | The main question |
| `variants` | Alternative phrasings separated by ` \| ` |
| `answer_en` / `answer_ur` | Answer in English / Roman Urdu |
| `source_line` | The official sources used |
| `last_verified` | Verification status and date |

### How the answers were made and checked
The answers were researched and drafted with AI assistance from official FBR, PSEB and SBP pages, then reviewed and edited. [Edit this sentence to match what you actually did.] The `last_verified` column records the status of each answer as of 14 and 19 November 2026, and the app shows it under every answer:

| Status | Answers |
|---|---:|
| Verified | 9 |
| Verified with caution (changes each year) | 7 |
| Partly verified | 14 |
| Correct with edits / Mostly correct with edits | 5 |
| Not independently verified | 4 |

I also spot-checked [LIST THE OFFICIAL PAGES YOU ACTUALLY OPENED, OR DELETE THIS SENTENCE] myself. "Verified" here means the claims matched the official pages consulted on that date, not that the answer is legally guaranteed.

## Evaluation

### Test sets
`faq_test_questions_50.csv` has **50 questions** written in different words from the FAQ phrasings. [STATE WHO WROTE THEM.] None appears word for word in the phrasings, but 4 are typo versions of existing phrasings (for example *"iris pasword reset"*), which flatters the short / typo score.

| Test type | Questions |
|---|---:|
| Paraphrase (English) | 9 |
| Roman Urdu | 10 |
| Short / typo | 10 |
| Indirect / scenario | 12 |
| Out of scope | 6 |
| Related but not covered | 3 |

41 of the 50 questions have an FAQ to match. The other 9 should be refused.

### Results by threshold

| Threshold | Overall | Answerable | Off-topic refused |
|:---:|:---:|:---:|:---:|
| 0.1 | 46.0% (23/50) | 48.8% (20/41) | 33.3% (3/9) |
| 0.2 | 46.0% (23/50) | 48.8% (20/41) | 33.3% (3/9) |
| 0.3 | 44.0% (22/50) | 46.3% (19/41) | 33.3% (3/9) |
| **0.4 (default)** | **50.0% (25/50)** | 46.3% (19/41) | 66.7% (6/9) |
| 0.5 | 40.0% (20/50) | 29.3% (12/41) | 88.9% (8/9) |

Results at 0.1 and 0.2 are identical.

**By test type at 0.4**

| Test type | Correct |
|---|---:|
| Paraphrase (English) | 22.2% (2/9) |
| Roman Urdu | 50.0% (5/10) |
| Short / typo | 70.0% (7/10) |
| Indirect / scenario | 41.7% (5/12) |
| Out of scope | 83.3% (5/6) |
| Related but not covered | 33.3% (1/3) |

**By question language at 0.4:** English 44.1% (15/34), Roman Urdu 62.5% (10/16).

### Why my first score was misleading
My first test set had 181 questions and scored about **96%** (174/181 at 0.4). But I had written the questions knowing the FAQs, and **18 of them appeared word for word in my phrasings**. I replaced it with the harder 50-question set above, and the score dropped to about 50%. A third small set of 20 questions scores 35% (7/20). Both earlier files are kept in the repo for reference.

### Reading the results
- **0.4 gives the best overall balance,** which is why it is the default. Higher thresholds refuse more off-topic questions (88.9% at 0.5) but also refuse valid ones (answerable accuracy falls to 29.3%).
- **The threshold is not the main limit.** Even at low thresholds only about half of answerable questions get the right FAQ. About half of the time the bot matches the wrong FAQ, which is a limit of word and character matching, not of the cutoff.
- **Best on short queries, weakest on paraphrases** that use different words from the FAQ wording.
- Each test type has only 3 to 12 questions, so one answer moves a percentage by 8 to 33 points. Treat the numbers as rough.
- The score measures whether the bot **picks the right FAQ**, not whether the tax content is legally correct.

## Limitations

- **Lexical, not semantic.** TF-IDF matches characters and words, not meaning. Reworded questions with little overlap can be missed or matched to the wrong FAQ.
- **"Related but not covered" questions** are hard to refuse, because they share vocabulary with real FAQs.
- **Small knowledge base:** 39 FAQs, so many legitimate tax questions are out of scope.
- **Verification varies** (see the table above). Answers are not legal advice, and tax rules change each year.
- **Roman Urdu spelling is not standardised,** so unusual spellings can still be missed.
- **No conversation memory.** Each question is answered on its own.
- **Small, partly self-written test set** (50 questions).

### Known issue
`evaluate.py` passes the language label `"urdu"` from the test file, while the app uses `"roman urdu"`, so evaluation returns English answers. Matching and the reported numbers are not affected.

## Run it locally

Requires **Python 3.12 or newer** (the app uses nested quotes inside f-strings).

```bash
git clone <your-repo-url>
cd CodeAlpha_FAQChatbot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run project/user_interface.py
```

Run the evaluation:
```bash
python project/evaluate.py
```

NLTK data (`punkt`, `punkt_tab`, `stopwords`, `wordnet`) downloads when `matcher.py` is imported.

`requirements.txt`: `streamlit`, `pandas`, `scikit-learn`, `nltk`

## Project structure

```
.
├── project/
│   ├── matcher.py                  # preprocessing, TF-IDF, matching, answer logic
│   ├── user_interface.py           # Streamlit chat UI
│   ├── evaluate.py                 # evaluation across thresholds
│   ├── faqs_new_updated.csv        # final FAQ knowledge base (used by the app)
│   ├── faq_test_questions_50.csv   # main test set (50 questions)
│   ├── faq_test_questions.csv      # earlier test set (181 questions, overlaps phrasings)
│   ├── faq_test_questions_new.csv  # extra test set (20 questions)
├── .streamlit/config.toml          # theme settings
├── requirements.txt
└── README.md
```

## Future improvements

I don't plan to continue this project, so these are suggestions for anyone who wants to build on it (you're welcome to fork it):

- **Sentence embeddings.** Try multilingual embeddings and compare them with TF-IDF using `evaluate.py`. They may help paraphrases. Roman Urdu support is uncertain and needs testing.
- **Hybrid retrieval** (TF-IDF plus embeddings), evaluated on the same test set.
- **Top-3 suggestions.** Measure how often the right FAQ is among the three best matches, and show "Did you mean...?" options when confidence is low.
- **A relevance classifier** to detect "related but not covered" questions.
- **A larger, independent test set,** for example questions from real users, kept separate from the phrasings.
- **Re-verify answers** against official FBR, PSEB and SBP pages after each Finance Act, and update the status labels.
- **Expand the knowledge base** (sales tax, SECP and sole proprietor registration, and more).
- **Urdu script (اردو) support** and spelling normalisation for Roman Urdu.
- **Conversation context** for follow-up questions.
- **User feedback** (thumbs up and down) to find gaps.
- **Unit tests** and a CI check that runs `evaluate.py`.

## What I learned

- How a classic retrieval pipeline works: preprocess, vectorize, compare, threshold.
- Why honest evaluation matters: my first test scored about 96%, but only because the questions overlapped my data. A fresh set gave about 50%.
- How a threshold trades coverage against safety, and why "I don't know" is better than a confident wrong tax answer.
- Handling low-resource, code-mixed language (Roman Urdu) with character n-grams and a custom stopword list.
- How Streamlit reruns the script, and why `session_state` and `st.cache_resource` are needed.
- Why a data pipeline needs verification labels, and how quickly tax information goes stale.

## Acknowledgements

- [CodeAlpha](https://www.codealpha.tech/) for the internship and the task.
- The public pages of FBR, PSEB and the State Bank of Pakistan, used as sources for the FAQ content.
- The open-source communities behind scikit-learn, NLTK, pandas and Streamlit.

## Author

**[YOUR NAME]**, 2nd-year Software Engineering student at the University of Gujrat.
[LinkedIn](https://linkedin.com/in/aafiaaftab) · [GitHub](https://github.com/[YOUR-USERNAME])

*Built during the CodeAlpha AI Internship.*
