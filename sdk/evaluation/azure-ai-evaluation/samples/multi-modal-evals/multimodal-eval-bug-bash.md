## Welcome to Bug Bash for Azure AI Evaluation SDK Multimodal support

Azure AI Evaluation SDK supported conversation using text as an Input and text as an output. 

At Ignite we are introducing new evaluators for Content Safety and Protected Material to evaluate Text + Image. 

These are service based evaluators which means SDK calls Evaluation Service for evaluation of content harm and protected material. 

### Prerequisites
- Azure AI Project in `EastUS2` region. It is used to get token/credential to call Evaluation service. 

### Resources

If you do not have the required resources, please use the following resources:

| Resource Type     | Resource Name                                                                                                                                                                                                                                                                  |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Project           | [ignite-multimodal-eval-project](https://ai.azure.com/build/overview?wsid=/subscriptions/b17253fa-f327-42d6-9686-f3e553e24763/resourceGroups/hanchi-test/providers/Microsoft.MachineLearningServices/workspaces/ignite-multimodal-eval-project&tid=72f988bf-86f1-41af-91ab-2d7cd011db47) |
| Multi-modal Evaluators           | [SDK Code](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal) |

### Multi-modal Use Cases

Use cases | Input | Output | Notes
--- | --- | --- | --- 
Visual QnA | Text + Image  | Text 
Image only prompts | Image | Text 
Image Generation | Text | Image 
Text + Image Generation | Text | Text + Image

# Multi-modal Evaluators

Evaluator Name | Link 
--- | --- 
ContentSafetyMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_content_safety_multimodal.py#L21) 
ViolenceMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_violence.py#L11) 
SexualMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_sexual.py#L11)
SelfHarmMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_self_harm.py#L11)
HateUnfairnessMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_hate_unfairness.py#L11) 
ProtectedMaterialMultiModalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_protected_material.py) 

## Instructions:

### 1. Setup Virtualenv 

##### Recommended path: 
`python3 -m venv .bugbashenv`

##### Linux based:
`source .bugbashenv/bin/activate`
##### Windows:
`.bugbashenv\Scripts\activate`

### 2. Install Azure AI Evaluation
```bash
pip install promptflow-azure
pip install azure-ai-evaluation
```
or 
```bash
pip install azure-ai-evaluation[remote]
```
Above statement installs dependencies such as promptflow-azure, azure-identity etc.

### Running Content Safety Evaluation
```bash
python content_safety_multimodal_evaluator.py  
python content_safety_multimodal_evaluate_api.py
```

### Azure AI project

Please select or create a new project in `EastUS2` region, and set the following values in env variable. 

```bash
os.environ["AZURE_SUBSCRIPTION_ID"] = ""
os.environ["RESOURCE_GROUP"] = ""
os.environ["PROJECT_NAME"] = ""
```


Link to this page [here](https://github.com/w-javed/azure-sdk-for-python/blob/Multi-modal-eval-Bug-Bash/sdk/evaluation/azure-ai-evaluation/samples/multi-modal-evals/multimodal-eval-bug-bash.md)
