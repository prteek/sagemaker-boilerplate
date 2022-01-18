FROM python:3.8
# Note: 
# The container created with this image will not work with Estimator object. To create a fully custom container uncomment the 3 lines at the bottom of this file and use appropriate model file name.
# This container can be used with SKLearn estimator and processing objects

ADD requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt
RUN pip3 install --no-cache sagemaker-training


# ----------- Fully custom container ----------- #
## Make sure to use  #!/usr/bin/env python at the top of model file to make it executable LAS page 273

# COPY model.py /usr/bin/train
# RUN chmod 755 /usr/bin/train
