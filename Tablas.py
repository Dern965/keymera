import boto3

# Configuración de DynamoDB local
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='fakeMyKeyId', aws_secret_access_key='fakeSecretAccessKey')

# Crear tabla Empenos
try:
    empenos_table = dynamodb.create_table(
        TableName='Empenios',
        KeySchema=[
            {
                'AttributeName': 'Num_Empenio',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Categoria',
                'KeyType': 'RANGE'  # Clave de ordenamiento
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Num_Empenio',
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
    print("Tabla 'Empenios' creada.")
except dynamodb.meta.client.exceptions.ResourceInUseException:
    print("La tabla 'Empenios' ya existe.")

# Crear tabla Ventas
try:
    ventas_table = dynamodb.create_table(
        TableName='Ventas',
        KeySchema=[
            {
                'AttributeName': 'Num_Venta',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Fecha_venta',
                'KeyType': 'RANGE'  # Clave de ordenamiento
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Num_Venta',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'Fecha_venta',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    ventas_table.wait_until_exists()
    print("Tabla 'Ventas' creada.")
except dynamodb.meta.client.exceptions.ResourceInUseException:
    print("La tabla 'Ventas' ya existe.")