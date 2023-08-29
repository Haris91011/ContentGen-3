import streamlit as st
from streamlit_chat import message
from streamlit_Utilities import *

openapi_key = st.secrets["open_ai_key"]
# openai.api_key = api_key.key
openai.api_key = openapi_key

st.title('Comment Replier')
prompt = st.text_input('Write Your comment.')
if 'Reply' not in st.session_state:
    st.session_state['Reply'] = []

Reply,col1,col2,col3,col4=st.columns(5)

if prompt:
    with Reply:
        if st.button("Generate Reply",use_container_width=True):
            st.session_state['Reply']=commentReplier(prompt)

if st.session_state['Reply']:
    st.header("Reply Generated")
    message(st.session_state['Reply'])