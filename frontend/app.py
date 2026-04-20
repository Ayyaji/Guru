import streamlit as st
import requests

st.set_page_config(page_title="GURU", page_icon="🧠")
st.title("GURU")

with st.sidebar:
    st.header("GURU")
    upload_file= st.file_uploader("Give GURU some context (PDF)", type="pdf")

user_input= st.chat_input("Helu Maga,Yen beku")
if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("GURU is thinking..."):
        respose=requests.post("http://localhost:8000/chat",json={"content":user_input})
    

    if respose.status_code==200:
        data= respose.json()
        with st.chat_message("assistant"):  
            st.markdown(data["response"])
    else:
        st.error("Failed to get response from GURU")


st.divider()
uploaded_file = st.file_uploader("Give GURU some context (PDF)", type="pdf")