import streamlit as st
import pandas as pd
from utils import dataframe_agent

def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["column"][0], inplace=True)
    
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)

st.title("CSV智能分析终端工具")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

data = st.file_uploader("上传的数据文件（CSV格式）：", type="csv")
if data: 
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])

query = st.text_area("请输入你关于以上表格的问题，或数据提取要求，或可视化要求（支持散点图、折线图、条形图）：")
button = st.button("生成回到")

if button and not openai_api_key:
    st.info("请输入密钥")
if button and "df" not in st.session_state:
    st.info("请先上传文件")
if button and openai_api_key and "df" in st.session_state:
    with st.spinner("AI正在思考中..."):
        resposne_dict = dataframe_agent(openai_api_key, st.session_state["df"], query)
        if "answer" in resposne_dict:
            st.write(resposne_dict["answer"])
        if "table" in resposne_dict:
            st.table(pd.DataFrame(resposne_dict["table"]["data"], 
                                  columns=resposne_dict["table"]["columns"]))
        if "bar" in resposne_dict:
            create_chart(resposne_dict["bar"], "bar")
        if "line" in resposne_dict:
            create_chart(resposne_dict["line"], "line")
        if "scatter" in resposne_dict:
            create_chart(resposne_dict["scatter"], "scatter")   
