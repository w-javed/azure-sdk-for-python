from pprint import pprint
import asyncio
import os
import json
import pandas as pd
from pprint import pprint
import uuid

from openai import AzureOpenAI 
from typing import Any, Dict, List, Optional

from azure.ai.evaluation.simulator import AdversarialScenario, AdversarialSimulator
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from azure.ai.evaluation import (
    ProtectedMaterialMultimodalEvaluator,
    evaluate,
)

async def call_gen_ai_application_or_llm(user_prompt, system_prompt) -> str:
    print("\n===== Calling Gen AI App or LLM =======")
    print(f"\nUser Prompt: {user_prompt}")
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
        # api_key=os.environ["AZURE_API_KEY"],
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
    print(f"\nLLM Response: {response}")
    if type(response) == dict:
        content = response["content"]
    return content

async def callback(
    messages: List[Dict],
    stream: bool = False,
    session_state: Any = None,
    context: Optional[Dict[str, Any]] = None,
) -> dict:
    print("\n===== Callback function is called =======")
    image_understanding_prompt = messages["messages"][0]["content"]
    content = await call_gen_ai_application_or_llm(image_understanding_prompt, "You are an AI assistant who can describe images.")
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
    
async def run_simulation():
    print("\n===== Initializing env variables =======")
    
    # For Simulation/Evaluation
    os.environ["AZURE_SUBSCRIPTION_ID"] = ""
    os.environ["AZURE_RESOURCE_GROUP"] = ""
    os.environ["AZURE_PROJECT_NAME"] = ""

    # For LLM (Image Understanding use case)
    os.environ["AZURE_DEPLOYMENT_NAME"] = ""
    os.environ["AZURE_ENDPOINT"] = ""
    os.environ["AZURE_API_VERSION"] = ""
    os.environ["AZURE_API_KEY"] = ""

    azure_cred = DefaultAzureCredential()
    project_scope = {
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
        "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
        "project_name": os.environ.get("AZURE_PROJECT_NAME"),
    }

    print("\n===== Initializing Adversarial Simulator =======")            
    simulator = AdversarialSimulator(azure_ai_project=project_scope, credential=azure_cred)

    print("\n===== Running Adversarial Simulator for Image Understanding =======")     
    simulator_output = await simulator(
            scenario=AdversarialScenario.ADVERSARIAL_IMAGE_UNDERSTANDING,
            max_conversation_turns=1,
            max_simulation_results=1,
            target=callback,
            api_call_retry_limit=3,
            api_call_retry_sleep_sec=1,
            api_call_delay_sec=30,
            concurrent_async_task=1,
        )

    print("\n===== Retrieved results for Simulator =======")
    
    file_name = "eval_sim_test.jsonl"

    # Write the output to the file
    with open(file_name, "w") as file:
        file.writelines([json.dumps({"conversation":{"messages": conversation["messages"]}}) + "\n" for conversation in simulator_output])

    # Evaluator simulator output
    protected_material_eval = ProtectedMaterialMultimodalEvaluator(azure_cred, project_scope)
    
    print("\n===== Running Evaluator with Simulation Datasets =======")
    # run the evaluation
    eval_output = evaluate(
        data=file_name,
        evaluation_name=f"e2e-sim-n-eval-image-understanding-{str(uuid.uuid4())}",
        azure_ai_project=project_scope,
        evaluators={"protected_material": protected_material_eval},
    )

    row_result_df = pd.DataFrame(eval_output["rows"])
    metrics = eval_output["metrics"]
    
    print("\n===== Printing Evaluation results =======")
    pprint(row_result_df)
    for col in row_result_df.columns:
        print(f"Column: {col}, Result: {row_result_df[col].values}")
    pprint(metrics)

    # Cleanup file
    os.remove(file_name)
    
async def main():
    await run_simulation()
    
if __name__ == "__main__":
    asyncio.run(main())