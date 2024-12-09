import os
from pprint import pprint
import pandas as pd
import uuid
import pathlib

from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import evaluate, ContentSafetyEvaluator


os.environ["AZURE_SUBSCRIPTION_ID"] = "b17253fa-f327-42d6-9686-f3e553e24763"
os.environ["RESOURCE_GROUP"] = "hanchi-test"
os.environ["PROJECT_NAME"] = "hancwang-eus2-0339"

if __name__ == '__main__':
    
    project_scope = {
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
        "resource_group_name": os.environ.get("RESOURCE_GROUP"),
        "project_name": os.environ.get("PROJECT_NAME"),
    }
    azure_cred = DefaultAzureCredential()

    print("\n===== Reading Data File =======")

    data_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "data")
    file_path = os.path.join(data_path, "dataset_messages_image_urls.jsonl")
    input_data = pd.read_json(file_path, lines=True)
    pprint(input_data)

    print("\n===== Calling Evaluate API - Content Safety Evaluator for multi-modal =======")
    content_safety_eval = ContentSafetyEvaluator(
        azure_ai_project=project_scope, credential=azure_cred
    )

    result = evaluate(
        evaluation_name=f"evaluate-api-multi-modal-eval-dataset-{str(uuid.uuid4())}",
        azure_ai_project=project_scope,
        data=file_path,
        evaluators={"content_safety": content_safety_eval}
    )
    print("\n======= Eval Results ======")
    pprint(result["rows"])