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
lang = st.sidebar.radio("**Select your language for answer:**", ["English", "Roman Urdu"])
lang = lang.lower()
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

st.sidebar.markdown("")
with st.sidebar.expander("Developer Settings"):
    threshold_score = st.slider("Confidence threshold: ", 0.0, 1.0, 0.3)
    st.caption("Below this score, the bot says it doesn’t know.")

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
    ans = get_answer(vectorizer, training_matrix, question, lang, id_dataset, df, threshold_score)
    st.session_state["messages"].append({"user": question, "bot": ans["answer"], "id": ans["id"], "source": ans["source"], "last_checked": ans["last_checked"], "score": ans["score"], "matched_question": ans["matched question"], "label": ans["label"]})

for chat_line in st.session_state["messages"]:
    with st.chat_message("user"):
        st.write(chat_line["user"])
    if chat_line["label"] != "Can't help with this":
        with st.container():
            st.write(chat_line["label"])
            with st.chat_message("assistant"):
                st.write(chat_line["bot"])
                if chat_line["id"] != 0:
                    st.caption("Source: " + chat_line["source"])
                    st.caption("Last checked: " + chat_line["last_checked"])
                    with st.expander("Why this answer?"):
                        st.write("matched question: " + chat_line["matched_question"])
                        st.write(f"Score: {chat_line["score"] * 100:.2f}%")
    else:
        with st.container():
            st.write(chat_line["label"])
            st.write("I can only answer questions about Pakistan tax and freelancing.")
            with st.expander("Try asking about one of these:"):
                st.markdown("● " + "**NTN**")
                st.write("● " + "**Filing returns**")
                st.write("● " + "**PSEB registration**")
                




