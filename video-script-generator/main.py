import streamlit as st
from utils import generate_script

st.title("视屏脚本生成器")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

subject = st.text_input("请输入视屏的主题")
video_length = st.number_input("请输入视屏的大致时长", min_value=0.1, step=0.1)
creativity = st.slider("请输入视屏的创造性", max_value=2.0, min_value=0.0, step=0.1, value=0.2)

submit = st.button("生成脚本")

if submit and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")
    st.stop()

if submit and not subject:
    st.info("请输入你的视屏主题")
    st.stop()

if submit and not video_length >= 0.1:
    st.info("请输入你的视屏时长大于等于0.1")
    st.stop()

if submit:
    with st.spinner("AI正在思考中..."):
        search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key)
    
    st.success("视屏脚本已经生成")
    st.subheader("标题")
    st.write(title)
    st.subheader("视屏脚本")
    st.write(script)
    with st.expander("维基百科搜索结构"):
        st.info(search_result)
    