from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from config import llm
from system_prompt import SYSTEM_PROMPT
from tools import read_paper, save_coding_result

tools = [read_paper, save_coding_result]

coder = create_agent(
    llm,
    system_prompt=SYSTEM_PROMPT,
    tools=tools,
)


def code_paper(file_path: str) -> dict:
    """Run the coding agent on a paper file and return the result messages."""
    prompt = f"""Please code the following paper for the SMS study.

Steps:
1. Use the `read_paper` tool to read the file: {file_path}
2. Extract bibliographic info and apply inclusion/exclusion criteria
3. If included, perform full coding (RQ1–RQ4)
4. IMPORTANT for RQ1: Each item in the lists MUST be a verbatim sentence copied word-for-word from the paper. Do NOT paraphrase or summarize.
5. Format the result as a JSON object with this structure:
{{
  "paper_info": {{
    "title": "...",
    "authors": [{{"name": "...", "affiliation": "..."}}],
    "year": "...",
    "venue": "...",
    "publication_type": "journal|conference|workshop|preprint|technical_report",
    "peer_reviewed": "yes|no|unclear",
    "doi_url": "...",
    "open_source_artifact": "yes|no|partial",
    "affiliation_region": "..."
  }},
  "included": true,
  "exclusion_reason": null,
  "coding": {{
    "RQ1": {{
      "Perception_ContextAcquisition": [],
      "Environment_Interaction": [],
      "Tool_CapabilityUse": [],
      "Memory_StateManagement": [],
      "Reasoning_Planning": [],
      "Action_Execution": [],
      "Feedback_Reflection": [],
      "Human_Collaboration": [],
      "Role_MultiagentCoordination": [],
      "Governance_Traceability": []
    }},
    "RQ2": {{
      "primary_form": "...",
      "secondary_form": null
    }},
    "RQ3": {{
      "application_domain": "...",
      "task_context": "...",
      "target_users": "...",
      "digital_artifacts": [],
      "domain_tools": []
    }},
    "RQ4": {{
      "evaluation_type": [],
      "benchmarks_datasets": [],
      "baselines": null,
      "metrics": [],
      "agentic_specific_metrics": [],
      "reproducibility": "yes|no|partial",
      "validity_discussion": "yes|no",
      "domain_validation": "yes|no",
      "statistical_analysis": "yes|no"
    }}
  }}
}}
5. Use `save_coding_result` tool with the paper title and the JSON string to save the result.
6. After saving, output the COMPLETE JSON object in your final reply (not a summary, the full JSON).
"""
    result = coder.invoke({"messages": [HumanMessage(content=prompt)]})
    return result["messages"][-1].content
