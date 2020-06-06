from azure.cosmos import exceptions, CosmosClient, PartitionKey
import family

# Initialize the Cosmos client
endpoint = "endpoint"
key = 'primary_key'

#region Create Cosmos Client
client = CosmosClient(endpoint, key)
#endregion

# Create a database
#region Create a Database
database_name = 'AzureSampleFamilyDatabase'
database = client.create_database_if_not_exists(id=database_name)
#endregion

# Create a container
# Using a good partition key improves the performance of database operations.
# See detailed documentation on partition keys here:
# https://docs.microsoft.com/en-us/azure/cosmos-db/partitioning-overview

#region Create Container if doesn't exist
container_name = 'FamilyContainer'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/lastName"),
    offer_throughput=400
)
#endregion

# Reconnecting to Azure Cosmos DB after creating database and container
# example of how to connect to existing database and container
# without creating a new database and container
#region Reconnection
client = CosmosClient(endpoint, key)
database = client.get_database_client(database=database_name)
container = database.get_container_client(container=container_name)
#endregion

# Add items to the container
family_items_to_create = [family.get_andersen_family_item(), 
    family.get_johnson_family_item(), 
    family.get_smith_family_item(), 
    family.get_wakefield_family_item()]

#region Create Items
for family_item in family_items_to_create:
    container.create_item(body=family_item)
#endregion

# Read items (key value lookups by partition key and id, aka point reads)
#region Read Item
for family in family_items_to_create:
    item_response = container.read_item(item=family['id'], partition_key=family['lastName'])
    request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
    print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
#endregion

# Query these items using the SQL query syntax. 
# Specifying the partition key value in the query allows Cosmos DB 
# to retrieve data only from the relevant partitions, which improves performance
# Detailed Documentation here: https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-getting-started
#region Query items by Partition key
query = "SELECT * FROM f WHERE f.lastName IN ('Wakefield', 'Andersen')"

items = list(container.query_items(
    query = query,
    enable_cross_partition_query = True
))

request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
#endregion

# Query these items using non partition key
# While performance is improved by using Partition key
# Cosmos DB doesn't require this and considered a feature of the product
#region Query items by non partition key
query = "SELECT * FROM f WHERE f.district = 'WA5' AND f.address.state = 'WA'"

items = list(container.query_items(
    query = query,
    enable_cross_partition_query = True
))

request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
#endregion

# Update Item
# Updating item is simple as modifying resulting dict() and passing it back
# Please note Cosmos does not support partial updates so make sure variable contains full item before updating
# Update family returned from last query
#region Update record
item = items[0] #query items come back as list of dictionary so putting into seperate dictionary for ease
item['children'] = [{'firstname': 'Liam', 'grade': 1}, {'firstname':'Emma','grade': 5, 'biketoschool': True}]
result = container.upsert_item(item) #Cosmos will return updated item

request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

print(f'Update completed and consumed {request_charge} request units')
#endregion

# Delete Item
# Deleting item requires passing in full item and partition key which in this example
# is lastname (see line 27)
#region Delete Item and confirm
query = "SELECT * FROM f WHERE f.lastname = 'Johnson' AND f.registered = false"

items = list(container.query_items(
    query = query,
    enable_cross_partition_query = True
))

container.delete_item(
    item = items[0] #First item in list
    partition_key = items[0]['lastname']
)

request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

print(f'Delete completed and consumed {request_charge} request units')

# Prove that delete was completed
query = "SELECT * FROM f WHERE f.lastname = 'Johnson' AND f.registered = false"

items = list(container.query_items(
    query = query,
    enable_cross_partition_query = True
))

request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

if not items: #Empty list
    print(f'Confirmed Item deleted and query consumed {request_charge} request units')

#endregion