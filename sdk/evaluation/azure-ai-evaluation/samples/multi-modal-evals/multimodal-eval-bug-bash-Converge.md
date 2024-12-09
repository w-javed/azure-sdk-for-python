## Welcome to Bug Bash for Azure AI Evaluation SDK for Multimodal

Earlier Azure AI Evaluation SDK supported text based evaluators. Now, we are introducing new evaluators to evaluate Text + Images (In Preview)

Following are the evaluators has been introduced. 
Content Safety (Self-harm, Violence, Sexual, Hate-Unfairness) and Protected Material. Since they are pub preview, we have marked them as @experimental that prints a following messages whenever used. 

<i>"This is an experimental class, and may change at any time. Please see https://aka.ms/azuremlexperimental for more information." </i>

These are service based evaluators that calls [Evaluation Service](https://msdata.visualstudio.com/Vienna/_git/vienna?path=%2Fsrc%2Fazureml-api%2Fsrc%2FRAISvc%2FAnnotation%20submission%20and%20retrieval.ipynb&_a=preview) for evaluation of content harm and protected material. 

### Prerequisites
- Azure AI Project in `eastus2` region. It is used to get token/credential to call Evaluation service. 

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
pip install "git+https://github.com/Azure/azure-sdk-for-python.git@main#egg=azure-ai-evaluation&subdirectory=sdk/evaluation/azure-ai-evaluation"
```
or 
```bash
pip install azure_ai_evaluation-1.1.0-py3-none-any.whl    
```
Other related dependencies are promptflow-azure, azure-identity, azure-cli etc.

To pull latest from the working branch. 
```bash
git clone https://github.com/Azure/azure-sdk-for-python.git
git cd sdk/evaluation/azure-ai-evaluation
git pull
git remote add w-javed https://github.com/w-javed/azure-sdk-for-python.git
git remote -v
git fetch w-javed
git checkout -b Multi-modal-eval-Bug-Bash w-javed/Multi-modal-eval-Bug-Bash
```

### Running Content Safety Evaluator
```bash
cd samples/multi-modal-evals/evals
python content_safety_multimodal_evaluator.py  
python content_safety_multimodal_evaluator_b64_images.py
python self_harm_multimodal_evaluator.py
```

### Running Evaluate API
```bash
python content_safety_multimodal_evaluate_api.py
python content_safety_multimodal_evaluate_api_target.py
```
Python scripts folder - [link](https://github.com/w-javed/azure-sdk-for-python/tree/Multi-modal-eval-Bug-Bash/sdk/evaluation/azure-ai-evaluation/samples/multi-modal-evals)

### Azure AI project

Please select or create a new project in `EastUS2` region, and set the following values in env variable. 

```bash
os.environ["AZURE_SUBSCRIPTION_ID"] = ""
os.environ["RESOURCE_GROUP"] = ""
os.environ["PROJECT_NAME"] = ""
```

### Possible use cases to test.
1. Modify messages payload with different text + image combination in user/assistant messages, and verify results. 
2. Provide text + images in user messages and verify results (image understanding).
3. Provide text + images in assistant messages and verify results (image gen use case).
2. Provide different image url links and verify results. 
3. Provide different images from local folder.


### Few known issues (Work in progress)
1. UI is not able to render conversation (messages[]) payload from the evaluation results uploaded by SDK to the project.

Please create a bug/task for any issue you encounter during bug bash using following link. Thanks!
ADO [link](https://msdata.visualstudio.com/Vienna/_workitems/edit/3299596/)

Link to this page [here](https://github.com/w-javed/azure-sdk-for-python/blob/Multi-modal-eval-Bug-Bash/sdk/evaluation/azure-ai-evaluation/samples/multi-modal-evals/multimodal-eval-bug-bash.md)
