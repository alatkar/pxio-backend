import os
import time
from typing import List

from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone as Client, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from ..documentmanager.documentutilities import splitDocumentsFromFolder

embeddings = OpenAIEmbeddings()
spec = ServerlessSpec(cloud="aws", region="us-west-2")
api_key = os.environ.get("PINECONE_API_KEY") or "PINECONE_API_KEY"
environment = os.environ.get("PINECONE_ENVIRONMENT") or "PINECONE_ENVIRONMENT"
pc = Client(api_key=api_key)


def GellAllIndicesInVectorDb() -> List[str]:
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    # index = pc.Index(existing_indexes[0])
    return existing_indexes


def IsIndexPresent(index_name: str) -> bool:
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    if index_name in existing_indexes:
        return True
    else:
        return False


def GetOrCreateVectorStore(docs: List[Document], index_name: str, recreate: bool):
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    # check if index already exists (it shouldn't if this is first time)
    if index_name not in existing_indexes:
        # if does not exist, create index
        pc.create_index(
            index_name,
            dimension=1536,  # dimensionality of minilm
            metric="dotproduct",
            spec=spec,
        )
        # wait for index to be initialized
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    # connect to index
    index = pc.Index(index_name)
    time.sleep(1)
    # view index stats
    print(index.describe_index_stats())

    total_vector_count = index.describe_index_stats()["total_vector_count"]
    if recreate and total_vector_count > 0:
        Pinecone.delete_index(
            index_name
        )  # Find function to clean it, rather than delete

    if total_vector_count == 0:
        vectorstore = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    else:
        vectorstore = Pinecone(index, embeddings.embed_query, "text")

    return vectorstore


def AddMoreDocumentsToVectorStore(docs: List[any], vectorstore):
    result = vectorstore.add_documents(docs)
    return result

def getOrCreateVectorStoreFromFolder(dir_path: str, index_name: str, recreate=False):
    # index_name = (
    #     os.path.basename(os.path.normpath(dir_path)).lower().strip().replace(" ", "")
    # )
    documents = []
    if not IsIndexPresent(index_name):
        documents = splitDocumentsFromFolder(dir_path)

    vectorstore = GetOrCreateVectorStore(
        documents, index_name=index_name, recreate=False
    )
    return vectorstore, index_name


def getvectorstoreForIndex(index_name: str):
  existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
  if index_name in existing_indexes:
    vectorstore = GetOrCreateVectorStore([], index_name=index_name, recreate=False)
    return vectorstore
  else:
    return None

  