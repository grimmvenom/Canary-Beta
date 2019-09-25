FROM python:3
ADD src /
ADD ./requirements.txt /
RUN pip install -r /requirements.txt

## Build Canary Docker Image
# docker build -t canary-beta .

## Option 1:
## Create Docker instance and mount Users Home Directory
# docker run -v ~/canary:/root/canary --name canary -i -t canary-beta bash

## Option2:
## Create a canary docker instance from newly created docker image
# docker create -it --name canary canary-beta
## Start canary instance
# docker start canary
## Run canary instance in interactive mode
# docker exec -it canary bash