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
from .llmmanager.runllms import executeLlmChain, executeLlmConversationChain, executeSummarizationChain
from .llmmanager.prompts_new import prompt_overview as prompt_overview_new, prompt_client_Information, prompt_project_timeline_and_future_work, prompt_evaluation_criteria, prompt_project_history
from .llmmanager.prompts_new import prompt_scope_of_work, prompt_proposal_timeline, prompt_required_qualification, prompt_financial_obligations, prompt_contact_information, prompt_submittal_process
from .llmmanager.prompts_new import prompt_role, prompt_format

logging.basicConfig(level=logging.INFO)

rfp = Blueprint('rfps', __name__, url_prefix='/rfps')
logger = logging.getLogger('RFP Controller')

def get_rfp():
    return {"res": "val"}

# Get All RFPs and Create new RFP
# ???? Why do we need this slash. Without this I am getting HTTP 308 for OPTIONS
@rfp.route("/", methods=["GET", "POST", "OPTIONS"])
def getOrCreateRfp():
    if request.method == "POST":
      if 'file' not in request.files:
        logger.log(level=0, msg='No file part')
        return ({"res": "No File"})
      files = request.files.getlist('file')
      # if files.count() > 0:
      #   logger.log('No file part')
      #   return ({"res": "No File"})
      #files = request.files.getlist['file']
      rfpid= request.form.get("rfpid")            
      target = TemporaryDirectory()
      if not os.path.isdir(target.name):
        os.mkdir(target)
      for file in files:
        # name = request.FILES[filename].name    
        logger.log(1, msg="Saving file "+ file.filename)
        file.save(os.path.join(target.name, secure_filename(file.filename)))
      vectorStore, indexName = getOrCreateVectorStoreFromFolder(dir_path=target.name, index_name=rfpid, recreate=False)
      return ({"res": "Created IndexName => " + indexName })
    
          
    # elif request.method == "OPTIONS":
    #   return _build_cors_preflight_response()
    elif request.method == "OPTIONS":
      return ({"res": "Options"})
    else:
      result = GellAllIndicesInVectorDb()
      return ({"res": result})

@rfp.route('/<rfpid>/summary', methods=["GET"])
@cache.cached()
def getRfpSummary(rfpid: str):
  if request.method == "GET":
    chat_history: str = [Tuple[str, str]]
    vectorStore = getvectorstoreForIndex(rfpid)
    
    ### resultSummary = executeSummarizationChain(vectorStore=vectorStore, prompt=prompt_overview_new, chainType="stuff", documentCount=20)
    
    resultOverview = executeLlmChain(prompt=prompt_overview_new, vectorStore=vectorStore) 
    
    resultClient = executeLlmChain(prompt=prompt_client_Information, vectorStore=vectorStore)
    chat_history.append([prompt_client_Information, resultClient])
    
    resultProjectHistory = executeLlmChain(prompt=prompt_project_history, vectorStore=vectorStore)
    chat_history.append([prompt_project_history, resultProjectHistory])
    
    resultSow = executeLlmChain(prompt=prompt_scope_of_work, vectorStore=vectorStore)
    chat_history.append([prompt_scope_of_work, resultSow])
    
    resultProposalTimeline = executeLlmChain(prompt=prompt_proposal_timeline, vectorStore=vectorStore)
    chat_history.append([prompt_proposal_timeline, ])
    
    resultQualification = executeLlmChain(prompt=prompt_required_qualification, vectorStore=vectorStore)
    chat_history.append([prompt_required_qualification, resultQualification])
    
    resultFinancialObligation = executeLlmChain(prompt=prompt_financial_obligations, vectorStore=vectorStore)
    chat_history.append([prompt_financial_obligations, resultFinancialObligation])
        
    # resultTimelineFutureWorkw = executeLlmChain(prompt=prompt_project_timeline_and_future_work, vectorStore=vectorStore)
    # chat_history.append([prompt_project_timeline_and_future_work, resultTimelineFutureWorkw])
    
    resultEvaluation = executeLlmChain(prompt=prompt_evaluation_criteria, vectorStore=vectorStore)
    chat_history.append([prompt_evaluation_criteria, resultEvaluation])
    
    resultContactInformation = executeLlmChain(prompt=prompt_contact_information, vectorStore=vectorStore)
    chat_history.append([prompt_contact_information, resultContactInformation])
    
    resultSubmittalProcess = executeLlmChain(prompt=prompt_submittal_process, vectorStore=vectorStore)
    chat_history.append([prompt_submittal_process, resultSubmittalProcess])
    
    return {
      "summary": resultOverview, 
      "client": resultClient, 
      "projectHistory": resultProjectHistory, 
      "sow": resultSow, 
      "resultProposalTimeline": resultProposalTimeline, 
      "qualification": resultQualification, 
      "financialObligation": resultFinancialObligation, 
      
      # "timelineSow": resultTimelineFutureWorkw, 
      "evaluation": resultEvaluation,
      "contact": resultContactInformation,
      "submittalProcess": resultSubmittalProcess,
    }
    
@rfp.route('/<rfpid>/overview', methods=["GET"])
@cache.cached()
def getRfpOverview(rfpid: str):
  if request.method == "GET":
    chat_history: str = [Tuple[str, str]]
    vectorStore = getvectorstoreForIndex(rfpid)    
    resultOverview = executeLlmChain(prompt=prompt_overview_new, vectorStore=vectorStore) 
    
    return {
      "summary": resultOverview, 
    }
 
@rfp.route('/<rfpid>/finance', methods=["GET"])
@cache.cached()
def getRfpFinancialObligation(rfpid: str):
  if request.method == "GET":
    chat_history: str = [Tuple[str, str]]
    vectorStore = getvectorstoreForIndex(rfpid)    
    resultFinancialObligation = executeLlmChain(prompt=prompt_financial_obligations, vectorStore=vectorStore)
    
    return {
      "financialObligation": resultFinancialObligation, 
    } 

@rfp.route('/<rfpid>/projecthistory', methods=["GET"])
@cache.cached()
def getRfpHistory(rfpid: str):
  if request.method == "GET":
    chat_history: str = [Tuple[str, str]]
    vectorStore = getvectorstoreForIndex(rfpid)    
    resultProjectHistory = executeLlmChain(prompt=prompt_project_history, vectorStore=vectorStore)
    
    return {
      "projectHistory": resultProjectHistory, 
    } 

@rfp.route('/<rfpid>/chat', methods=["POST"])
#@cache.cached()
def rfpConversation(rfpid: str):
  # Support chat history
  data = request.data  
  messages = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
  users = json.loads(request.data)
  for user in users["messages"]:
    print(user["role"])
    print(user["content"])
    prompt = user["content"]

  #req = request.json()
  #prompt = request.json['prompt']    
  prompt = prompt_role + " " + prompt + " " + prompt_format
  vectorStore = getvectorstoreForIndex(rfpid)
  resultPrompt = executeLlmChain(prompt=prompt, vectorStore=vectorStore)
  
  return resultPrompt
    
#Upload additional files for an RFP
@rfp.route('/<rfpid>/upload', methods=['POST'])
def fileUpload():
  target = TemporaryDirectory()
  # target=os.path.join(temp_dir,'test_docs')
  if not os.path.isdir(target):
      os.mkdir(target)
  logger.info("welcome to upload`")
  file = request.files['file'] 
  filename = secure_filename(file.filename)
  destination="/".join([target, filename])
  file.save(destination)
  session['uploadFilePath']=destination
  response="Whatever you wish too return"
  return response

@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        f.save(f.filename)   
        return {"name": f.filename}
      
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response