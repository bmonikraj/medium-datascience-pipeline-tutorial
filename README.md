# medium-ds-pipeline-tutorial
Data science production pipeline tutorial 

--------------------------------------------------------------------------------------------------------------

## Note 
1. This tutorial assumes that you have basic knowledge of Python, websockets and sklearn (Basic ML with classification using GaussianNB model for binary classification). It assumes that you understand the code base (which has been kept as simple as possible). For further understanding, please refer #4 in current 'Note' section. 
2. The whole communication between services happend using MQ broker RabbitMQ. You can use something else, if you are familiar with, by changing protocol and dependencies. 
3. You can clone the repository for a Quick Start on this tutorial
4. For any **queries, discussions and ideas, please feel free to drop a mail at [bmonikraj@gmail.com]** 

--------------------------------------------------------------------------------------------------------------

## Data information 
at http://archive.ics.uci.edu/ml/datasets/connectionist+bench+(sonar,+mines+vs.+rocks) 

--------------------------------------------------------------------------------------------------------------

## Idea and KT for running below scripts and deployment design
- The artifacts of the projects are => { clf_model.sav, **predictor.py** } , { **service.py** } 
- The testing script of the project is => { client.py }
- Install all the dependencies of the project before running any script, **on individual target system** => Quick Note : If you have latest Anaconda version of python installed (3.6+ Py), then you only need to install *pika*
- Make sure to have data file in the same directory as of trainer.py => Also available in the repository
- You will need RabbitMQ to use this tutorial. You can install locally or use CloudAMQ free service for the purpose => Once you have the *Connection URL String* of rabbitMq, put (at RABBITMQ_CONN) them in files { predictor.py, service.py } 
- Once the training is complete by running command mentioned below in **#1** and clf_model.sav is generated, { clf_model.sav, predictor.py } should be residing in same directory and can be treated as one **logical deployment unit (LDU 1)**, with their required dependencies, as mentioned in trainer.py and predictor.py installed
- After installing dependencies of service.py, this can be treated as another **logical deployment unit (LDU 2)**.
- We can run **(LDU 1)** by taking care of above mentioned pre-requisite and running command mentioned below in **#2**
- We can run **(LDU 2)** by taking care of above mentioned pre-requisite and running command mentioned below in **#3**
- We can test by running command mentioned below in **#4**. The test data is hard-coded in the client.py file. You can change accordingly. 

--------------------------------------------------------------------------------------------------------------

## Commands for running individual script = 
1. Running ```trainer``` 

   ```python trainer.py``` -> This will save ```clf_model.sav``` in the same directory as of *trainer.py*
   The clf_model.sav file is the artifact which must be kept in the same directory as of *predictor.py* file.
   
2. Running ```predictor```

   ```python predictor.py``` -> This will run the predictor application
   
3. Running ```service```

   ```python service.py``` -> This will run the service application, a Websocket application which acts in async mode with respective client
   
4. Running ```client```

   ```python client.py <host_of_ws_server>:<port>``` -> This will run a simple websocker based client which will connect to given websocket server (should connect to accessible ```service``` instance), send test data and receive it's response
   
--------------------------------------------------------------------------------------------------------------

