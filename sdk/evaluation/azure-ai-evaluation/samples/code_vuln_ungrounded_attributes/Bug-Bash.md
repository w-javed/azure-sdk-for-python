## Welcome to Bug Bash for Azure AI Evaluation SDK 

### Prerequisites
- Azure AI Project in `eastus2` region. It is used to get token/credential to call Evaluation service. 

### Resources

If you do not have the required resources, please use the following resources:


| Resource Type     | Resource Name                                                                                                                                                                                                                                                                  |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Project           | [hancwang-eus2-0339](https://ai.azure.com/build/evaluation?wsid=/subscriptions/b17253fa-f327-42d6-9686-f3e553e24763/resourceGroups/hanchi-test/providers/Microsoft.MachineLearningServices/workspaces/hancwang-eus2-0339&tid=72f988bf-86f1-41af-91ab-2d7cd011db47) |


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
pip install --upgrade git+https://github.com/Azure/azure-sdk-for-python.git@main#subdirectory=sdk/evaluation/azure-ai-evaluation
```

### Running Code Vulnerability & Ungrounded Attributes Evaluator
```bash
python code_vuln_evaluator.py  
python ungrounded_attributes_evaluator.py
```

### Running Evaluate API
```bash
python code_vuln_evaluate_api.py  
python ungrounded_attributes_evaluate_api.py
```

### Simulations
```bash
python code_vuln_simulation.py
python ungrounded_att_simulation.py
```


### Azure AI project

Please select or create a new project in `EastUS2` region, and set the following values in env variable. 

```bash
os.environ["AZURE_SUBSCRIPTION_ID"] = ""
os.environ["RESOURCE_GROUP"] = ""
os.environ["PROJECT_NAME"] = ""
```

### Possible use cases to test.
- Find zip file that contains test data for Code Vulnerability. 
    codevuln_test-data.jsonl.zip

- Find zip file that contains test data for Ungrounded Attributes. 
    ungrounded_attributes_test_data.zip

Please create a bug/task for any issue you encounter during bug bash using following link. Thanks!
ADO [link](https://msdata.visualstudio.com/Vienna/_workitems/edit/3299596/)

