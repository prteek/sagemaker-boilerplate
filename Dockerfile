FROM continuumio/miniconda3

ADD environment.yml /tmp/environment.yml
ADD model.py /tmp/model.py

# required files for sagemaker-training
RUN apt-get update
RUN apt-get install gcc libc-dev g++ libffi-dev libxml2 libffi-dev unixodbc-dev -y

# install dependencies in 'base' environment because sagemaker-training uses it to invoke entrypoint
# stick to python 3.8 in environment.yml since 3.10 has issues with sagemaker-training

RUN conda env update --name base --file /tmp/environment.yml
