from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from vector_1 import retriever

llm = OllamaLLM(model="qwen3:0.6b")

template = """
You are an expert in answering questions about coffee all of the world

here are some relevant reviews : {reviews}

here is the question to answer : {question}

"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm

while True :
    print("\n********")
    question = input("Ask a question to answer (q for quit) :")
    print("\n\n")
    if question == 'q':
        break

    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews":reviews,"question":question})
    print(result)