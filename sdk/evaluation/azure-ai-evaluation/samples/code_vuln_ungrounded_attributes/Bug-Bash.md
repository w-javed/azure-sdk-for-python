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

### 2. To checkout Bug Bash branch.
```bash
To pull latest code from the Bug bash branch.

git clone https://github.com/Azure/azure-sdk-for-python.git
cd azure-sdk-for-python
git pull
git remote add w-javed https://github.com/w-javed/azure-sdk-for-python.git
git remote -v
git fetch w-javed
git checkout -b BugBash_CodeVuln_UngroundedAttributes w-javed/BugBash_CodeVuln_UngroundedAttributes
cd sdk/evaluation/azure-ai-evaluation/samples/code_vuln_ungrounded_attributes
```

### 3. Install Azure AI Evaluation
```bash
pip install --upgrade git+https://github.com/Azure/azure-sdk-for-python.git@main#subdirectory=sdk/evaluation/azure-ai-evaluation
```


### 4. Running Code Vulnerability & Ungrounded Attributes Evaluator
```bash
python code_vuln_evaluator.py  
python ungrounded_attributes_evaluator.py
```

### 5. Running Evaluate API
```bash
python code_vuln_evaluate_api.py  
python ungrounded_attributes_evaluate_api.py
```

### 6. Simulations
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
ADO [link](https://msdata.visualstudio.com/Vienna/_workitems/create/Bug?templateId=d44a0102-a118-44ff-acfd-a3baf550ec0e&ownerId=8d25f9a6-0175-4ac6-8d4e-c1e2702a635c)

