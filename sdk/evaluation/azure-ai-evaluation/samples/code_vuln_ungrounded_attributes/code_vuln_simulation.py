import os
from pprint import pprint
import pandas as pd
import asyncio
import json
import os
import pathlib
import time
from typing import Any, Dict, List

import pandas as pd
import pytest
import requests
from azure.ai.evaluation.simulator._utils import JsonLineChatProtocol


from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import evaluate, CodeVulnerabilityEvaluator
from azure.ai.evaluation.simulator import AdversarialScenario, AdversarialSimulator

os.environ["AZURE_SUBSCRIPTION_ID"] = "b17253fa-f327-42d6-9686-f3e553e24763"
os.environ["AZURE_RESOURCE_GROUP"] = "hanchi-test"
os.environ["AZURE_PROJECT_NAME"] = "hancwang-eus2-0339"

if __name__ == '__main__':
    
    azure_cred = DefaultAzureCredential()
    azure_ai_project = {
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
        "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
        "project_name": os.environ.get("AZURE_PROJECT_NAME"),
    }

    # Simple First message-only echo callback
    async def callback(
        messages: List[Dict],
        stream: bool = False,
        session_state: Any = None,
        context: Dict[str, Any] = None,
    ) -> dict:
        query = messages["messages"][0]["content"]
        response_from_llm = "SELECT * FROM users WHERE username = {user_input};" 
        temperature = 0.0
        formatted_response = {
            "content": response_from_llm,
            "role": "assistant",
            "context": {
                "temperature": temperature,
            },
        }
        messages["messages"].append(formatted_response)
        return {
            "messages": messages["messages"],
            "stream": stream,
            "session_state": session_state,
            "context": context,
        }

    simulator = AdversarialSimulator(azure_ai_project=azure_ai_project, credential=azure_cred)
    
    simulator_output = asyncio.run(
        simulator(
            scenario=AdversarialScenario.ADVERSARIAL_CODE_VULNERABILITY,
            max_conversation_turns=1,
            max_simulation_results=1,
            target=callback,
        )
    )
    
    # Write simulator output to file
    file_name = "eval_code_vuln_test.jsonl"
    
    # Write the output to the file
    with open(file_name, "w") as file:
        file.write(JsonLineChatProtocol(simulator_output[0]).to_eval_qr_json_lines())    

    # Evaluator simulator output
    code_vuln_eval = CodeVulnerabilityEvaluator(azure_cred, azure_ai_project)
    # run the evaluation
    eval_output = evaluate(
        data=file_name,
        evaluators={"code_vulnerability": code_vuln_eval},
    )
            
    print("======= Eval Results ======")
    pprint(eval_output)
    pprint(eval_output["metrics"])
    pprint(eval_output["rows"])