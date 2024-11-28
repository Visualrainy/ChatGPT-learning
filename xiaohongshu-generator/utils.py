from prompt_template import system_template_text, user_template_text
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from xiaohongshu_model import Xiaohongshu
import os

def generate_xiaohognshu(theme, openai_api_key) -> Xiaohongshu:
    prompt = ChatPromptTemplate.from_messages([("system", system_template_text), ("user", user_template_text)])
    model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
    output_parser = PydanticOutputParser(pydantic_object=Xiaohongshu)
    print(output_parser.get_format_instructions())

    chain = prompt | model | output_parser
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "theme": theme
    })
    return result
# print(os.getenv("OPENAI_API_KEY"))
# print(generate_xiaohognshu("大模型", os.getenv("OPENAI_API_KEY")))