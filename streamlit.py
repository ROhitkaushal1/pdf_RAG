from llama_index.llms.openai.base import OpenAI
from llama_index.core import (
    load_index_from_storage,
    StorageContext,
)
import time
from llama_index.vector_stores.faiss import FaissVectorStore
from dotenv import load_dotenv
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import StorageContext
import streamlit as st 
load_dotenv()



# load index from disk
vector_store = FaissVectorStore.from_persist_dir("./storage_1")
storage_context = StorageContext.from_defaults(
    vector_store=vector_store, persist_dir="./storage_1"
)
@st.cache_data
def fetch_index():
    idx = load_index_from_storage(storage_context=storage_context)
    return idx

from llama_index.core.prompts import PromptTemplate
from llama_index.core.query_engine import RetrieverQueryEngine




def question_answer(question):
    index = fetch_index() 
    custom_prompt = PromptTemplate(
    "We have provided context information below which is legal documentation and it has a title in which under we have lot of subheadings so if someone ask for the title information inckude all the subheadings. .\n"
    "here is the information {context_str}\n"
    "please answer the question in detail: {query_str} ."
    )

    #Retriver
    retriever = index.as_retriever(similarity_top_k=5)

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        text_qa_template=custom_prompt
    )

    response = query_engine.query(question)

    # LLM to answer
    llm = OpenAI(model="gpt-4o-mini")
    resp = llm.complete(str(response))
    resp_final = str(resp)
    return resp_final

    
#streamlit ui
def stream_data(x):
        for word in x.split(" "):
            yield word + " "
            time.sleep(0.02)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question:"):


    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"

    ans = question_answer(response)

    with st.chat_message("assistant"):
        
        st.write(stream_data(ans))
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ans})

if __name__ == "__main__":
    st.set_page_config(page_title="LLM Chatbot", page_icon=":robot:")
    st.title("LLM Chatbot")
    st.write("Ask me anything about the legal documents!")




 