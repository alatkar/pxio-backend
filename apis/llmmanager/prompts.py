
from langchain import PromptTemplate

prompt_insight: str = """
Based on this {project_summary} provided and the work items, {sows}
please detect what kind of civil engineering project is this. 
Also provide any insights or learnings from our knowledge base based on the those details.
"""

def getinsightprompt(summary: str, sows: str) -> str:
  prompt_template = PromptTemplate(
          template=prompt_insight, input_variables=["project_summary", "sows"]
  )
  template = prompt_template.format_prompt(project_summary=summary, sows=sows)
  return template


prompt_overview: str = """
Please provide concise and comprehensive summary of this Project. 
You should capture the main points and key details while conveying the intentions mentioned in this RFP.
Please keep all relevant details without repeating the content.
"""

prompt_client_information: str = """
Please provide details of the client information provide in the document.
Present this information in bullet points.
"""

prompt_scopeofwork: str = """
Please provide concise summary of all the tasks required in this RFP. 
Please provide as much technical information as possible. 
Please use Civil Engineering Langauge as much as possible to describe the statement of work expected in this RFP.
"""

prompt_timelines: str = """
What are different timelines and milestone dates provided in this document
Present this information in bullet points.
"""

prompt_qualifications: str = """
What are qualification, experience and other requirements expected from the contractors.
Present this information in bullet points.
"""

prompt_legal: str = """
What are different laws and regulations involved in this project?
Are there any regulatory requirements needed?
Present this information in bullet points.
"""

prompt_submittal: str = """
Give details of the submittal process. How are proposals evaluated?
Present this information in bullet points.
"""

