import azure.cosmos.cosmos_client as cosmos_client

config = {
    'ENDPOINT': 'FILLME',
    'PRIMARYKEY': 'FILLME',
    'DATABASE': 'CosmosDatabase',
    'CONTAINER': 'CosmosContainer'
}

# Initialize the Cosmos client
client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                    'masterKey': config['PRIMARYKEY']})

# Create a database
db = client.CreateDatabase({'id': config['DATABASE']})

# Create container options
options = {
    'offerThroughput': 400
}

container_definition = {
    'id': config['CONTAINER']
}

# Create a container
container = client.CreateContainer(db['_self'], container_definition, options)

# Create and add some items to the container
item1 = client.CreateItem(container['_self'], {
    'id': 'server1',
    'Web Site': 0,
    'Cloud Service': 0,
    'Virtual Machine': 0,
    'message': 'Hello World from Server 1!'
}
)

item2 = client.CreateItem(container['_self'], {
    'id': 'server2',
    'Web Site': 1,
    'Cloud Service': 0,
    'Virtual Machine': 0,
    'message': 'Hello World from Server 2!'
}
)

# Query these items in SQL
query = {'query': 'SELECT * FROM server s'}

options = {}
options['enableCrossPartitionQuery'] = True
options['maxItemCount'] = 2

result_iterable = client.QueryItems(container['_self'], query, options)
for item in iter(result_iterable):
    print(item['message'])
