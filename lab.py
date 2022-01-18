import os
from dotenv import load_dotenv
from sagemaker.sklearn import SKLearn
from smexperiments.experiment import Experiment
from smexperiments.trial import Trial
from smexperiments.tracker import Tracker
from datetime import datetime
from sagemaker.session import Session
from sagemaker.utils import S3_PREFIX

load_dotenv("local_credentials.env")


bucket = 'sagemaker-boilerplate'
image_uri = '434616802091.dkr.ecr.eu-west-1.amazonaws.com/sagemaker-boilerplate'
role = os.environ['SAGEMAKER_EXECUTION_ROLE']
session = Session(default_bucket=bucket)

# Upload data
data_dir = session.upload_data('transfusion.data', bucket=bucket, key_prefix='data')
training_dir = "/".join(i for i in data_dir.split("/")[:-1])


# Configure estimator
job_name = 'training'
output_path = f"s3://{bucket}/model/"
hyperparameters = {'alpha': 0.1}

metrics = [{'Name': 'accuracy', 'Regex': "accuracy=([0-9\\.]+);"}]

estimator = SKLearn(entry_point='model.py',
                    image_uri=image_uri,
                    role=role,
                    instance_type='ml.m5.large',
                    instance_count=1,
                    output_path=output_path,
                    use_spot_instances=True,
                    base_job_name=job_name,
                    metric_definitions=metrics,
                    max_wait=100000,
                    hyperparameters=hyperparameters,
                   )

# Setup experiment and trial
experiment_name = 'sagemaker-boilerplate'
description = 'Setup template trials for easy experimentation'
try:
    experiment = Experiment.create(experiment_name=experiment_name, 
                              description=description)
except:
    print("Experiment exists")
    experiment = Experiment.load(experiment_name=experiment_name)
    


trial_name = "check-for-output-location"
trial = Trial.create(experiment_name=experiment.experiment_name,
                    trial_name=trial_name)

with Tracker.create(display_name='metadata', 
                    artifact_bucket=bucket, 
                    artifact_prefix='metadata') as tracker:
    tracker.log_parameters({'bucket':bucket, 'metrics':'accuracy'})
    tracker.log_artifact('Dockerfile', name='dockerfile')
    tracker.log_artifact('requirements.txt', name='requirements-file')
    
trial.add_trial_component(tracker.trial_component)

experiment_config = {"ExperimentName": experiment.experiment_name,
                     "TrialName": trial.trial_name,
                     "TrialComponentDisplayName": job_name}

estimator.fit({'training':training_dir}, experiment_config=experiment_config)

