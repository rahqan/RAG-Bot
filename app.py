import streamlit as st
import hashlib
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
# from langchain_community.vectorstores import Pinecone
# from langchain_community.vectorstores import FAISS
from InstructorEmbedding import INSTRUCTOR
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_community.document_loaders import WebBaseLoader




def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    print(type(text))        
    return text 

def get_text_chunks(raw_text):
    text_splitter=CharacterTextSplitter(separator='\n',chunk_size=100,chunk_overlap=50,length_function=len)
    chunks=text_splitter.split_text(raw_text)
    return chunks

def convert_list_to_dict(input_list):
    # Initialize an empty dictionary
    output_dict = {}

    

    for i in range(0, len(input_list)-1):
        # Use the current element as the key and the next element as the value
        key = str(i)
        value = str(input_list[i])

        # Add the key-value pair to the dictionary
        output_dict[key] = value

    return output_dict

def get_web_text(url):
    loader=WebBaseLoader(url)
    document=loader.load()
    document=str(document[0])
    return document


def to_vector_db(text_chunks):
    pc = Pinecone(api_key='')
    index_name = "pdfapp"
    index = pc.Index(index_name)

    model = INSTRUCTOR('hkunlp/instructor-xl')
    instruction = "data of innovative product developement"

    for i in range(len(text_chunks)):
        # Ensure the embedding is a list of floats
        embeddings = model.encode([[instruction, text_chunks[i]]])[0]
        # index.upsert(vectors=[(text_chunks[i], embeddings)], namespace="ns1")
        
        index.upsert(vectors=[{"id":str(i),"values":embeddings,"metadata":{str(i):text_chunks[i]}}],namespace="ns1")



def query_to_vector(user_query):
    model = INSTRUCTOR('hkunlp/instructor-xl')
    instruction = "query on data of innovative product developement"
    embeddings = model.encode([[instruction, user_query]])[0].tolist()
    return embeddings


        
def relevant_search_in_db(vector_query):    
    pc = Pinecone(api_key='')
    index_name = "pdfapp"
    index = pc.Index(index_name)

    result=index.query(
  vector=vector_query,
  top_k=10,
  include_values=False,namespace="ns1",include_metadata=True
)
    return result
    







def main():
    load_dotenv()
    st.set_page_config(page_title="Chat With Multiple PDFs or any Website",page_icon=":books:")
    st.header("Chat with multiple PDFs :books:")
    
    # with st.sidebar:
    st.subheader("Your Documents")
    pdf_docs = st.file_uploader("Upload Your PDFs and click on 'Process'",accept_multiple_files=True)
    conversation = []
    


    user_query = st.text_input("Ask me anything")
    # webscrape the website

    # url=st.text_input("Enter url")
    # if url:
    #     raw_web_text=get_web_text(url)


    if user_query:
        conversation.append("User: " + user_query)
    if st.button("Process"):
        with  st.spinner("Processing"):

            # extract the pdf text
            raw_text = get_pdf_text(pdf_docs)
            

            # get the text chunks

            # web_text_chunks=get_web_text(raw_text)
            pdf_text_chunks=get_text_chunks(raw_text)
            

            
            st.write(pdf_text_chunks)

            # st.write(web_text_chunks)

            # create and store the data into vector store
            
            to_vector_db(pdf_text_chunks)
            # to_vector_db(web_text_chunks)
        
            print("converted and stored embeddings")
        
        # Get chatbot response when the user clicks the "Ask" button
            
            vector_query=query_to_vector(user_query)
            st.write("query in vector form:")
            
            st.write(vector_query)
            result=relevant_search_in_db(vector_query)
            st.write("Results:")
            print(result)
                    # Add the chatbot response to the conversation
            conversation.append("Chatbot: " + str(result))

    # llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="")




    # Display the conversation
    for message in conversation:
        st.write(message) 

        print(result)
            # print(vector_query)
        st.write(result)
        st.write("SUCCESSSS")








if __name__=="__main__":
    main()