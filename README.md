# Kafka proto 
This repo contains a kafka producer for different type of proto files.
The data itself was taken from a kaggle competition.

## Getting started
You will need the following tools to get started:
* Python 3
* Installation of requirements.txt in a virtualenv
* Install docker and docker-compose
* Run docker-compose before starting

## Proto files
The following proto files are present
* etf.proto: A simple proto file with basic datatypes
* etf_complex.proto: A proto file with complex data types

## Running the program
The following script needs to be executed:
```python
.../kafka_proto_py/kafka_proto_api/start_producer.py
```
You will need to set the working directory to the root of the project