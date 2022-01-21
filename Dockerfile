FROM continuumio/miniconda3

# Note: 
# The container created with this image will not work with Estimator object. To create a fully custom container uncomment the 2 lines at the bottom of this file and use appropriate model file name instead of model.py
# This container can be used with SKLearn estimator and processing objects

ADD environment.yml /tmp/environment.yml
ADD model.py /tmp/model.py

# required files for sagemaker-training
RUN apt-get update
RUN apt-get install gcc libc-dev g++ libffi-dev libxml2 libffi-dev unixodbc-dev -y

# install dependencies in base environment stick to python 3.8 since 3.10 has issues with sagemaker-training
RUN deactivate
RUN conda env update --file /tmp/environment.yml -n base

# ----------- Fully custom container ----------- #
## Make sure to use  #!/usr/bin/env python at the top of model file to make it executable LAS page 273
# COPY model.py /usr/bin/train
# RUN chmod 755 /usr/bin/train