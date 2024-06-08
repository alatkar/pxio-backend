import json
import time, os
import logging
from types import SimpleNamespace
from typing import Tuple

from apis.documentmanager.documentutilities import splitDocumentsFromFolder
from . import app, cache
from flask import Blueprint, make_response, redirect, request, session
from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile, TemporaryDirectory

from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string

from .dotastoremanager.vectorstoreprovider import getOrCreateVectorStoreFromFolder, getvectorstoreForIndex, GellAllIndicesInVectorDb
from .llmmanager.runllms import executeLlmChain
from .llmmanager.prompts_new import prompt_proposal

logging.basicConfig(level=logging.INFO)

proposals = Blueprint('proposals', __name__, url_prefix='/proposals')
logger = logging.getLogger('Proposals Controller')

@proposals.route("/")
def get_proposal():
    return {"res": "val"}

@proposals.route('/<proposalid>', methods=["GET"])
@cache.cached()
def getRfpSummary(proposalid: str):
  if request.method == "GET":
    chat_history: str = [Tuple[str, str]]
    vectorStore = getvectorstoreForIndex(proposalid)
    
    ### resultSummary = executeSummarizationChain(vectorStore=vectorStore, prompt=prompt_overview_new, chainType="stuff", documentCount=20)
    
    proposal = executeLlmChain(prompt=prompt_proposal, vectorStore=vectorStore) 
    return {
      "proposal": proposal, 
    }

@proposals.route("/{proposalid}")
def new_proposal():
    return {"NEWres": "val"}
