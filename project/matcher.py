import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pathlib import Path

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")


def read(path):
    try:
        dataframe = pd.read_csv(path)
        return dataframe
    except FileNotFoundError:
        print("File not found")
        

def clean_variants(df):
    df = df.copy()
    df["variants"] = df["variants"].apply(lambda x: list(dict.fromkeys(v.strip() for v in x.split(" | "))))
    return df 


def build_enteries(df):
    pairs = []
    for  key,value in df.iterrows():
        for line in value["variants"]:
            pair = [line, value["id"]]
            pairs.append(pair)

    return pairs


def preprocess(pairs):
    pairs = pairs.copy()

    stopwords_set_eng = stopwords.words("english")
    stopwords_set_urdu = {
    "kya", "hai", "hain", "ho", "hota", "hoti", "hota", "ka", "ki", "ke",
    "ko", "se", "me", "mein", "par", "pe", "aur", "ya", "kaise", "kese",
    "karein", "karain", "kare", "raha", "rahi", "aa",
    "gaya", "gayi", "mera", "meri", "mujhe", "main", "to", "bhi"
    }

    lemmatizer = WordNetLemmatizer()

    new_pairs = []
    training_dataset = []
    id_dataset = []
    for pair in pairs:
        pair[0] = word_tokenize(pair[0].lower())
        pair[0] = [word for word in pair[0] if word not in stopwords_set_eng]
        pair[0] = [word for word in pair[0] if word not in stopwords_set_urdu]
        pair[0] = [lemmatizer.lemmatize(word) for word in pair[0]]
        training_dataset.append(" ".join(pair[0]))
        id_dataset.append(pair[1])

    for pair in pairs:
        if pair not in new_pairs and (len(pair[0]) > 3):
            new_pairs.append(pair)

    return new_pairs, training_dataset, id_dataset


def train(data_set):
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
    training_matrix = vectorizer.fit_transform(data_set)
    return training_matrix, vectorizer


def get_answer(vectorizer, training_matrix, question, lang, id_dataset, df):
    _,processed_question,_ = preprocess([[question,0]])
    q_vector = vectorizer.transform(processed_question)
    cos_list = cosine_similarity(training_matrix, q_vector)
    ans_pos = cos_list.argmax()
    cos_ans = cos_list.max()
    id = id_dataset[ans_pos]

    if cos_ans > 0.3:
        for key,value in df.iterrows():
            if value["id"] == id:
                if lang == "roman urdu":
                    return id, value["answer_ur"]
                else:
                    return id, value["answer_en"]
    else:
        return 0, "Bot is not sure about this!"


def evaluate(vectorizer, training_dataset, questions_dataset, id_dataset, df):
    passed = 0
    failed = 0
    for key,value in questions_dataset.iterrows():
        id, ans = get_answer(vectorizer, training_dataset, value["test_question"], value["lang"], id_dataset, df)
        if value["expected_faq_id"] != "NONE":
            if id == int(value["expected_faq_id"]):
                print("test case passed")
                passed = passed + 1
            else: 
                if id == 0:
                    passed = passed + 1
                else:
                    failed = failed + 1
        else:
            print("Unexpected test case")
            passed = passed + 1

    total = passed + failed
    print((passed/total) * 100)

def load_bot():
    dataframe = read(Path(__file__).parent / "faqs_new.csv")
    df = clean_variants(dataframe)
    pairs = build_enteries(df)
    pair, training_dataset, id_dataset = preprocess(pairs)

    new_training_data = []
    new_id_dataset = []
    for text,id in zip(training_dataset,id_dataset):
        if len(text.split()) >= 1:
            new_training_data.append(text)
            new_id_dataset.append(id)
    print(len(training_dataset), len(new_training_data))
    training_matrix, vectorizer = train(new_training_data)
    return new_id_dataset, df, training_matrix, vectorizer

# print(dataframe)
# print(dataframe.info())
# print(df["variants"])
# print(df.info())
# print(pairs[:3])
# print(pair[:3])
# print(training_dataset[:3])
# print(id_dataset[:3])

if __name__ == "__main__":
    id_dataset, df, training_matrix, vectorizer = load_bot()

# id_dataset, df, training_matrix, vectorizer = load_bot()
# testcase = read("faq_test_questions.csv")
# print(testcase.info())
# evaluate(vectorizer, training_matrix, testcase, id_dataset, df)

