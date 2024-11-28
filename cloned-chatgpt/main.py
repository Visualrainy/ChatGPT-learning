import streamlit as st
from langchain.memory import ConversationBufferMemory

from utils import get_chat_response

st.title("克隆ChatGPT")
with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

if "memory" not in st.session_state:
    memory = ConversationBufferMemory(return_messages=True)
    st.session_state["memory"] = memory
    st.session_state["message"] = [{"role":"ai", "content":"你好，我是你的ai助手，有什么可以帮助你的吗？"}]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("请输入你的OpenAI API Key")
        st.stop
    st.session_state["message"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中..."):
        response = get_chat_response(prompt, st.session_state["memory"], openai_api_key)
    
    msg = {"role": "ai", "content": response}
    st.session_state["message"].append(msg)
    st.chat_message("ai").write(response)