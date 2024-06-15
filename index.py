import boto3
from botocore.exceptions import ClientError
import tkinter as tk
from tkinter import messagebox

# Configuración de DynamoDB Local
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://localhost:8000",
    region_name="us-west-2",
    aws_access_key_id="fakeMyKeyId",
    aws_secret_access_key="fakeSecretAccessKey"
)

# Crear tabla (si no existe)
try:
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.wait_until_exists()
except ClientError as e:
    if e.response['Error']['Code'] != 'ResourceInUseException':
        raise

table = dynamodb.Table('Users')

def insert_user():
    username = entry_username.get()
    age = entry_age.get()
    try:
        table.put_item(
            Item={
                'username': username,
                'age': int(age)
            }
        )
        messagebox.showinfo("Success", "User added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def fetch_users():
    try:
        response = table.scan()
        items = response['Items']
        users_list.delete(0, tk.END)
        for item in items:
            users_list.insert(tk.END, f"Username: {item['username']}, Age: {item['age']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal
root = tk.Tk()
root.title("DynamoDB Local GUI")

# Crear widgets
label_username = tk.Label(root, text="Username")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_age = tk.Label(root, text="Age")
label_age.pack()
entry_age = tk.Entry(root)
entry_age.pack()

button_add = tk.Button(root, text="Add User", command=insert_user)
button_add.pack()

button_fetch = tk.Button(root, text="Fetch Users", command=fetch_users)
button_fetch.pack()

users_list = tk.Listbox(root)
users_list.pack()

# Ejecutar la aplicación
root.mainloop()
