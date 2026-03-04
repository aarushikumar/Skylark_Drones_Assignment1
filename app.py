import streamlit as st
from agent import answer_question

st.title("Monday.com Business Intelligence Agent")

question = st.text_input("Ask a business question")

if question:

    response, actions = answer_question(question)

    st.subheader("Agent Actions")

    for a in actions:
        st.write("-", a)

    st.subheader("Answer")

    st.write(response)