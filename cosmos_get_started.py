from azure.cosmos.aio import CosmosClient as cosmos_client
from azure.cosmos import PartitionKey, exceptions
import asyncio
import family

# <add_uri_and_key>
endpoint = "<Your Cosmos DB Resource URI>"
key = "<Your Cosmos DB Resource PRIMARY KEY>"
# </add_uri_and_key>


# <define_database_and_container_name>
database_name = 'AzureSampleFamilyDatabase'
container_name = 'FamilyContainer'
# </define_database_and_container_name>

# <create_database_if_not_exists>
async def get_or_create_db(client, database_name):
    try:
        database_obj  = client.get_database_client(database_name)
        await database_obj.read()
        return database_obj
    except exceptions.CosmosResourceNotFoundError:
        print("Creating database")
        return await client.create_database(database_name)
# </create_database_if_not_exists>
    
# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
async def get_or_create_container(database_obj, container_name):
    try:        
        todo_items_container = database_obj.get_container_client(container_name)
        await todo_items_container.read()   
        return todo_items_container
    except exceptions.CosmosResourceNotFoundError:
        print("Creating container with lastName as partition key")
        return await database_obj.create_container(
            id=container_name,
            partition_key=PartitionKey(path="/lastName"),
            offer_throughput=400)
    except exceptions.CosmosHttpResponseError:
        raise
# </create_container_if_not_exists>
    
# <method_populate_container_items>
async def populate_container_items(container_obj, items_to_create):
    # Add items to the container
    family_items_to_create = items_to_create
    # <create_item>
    for family_item in family_items_to_create:
        inserted_item = await container_obj.create_item(body=family_item)
        print("Inserted item for %s family. Item Id: %s" %(inserted_item['lastName'], inserted_item['id']))
    # </create_item>
# </method_populate_container_items>


# <method_read_items>
async def read_items(container_obj, items_to_read):
    # Read items (key value lookups by partition key and id, aka point reads)
    # <read_item>
    for family in items_to_read:
        item_response = await container_obj.read_item(item=family['id'], partition_key=family['lastName'])
        request_charge = container_obj.client_connection.last_response_headers['x-ms-request-charge']
        print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
    # </read_item>
# </method_read_items>

# <method_query_items>
async def query_items(container_obj, query_text):
    # enable_cross_partition_query should be set to True as the container is partitioned
    # In this case, we do have to await the asynchronous iterator object since logic
    # within the query_items() method makes network calls to verify the partition key
    # definition in the container
    # <query_items>
    query_items_response = container_obj.query_items(
        query=query_text,
        enable_cross_partition_query=True
    )
    request_charge = container_obj.client_connection.last_response_headers['x-ms-request-charge']
    items = [item async for item in query_items_response]
    print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
    # </query_items>
# </method_query_items>

# <run_sample>
async def run_sample():
    # <create_cosmos_client>
    async with cosmos_client(endpoint, credential = key) as client:
    # </create_cosmos_client>
        try:
            # create a database
            database_obj = await get_or_create_db(client, database_name)
            # create a container
            container_obj = await get_or_create_container(database_obj, container_name)
            # generate some family items to test create, read, delete operations
            family_items_to_create = [family.get_andersen_family_item(), family.get_johnson_family_item(), family.get_smith_family_item(), family.get_wakefield_family_item()]
            # populate the family items in container
            await populate_container_items(container_obj, family_items_to_create)  
            # read the just populated items using their id and partition key
            await read_items(container_obj, family_items_to_create)
            # Query these items using the SQL query syntax. 
            # Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
            query = "SELECT * FROM c WHERE c.lastName IN ('Wakefield', 'Andersen')"
            await query_items(container_obj, query)                 
        except exceptions.CosmosHttpResponseError as e:
            print('\nrun_sample has caught an error. {0}'.format(e.message))
        finally:
            print("\nQuickstart complete")
# </run_sample>

# <python_main>
if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_sample())
# <python_main>

    











