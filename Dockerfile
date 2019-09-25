FROM python:3
ADD src /canary/src
ADD ./requirements.txt /canary
RUN pip install -r /canary/requirements.txt
RUN echo 'alias canary="python canary/src/canary.py "' >> ~/.bashrc

## Build Canary Docker Image
# docker build -t canary-beta .

## Create Docker instance and mount Users Home Directory
# docker run -v ~/canary:/root/canary --name canary -i -t canary-beta bash

# Run Canary
# canary -u "https://www.google.com" -t scrape