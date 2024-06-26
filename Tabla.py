import boto3

# Configuración de DynamoDB local
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='fakeMyKeyId', aws_secret_access_key='fakeSecretAccessKey')

# Crear tabla Transacciones
try:
    empenos_table = dynamodb.create_table(
        TableName='Transacciones',
        KeySchema=[
            {
                'AttributeName': 'Num_Transaccion',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Categoria',
                'KeyType': 'RANGE'  # Clave de ordenamiento
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Num_Transaccion',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'Categoria',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    empenos_table.wait_until_exists()
    print("Tabla 'Transacciones' creada.")
except dynamodb.meta.client.exceptions.ResourceInUseException:
    print("La tabla 'Transacciones' ya existe.")