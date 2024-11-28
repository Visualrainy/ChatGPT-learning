from langchain_openai import ChatOpenAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

def qa_agent(openai_api_key, memory, uploaded_file, question):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key = openai_api_key)
    
    file_content = uploaded_file.read()
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as temp_file: 
        temp_file.write(file_content)
    
    # load
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()

    # split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50, 
        separators=["\n","。", "！", "？", "，", "、", ""]
    )
    texts = text_splitter.split_documents(docs)
    
    # embedding and save in db
    embeddings_model = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings_model)
    
    # retriever
    retriever = db.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )
    response = qa.invoke({"chat_history": memory, "question": question})
    return response


 