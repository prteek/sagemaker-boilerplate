# sagemaker-boilerplate
Data science experiments using Sagemaker  

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/prteek/sagemaker-boilerplate/HEAD)

This repo is an exercise in using both Cloud tools to quickly iterate and prototype on ML problem and well as demonstrating a logical approach to ML problem solving

### Setup 
Make sure you're using virtual environment

```shell
python3 -m pip install -r requirements.txt
```

Create a ```local_credentials.env``` file (do not share it or add to git or push to ECR) which should look something like below but with your own credentials:

---
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE  
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY  
AWS_DEFAULT_REGION=eu-west-1  
SAGEMAKER_EXECUTION_ROLE=arn:aws:iam::432123456789:role/service-role/AmazonSageMaker-ExecutionRole-20210330T123456)

---
    
    (Additionally for above you can setup AWS credentials in cli)

Although the process can be accomplished locally it would be best to use AWS for data storage and training.
Setup on AWS requires:
1. An appropriate Role which can read/write to s3 and launch training/hpo jobs on sagemaker
2. An s3 bucket exclusively for the project
3. AWS cli configure with a profile 'personal' to use Makefile automations
4. Use the following make commands to setup AWS (first change REPO name and region at the top of Makefile and ensure step 3 is done)

```shell
make create-ecr-repo # This will create an ECR repo to work with Sagemaker

make all # This will build and push your image to ECR to be later used by Sagemaker (make a note of image URI and use it wherever required)

make create-bucket # This will create an s3 bucket with the name specified as REPO in Makefile (keep using this bucket name wherever required)
```

### Data file
```transfusion.data```


### Train a model
There are many model specific files that can generate ML model by training either locally or in Sagemaker.  
The helper ```lab.py``` can be used to start training using any model file (model.py, non_linear_model.py)



### Read the report.md
There is a small analysis (in progress) that highlights a mothodical approach to modelling and EDA. You can read `report.md` and feel free to drop any feedback you may have.
