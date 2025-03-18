import os
from pprint import pprint
import pandas as pd
import uuid
import pathlib
import json


from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import evaluate, UngroundedAttributesEvaluator


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
    evaluators = {
            "ungrounded_attributes": UngroundedAttributesEvaluator(azure_cred, project_scope),
        }

    # run the evaluation
    result = evaluate(
        data="evaluate_test_data_with_chat.jsonl",
        evaluators=evaluators,
    )
        
    print("======= Eval Results ======")
    pprint(result)
    pprint(result["metrics"])
    pprint(result["rows"])