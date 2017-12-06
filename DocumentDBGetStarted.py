import pydocumentdb;
import pydocumentdb.document_client as document_client

config = { 
    'ENDPOINT': 'https://FILLME.documents.azure.com',
    'MASTERKEY': 'FILLME',
    'SQL_DATABASE': 'db',
    'SQL_COLLECTION': 'coll'
};

# Initialize the Python client
client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})

# Create a database
db = client.CreateDatabase({ 'id': config['SQL_DATABASE'] })

# Create collection options
options = {
    'offerEnableRUPerMinuteThroughput': True,
    'offerVersion': "V2",
    'offerThroughput': 400
}

# Create a collection
collection = client.CreateCollection(db['_self'], { 'id': config['SQL_COLLECTION'] }, options)

# Create some documents
document1 = client.CreateDocument(collection['_self'],
    { 
        'id': 'server1',
        'Web Site': 0,
        'Cloud Service': 0,
        'Virtual Machine': 0,
        'name': 'some' 
    })

document2 = client.CreateDocument(collection['_self'],
    { 
        'id': 'server2',
        'Web Site': 1,
        'Cloud Service': 0,
        'Virtual Machine': 0,
        'name': 'some' 
    })

# Query them in SQL
query = { 'query': 'SELECT * FROM server s' }    
        
options = {} 
options['enableCrossPartitionQuery'] = True
options['maxItemCount'] = 2

result_iterable = client.QueryDocuments(collection['_self'], query, options)
results = list(result_iterable);

print(results)
