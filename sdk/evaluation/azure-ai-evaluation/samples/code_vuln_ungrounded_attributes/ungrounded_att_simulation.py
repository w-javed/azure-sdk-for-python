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
from azure.ai.evaluation import evaluate, UngroundedAttributesEvaluator
from azure.ai.evaluation.simulator import AdversarialScenario, AdversarialSimulator

os.environ["AZURE_SUBSCRIPTION_ID"] = ""
os.environ["AZURE_RESOURCE_GROUP"] = ""
os.environ["AZURE_PROJECT_NAME"] = ""

if __name__ == '__main__':
    
    azure_cred = DefaultAzureCredential()
    azure_ai_project = {
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
        "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
        "project_name": os.environ.get("AZURE_PROJECT_NAME"),
    }

    response_from_llm = '''
        Person 1 might experience emotions such as:
            Curiosity – They may wonder what the experience of meditation feels like.
            Admiration – They might appreciate Person 2’s ability to find peace and focus.
            Inspiration – They could feel motivated to try meditation themselves.
            Serenity – Simply observing a calm moment might bring them a sense of peace.
            Happiness – Seeing someone enjoy a tranquil experience could make them feel happy.
            Their emotions would likely depend on their own mindset and past experiences with meditation or peaceful settings.
        ''' 

    # Simple First message-only echo callback
    async def callback(
        messages: List[Dict],
        stream: bool = False,
        session_state: Any = None,
        context: Dict[str, Any] = None,
    ) -> dict:
        import re
        generated_text = messages["messages"][0]["content"]
        
        conversation_match = re.search(r"<START CONVERSATION>(.*?)<END CONVERSATION>", generated_text, re.DOTALL)
        conversation = conversation_match.group(1).strip() if conversation_match else ""

        query_match = re.search(r"<END CONVERSATION>\s*(.*)", generated_text, re.DOTALL)
        query = query_match.group(1).strip() if query_match else ""

        messages = {"messages": []}
        user_message = {
            "content": query,
            "role": "user",
            "context": conversation,
        }
        
        temperature = 0.0
        formatted_response = {
            "content": response_from_llm,
            "role": "assistant",
            "context": {
                "temperature": temperature,
            },
        }
        messages["messages"].append(user_message)
        messages["messages"].append(formatted_response)
        return {
            "messages": messages["messages"],
            "stream": stream,
            "session_state": session_state,
            "context": conversation,
        }

    simulator = AdversarialSimulator(azure_ai_project=azure_ai_project, credential=azure_cred)
    
    simulator_output = asyncio.run(
        simulator(
            scenario=AdversarialScenario.ADVERSARIAL_UNGROUNDED_ATTRIBUTES,
            max_conversation_turns=1,
            max_simulation_results=1,
            target=callback,
        )
    )
    
    # Write simulator output to file
    file_name = "eval_ungrounded_attributes_test.jsonl"
    
    # Write the output to the file
    with open(file_name, "w") as file:
        file.write(JsonLineChatProtocol(simulator_output[0]).to_eval_qr_json_lines()) 

    # Evaluator simulator output
    ua_eval = UngroundedAttributesEvaluator(azure_cred, azure_ai_project)
    # run the evaluation
    eval_output = evaluate(
        data=file_name,
        evaluators={"ungrounded_attributes": ua_eval},
    )
            
    print("======= Eval Results ======")
    pprint(eval_output)
    pprint(eval_output["metrics"])
    pprint(eval_output["rows"])