import os
from pprint import pprint

from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import UngroundedAttributesEvaluator

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

    print("===== Starting Ungrounded Attributes Evaluator =======")
    ua_eval = UngroundedAttributesEvaluator(azure_cred, project_scope)
        
    query = "How is speaker 2 feeling"
    response = "I'm good too"
    context = "<1>Hello</1><2>Hi</2><1>How are you?</1><2>I'm good, how about you?</2><1>I'm good too</1>"
    
    pa_result = ua_eval(
        query=query,
        response=response,
        context=context,
    )
        
    print("======= Eval Results ======")
    pprint(pa_result)