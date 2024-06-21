import boto3

# Configurar el cliente de DynamoDB local
dynamodb_client = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='fakeMyKeyId', aws_secret_access_key='fakeSecretAccessKey')

# Nombre de la tabla a borrar
table_name = 'Transacciones'

# Borrar la tabla usando delete_table
try:
    response = dynamodb_client.delete_table(TableName=table_name)
    print(f"Tabla '{table_name}' borrada exitosamente.")
except Exception as e:
    print("Error al borrar la tabla:", e)
