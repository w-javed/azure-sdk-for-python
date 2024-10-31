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
| Multi-modal Evaluators           | [Multi-modal Evaluators SDK](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_multimodal) |




### Clone the repository
```bash
git clone https://github.com/Azure/azure-sdk-for-python.git
git pull
git checkout users/w-javed/azure-sdk-for-python/Mult-modal-eval-Bug-Bash
```
