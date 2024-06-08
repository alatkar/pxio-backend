from typing import Dict, List

from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string

def executeLlmChain(prompt: str, vectorStore: any, documents=12, chainType="stuff"):
    #llm = ChatOpenAI(verbose=True, temperature=0, model="gpt-4-0125-preview")
    #llm = ChatOpenAI(verbose=True, temperature=0, model="gpt-4")
    llm = ChatOpenAI(verbose=True, temperature=0, model="gpt-3.5-turbo-0125")
    
    qa = RetrievalQA.from_llm(
        llm=llm,
        # retriever=vectorStore.as_retriever(),
        retriever=vectorStore.as_retriever(search_kwargs={"k": documents}),
        # chain_type_kwargs={"return_source_documents": True}
        #chain_type_kwargs={"chain_type": chainType, "return_source_documents": True}
    )


    result = qa({"query": prompt})
    finalRes = result["result"]
    return finalRes


def executeLlmConversationChain(
    prompt: str, vectorStore: any, documents=4,chatHistory: List[tuple[str, str]] = ()
):
    
    chat = ChatOpenAI(verbose=True, temperature=0)
    qa = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=vectorStore.as_retriever(search_kwargs={"k": documents}),        
        return_source_documents=True,
    )

    result = qa({"question": prompt, "chat_history": []})
    return result


def executeSummarizationChain(
    vectorStore: any, prompt=" ", chainType="map_reduce", documentCount=100
):
    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")
    chain = load_summarize_chain(llm=llm, chain_type=chainType)

    # search = vectorStore.similarity_search(prompt)
    docs = vectorStore.as_retriever(
        search_kwargs={"k": documentCount}
    ).get_relevant_documents(prompt)
    result = chain.run(docs)
    return result
