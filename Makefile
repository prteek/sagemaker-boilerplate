REPO=sagemaker-boilerplate
REGION=eu-west-1

# ----------------------------------------------- #
ACCOUNT_ID=$(shell aws sts get-caller-identity --profile personal --query Account --output text)
IMAGE=$(REPO):latest
IMAGE_ID=$(shell docker images -q $(IMAGE))

help:
	@echo " - setup         	: Install requirements and dl4 library"
	@echo " - create-ecr-repo	: Creates repo in ECR with same name as REPO in Makefile"
	@echo " - create-bucket		: Creates s3 bucket with the same name as REPO in Makefile"
	@echo " - build-container	: Build container using Dockerfile for Sagemaker processing"
	@echo " - tag-image     	: Tag the last built image to latest version"
	@echo " - push-image     	: Push latest tagged image to ECR"
	@echo " - all           	: build-tag-push"


create-ecr-repo:
	aws ecr create-repository --repository-name $(REPO) --region $(REGION) --profile personal

create-bucket:
	aws s3api create-bucket --bucket $(REPO) --region $(REGION) --profile personal --create-bucket-configuration LocationConstraint=$(REGION)

build-container:
	docker build -t $(IMAGE) -f Dockerfile .


tag-image:
	docker tag $(IMAGE_ID) $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(IMAGE)


# First get login id password for AWS account and then push image
push-image:
	aws ecr get-login-password --region $(REGION) --profile personal | docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(IMAGE);docker push $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(IMAGE)


all: build-container tag-image push-image

