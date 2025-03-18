import os
from pprint import pprint

from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import CodeVulnerabilityEvaluator

os.environ["AZURE_SUBSCRIPTION_ID"] = ""
os.environ["RESOURCE_GROUP"] = ""
os.environ["PROJECT_NAME"] = ""

if __name__ == '__main__':


    project_scope = {
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
        "resource_group_name": os.environ.get("RESOURCE_GROUP"),
        "project_name": os.environ.get("PROJECT_NAME"),
    }
    azure_cred = DefaultAzureCredential()

    print("===== Starting Code Vulnerability Evaluator =======")
    code_vuln_eval = CodeVulnerabilityEvaluator(credential=azure_cred, azure_ai_project=project_scope)
    
    context = "{\n\t\t\t\t\toptimize"
    completion = "dKeys = false;\n"
    
    code_vulnerability_result = code_vuln_eval(
        query=context,
        response=completion
    )
        
    print("======= Eval Results ======")
    pprint(code_vulnerability_result)