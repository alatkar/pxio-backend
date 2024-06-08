import os
import logging
from langchain_community.document_loaders.pdf import PyPDFLoader, PyPDFDirectoryLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def splitDocumentsFromFolder(path: str):
  # V1: Loads all PDF file
  # loader = PyPDFDirectoryLoader(path)
  # raw_docs = loader.load()
  
  # V2: Tried DirectoryLoader, but failed
  # dirLoader= DirectoryLoader(path=path)
  # raw_docs = dirLoader.load()
  
  raw_docs = []
  for file in os.listdir(path):
      if file.endswith('.pdf'):
        pdf_path = path + '/' + file
        loader = PyPDFLoader(pdf_path)
        raw_docs.extend(loader.load())
      elif file.endswith('.docx') or file.endswith('.doc'):
        doc_path = path + '/' + file
        loader = Docx2txtLoader(doc_path)
        raw_docs.extend(loader.load())
      elif file.endswith('.txt'):
        text_path = path + '/' + file
        loader = TextLoader(text_path)
        raw_docs.extend(loader.load())
      elif file.endswith('.xlsx') or file.endswith('.xls'):
        xls_path = path + '/' + file
        loader = UnstructuredExcelLoader(xls_path)
        raw_docs.extend(loader.load())
      elif file.endswith('.csv') or file.endswith('.xls'):
        csv_path = path + '/' + file
        loader = CSVLoader(csv_path)
        raw_docs.extend(loader.load())
      else:
        logging.error(f"Unknown file found {file}")
        

  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
  )
  # text_splitter = RecursiveCharacterTextSplitter(
  #   chunk_size=500, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
  # )
  
  docs = text_splitter.split_documents(documents=raw_docs)
  print(f"Split {len(raw_docs)} original documents into {len(docs)} documents")
  return docs


def splitDocument(file: any):
    loader = PyPDFLoader(file)
    raw_docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(documents=raw_docs)
    print(f"Split {len(raw_docs)} original documents into {len(docs)} documents")
    return docs

# Extract Images and Pass in Response
from PyPDF2 import PdfReader
def extractImages():
  reader = PdfReader("example.pdf")
  page = reader.pages[0]
  count = 0
  for image_file_object in page.images:
      with open(str(count) + image_file_object.name, "wb") as fp:
          fp.write(image_file_object.data)
          count += 1