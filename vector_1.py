from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
import os
import pandas as pd

embeddings = OllamaEmbeddings(model='mxbai-embed-large')

df = pd.read_csv("simplified_coffee.csv")

chroma_location = ".\chroma_location"

add_document = not os.path.exists(chroma_location)

if add_document :
    documents=[]
    ids=[]

    for index , row in df.iterrows():
        document = Document(
            page_content=row['review'],
            metadata ={"review_data":row['review_date'],"Rating":row['rating'],"Price_for_100g":row['100g_USD'],'location':row['loc_country']},
            id=str(index) 
        )
        documents.append(document)
        ids.append(str(index))
    print(document)

vectore_store = Chroma(
    collection_name="simplified_coffee",
    persist_directory=chroma_location,
    embedding_function=embeddings
)

if add_document :
    vectore_store.add_documents(documents=documents,ids=ids)

retriever= vectore_store.as_retriever(
    search_kwagds={'k':5}
)