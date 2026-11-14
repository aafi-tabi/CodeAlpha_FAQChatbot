import streamlit as st
from matcher import load_bot, get_answer

@st.cache_resource
def get_bot():
    id_dataset, df, training_matrix, vectorizer = load_bot()
    return id_dataset, df, training_matrix, vectorizer

id_dataset, df, training_matrix, vectorizer = get_bot()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.sidebar.markdown("**TAX HELPER**")
st.sidebar.markdown("")
st.sidebar.markdown("**Answer Lanquage**")
lang = st.sidebar.radio("**Select your language for answer:**", ["Urdu", "English"])
lang = lang.lower()
st.sidebar.markdown("")
st.sidebar.slider("Confidence threshold: ", 0.0, 1.0, 0.3, disabled = True)
st.sidebar.caption("Below this score, the bot says it doesn’t know.")
st.sidebar.markdown("")
with st.sidebar:
    with st.container():
        st.markdown("**Try asking**")
        b1 = st.button("What is an NTN?")
        b2 = st.button("How do I register with PSEB?")
        b3 = st.button("Freelancing par tax kitna lagta hai?")

clr_chat = st.sidebar.button("**Clear chat**")
if clr_chat:
    st.session_state["messages"] = []

st.title("Pakistan Tax & Freelancer FAQ Bot")
st.markdown("**Ask about NTN, filing returns, PSEB registration and receiving foreign payments. Answers in English or Roman Urdu.**")
st.info("General information only, not tax advice. Check current rates and deadlines on fbr.gov.pk.")

question = None
if b1:
    question = "What is an NTN?"
elif b2:
    question = "How do I register with PSEB?"
elif b3:
    question = "Freelancing par tax kitna lagta hai?"
else:
    question = st.chat_input("Ask a question: ")

if question:
    id, ans = get_answer(vectorizer, training_matrix, question, lang, id_dataset, df)
    st.session_state["messages"].append({"user": question, "bot": ans})

for chat_line in st.session_state["messages"]:
    with st.chat_message("user"):
        st.write(chat_line["user"])
    with st.chat_message("assistant"):
        st.write(chat_line["bot"])


