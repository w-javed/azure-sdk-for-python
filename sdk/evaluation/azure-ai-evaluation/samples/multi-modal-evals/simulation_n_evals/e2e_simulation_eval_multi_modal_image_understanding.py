from pprint import pprint
import asyncio
import os
import json
import pandas as pd

from openai import AzureOpenAI 
from typing import Any, Dict, List, Optional

from azure.ai.evaluation.simulator import AdversarialScenario, AdversarialSimulator
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from azure.ai.evaluation import (
    ProtectedMaterialMultimodalEvaluator,
    evaluate,
)

# For Simulation/Evaluation
os.environ["AZURE_SUBSCRIPTION_ID"] = ""
os.environ["AZURE_RESOURCE_GROUP"] = ""
os.environ["AZURE_PROJECT_NAME"] = ""

# For LLM (Image Understanding use case)
os.environ["AZURE_DEPLOYMENT_NAME"] = ""
os.environ["AZURE_ENDPOINT"] = ""
os.environ["AZURE_API_VERSION"] = ""

# For LLM Dall-e-3 (Image generation)
os.environ["AZURE_DEPLOYMENT_NAME_DALLE"] = ""
os.environ["AZURE_ENDPOINT_DALLE"] = ""
os.environ["AZURE_API_VERSION_DALLE"] = ""

if __name__ == '__main__':
    
    azure_cred = DefaultAzureCredential()
    project_scope = {
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
        "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
        "project_name": os.environ.get("AZURE_PROJECT_NAME"),
    }

    def call_gen_ai_application_or_llm(user_prompt, system_prompt) -> str:
        deployment = os.environ.get("AZURE_DEPLOYMENT_NAME")
        endpoint = os.environ.get("AZURE_ENDPOINT")
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://cognitiveservices.azure.com/.default",
        )

        # Get a client handle for the AOAI model
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_version=os.environ.get("AZURE_API_VERSION"),
            azure_ad_token_provider=token_provider,
        )
        
        # Call the model 
        messages = []
        messages.append(
            {
                "role": "system",
                "content": system_prompt,
            }
        )
        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )
        
        completion = client.chat.completions.create(
            model=deployment,
            messages=messages,
        ) 

        response = completion.to_dict()["choices"][0]["message"]
        if type(response) == dict:
            content = response["content"]
        return content


    async def callback(
        messages: List[Dict],
        stream: bool = False,
        session_state: Any = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> dict:
        image_understanding_prompt = messages["messages"][0]["content"]
        content = call_gen_ai_application_or_llm(image_understanding_prompt, "You are an AI assistant who can describe images.")
        formatted_response = {
            "content": content, 
            "role": "assistant"
        }
        messages["messages"].append(formatted_response)
        return {
            "messages": messages["messages"],
            "stream": stream,
            "session_state": session_state,
            "context": context,
        }
                
    simulator = AdversarialSimulator(azure_ai_project=project_scope, credential=azure_cred)

    simulator_output = simulator(
            scenario=AdversarialScenario.ADVERSARIAL_IMAGE_UNDERSTANDING,
            max_conversation_turns=1,
            max_simulation_results=1,
            target=callback,
            api_call_retry_limit=3,
            api_call_retry_sleep_sec=1,
            api_call_delay_sec=30,
            concurrent_async_task=1,
        )

    pprint(simulator_output) 

    file_name = "eval_sim_test.jsonl"

    # Write the output to the file
    with open(file_name, "w") as file:
        file.writelines([json.dumps({"conversation":{"messages": conversation["messages"]}}) + "\n" for conversation in simulator_output])

    # Evaluator simulator output
    protected_material_eval = ProtectedMaterialMultimodalEvaluator(azure_cred, project_scope)
    # run the evaluation
    eval_output = evaluate(
        data=file_name,
        evaluation_name="sim_image_understanding_protected_material_eval",
        azure_ai_project=project_scope,
        evaluators={"protected_material": protected_material_eval},
    )

    row_result_df = pd.DataFrame(eval_output["rows"])
    metrics = eval_output["metrics"]
    pprint(row_result_df)
    pprint(metrics)

    # Cleanup file
    os.remove(file_name)