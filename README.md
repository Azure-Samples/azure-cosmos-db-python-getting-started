---
services: cosmos-db
platforms: python
author: arramac
---

# Developing a Python app using Azure Cosmos DB
Azure Cosmos DB is Microsoft’s globally distributed multi-model database service. One of the supported APIs is the SQL API, which provides a JSON document model with SQL querying and JavaScript procedural logic. This sample shows you how to use the Azure Cosmos DB with the SQL API to store and access data from a Python application.

## Running this sample

* Before you can run this sample, you must have the following prerequisites:
    * [Visual Studio Code](https://code.visualstudio.com/)
    * [Python extention for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python#overview)
    * [Python 3.6](https://www.python.org/downloads/) with \<install location\>\Python36 and \<install location>\Python36\Scripts added to your PATH. 

* Then, clone this repository using: 
     `git clone https://github.com/Azure-Samples/azure-cosmos-db-python-getting-started.git`

* Next, substitute the endpoint and primary key in `CosmosGetStarted.py` with your Cosmos DB account's values. 

* In Visual Studio Code, select **View** > **Integrated terminal** to open the visual Studio Code integrated terminal.

* In the terminal, run ```python CosmosGetStarted.py.```

## About the code
The code included in this sample is intended to get you quickly started with a Python application that connects to Azure Cosmos DB with the SQL API.

## More information

- [Azure Cosmos DB](https://docs.microsoft.com/azure/cosmos-db/introduction)
- [Azure Cosmos DB: SQL API introduction](https://docs.microsoft.com/azure/cosmos-db/sql-api-introduction)
- [Azure Cosmos DB Python SDK Reference](https://docs.microsoft.com/azure/cosmos-db/sql-api-sdk-python)
