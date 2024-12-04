## Bug Bash for Adversarial Simulator for Image Understanding and Image Generation.

Azure AI Evaluation SDK now supports multi-modal (text+image based) evaluators. 

Following are the evaluators has been introduced. 

# Multi-modal Evaluators

Evaluator Name | Link 
--- | --- 
ContentSafetyMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_content_safety_multimodal.py#L21) 
ViolenceMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_violence.py#L11) 
SexualMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_sexual.py#L11)
SelfHarmMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_self_harm.py#L11)
HateUnfairnessMultimodalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_hate_unfairness.py#L11) 
ProtectedMaterialMultiModalEvaluator | [link](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal/_protected_material.py) 


## Adversarial Image Scenarios

The AdversarialSimulator supports a range of scenarios, hosted in the service, to simulate against your target application or function. For multi-modal support, the following adversarial scenario enums are now supported:

Scenario | Description | Datasets
--- | --- | ---
Image Understanding | Input: Text+Image Output: Text | In this scenario, the Adversarial Simulator provides a combination of multi-modal harmful text + image(s) prompt, which can be used in your GenAI application to understand the input. The Simulator expects that an assistant message (a response from GenAI app) is added in the conversation in callback function.
Image Generation | Input: Text Output: Image(s) | In this scenario the Adversarial Simulator provides harmful text prompts, which can be used in your GenAI application or LLMs to generate image(s) and use these Text + Image prompts for evaluation purposes. Simulator expects an assistant message with image(s) to be added in the conversation within the callback function. 

Please follow detailed documentation [here](https://docs.aml-babel.com/tools/azure-ai-evaluation/#adversarial-simulator-for-image-multi-modal-use-cases)


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
pip install "git+https://github.com/Azure/azure-sdk-for-python.git@main#egg=azure-ai-evaluation&subdirectory=sdk/evaluation/azure-ai-evaluation"
```

To pull latest from the working branch. 
```bash
git clone https://github.com/Azure/azure-sdk-for-python.git
git pull
git remote add w-javed https://github.com/w-javed/azure-sdk-for-python.git
git remote -v
git fetch w-javed
git checkout -b Multi-modal-eval-Bug-Bash w-javed/Multi-modal-eval-Bug-Bash
```

### Running Content Safety Evaluator
```bash
python e2e_simulation_eval_multi_modal_image_understanding.py 
python e2e_simulation_eval_multi_modal_image_generation.py  
```


Please create a bug/task for any issue you encounter during bug bash using following link. Thanks!
ADO [link](https://msdata.visualstudio.com/Vienna/_workitems/edit/3299596/)

Link to this page [here](https://github.com/w-javed/azure-sdk-for-python/blob/Multi-modal-eval-Bug-Bash/sdk/evaluation/azure-ai-evaluation/samples/multi-modal-evals/multimodal-eval-bug-bash.md)
