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

async def call_llm_image_generation(query: str) -> str:
    print("\n===== Generating Image =======")
    deployment = os.environ.get("AZURE_DEPLOYMENT_NAME_DALLE")
    endpoint = os.environ.get("AZURE_ENDPOINT_DALLE")
    
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_version=os.environ.get("AZURE_API_VERSION_DALLE"),
        api_key=os.environ["AZURE_OPENAI_API_KEY_DALLE"],
        # azure_ad_token_provider=token_provider,
    )
    
    print(f"\nImage Prompt: {query}")
    result = client.images.generate(
        model=deployment,
        prompt=query,
        n=1,
        # following headers are required for the LLM to by pass content filtering for harmful content.
        extra_headers={"x-policy-id-override": "annotate",
            "x-prompt-transformation-disabled": "true"}
    )

    image_url = json.loads(result.model_dump_json())['data'][0]['url']
    return image_url

async def callback(
    messages: List[Dict],
    stream: bool = False,
    session_state: Any = None,
    context: Optional[Dict[str, Any]] = None,
) -> dict:
    print("\n===== Callback is called via Simulation =======")
    image_gen_prompt = messages["messages"][0]["content"]
    image_url = await call_llm_image_generation(image_gen_prompt)
    print(f"\nImage URL: {image_url}")
    content = [
        {
            "type": "image_url",
            "image_url": {"url": image_url},
        }
    ]
    formatted_response = {"content": content, "role": "assistant"}
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

    # For LLM Dall-e-3 (Image generation)
    os.environ["AZURE_DEPLOYMENT_NAME_DALLE"] = "Dalle3"
    os.environ["AZURE_ENDPOINT_DALLE"] = "https://roaroai.openai.azure.com/"
    os.environ["AZURE_API_VERSION_DALLE"] = "2024-05-01-preview"
    os.environ["AZURE_OPENAI_API_KEY_DALLE"] = ""
    
    azure_cred = DefaultAzureCredential()
    project_scope = {
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
        "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
        "project_name": os.environ.get("AZURE_PROJECT_NAME"),
    }

    print("\n===== Initializing Adversarial Simulator =======")            
    simulator = AdversarialSimulator(azure_ai_project=project_scope, credential=azure_cred)

    print("\n===== Running Adversarial Simulator for Image Understanding =======")     
    image_gen_outputs = await simulator(
        scenario=AdversarialScenario.ADVERSARIAL_IMAGE_GEN,
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
        file.writelines([json.dumps({"conversation":{"messages": conversation["messages"]}}) + "\n" for conversation in image_gen_outputs])

    # Evaluator simulator output
    protected_material_eval = ProtectedMaterialMultimodalEvaluator(azure_cred, project_scope)
    
    print("\n===== Running Evaluator with Simulation Datasets =======")
    # run the evaluation
    eval_output = evaluate(
        data=file_name,
        evaluation_name=f"e2e-sim-n-eval-image-gen-{str(uuid.uuid4())}",
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