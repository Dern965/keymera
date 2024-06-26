import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='fakeMyKeyId', aws_secret_access_key='fakeSecretAccessKey')
table = dynamodb.Table('Transacciones')

transacciones = [
    {
        "Num_Transaccion": 1,
        "Categoria": "Electrónica",
        "Articulo": {
            "Nombre": "Televisor",
            "Precio": Decimal('500'),
            "Tipo_transaccion": True,
            "Descripciones": {
                "Ancho": Decimal('120'),
                "Alto": Decimal('70'),
                "Profundidad": Decimal('10'),
                "Peso": Decimal('15'),
                "Material": "Plástico",
                "Rasgos": "Pantalla 4K"
            }
        },
        "Cliente": {
            "Nombre": "Juan Pérez",
            "Calle": "Av. Siempre Viva",
            "No_int": "15",
            "No_ext": "5",
            "CP": "12345",
            "Estado": "CDMX",
            "Municipio": "Coyoacán",
            "Colonia": "Centro",
            "Telefono": "5551234567",
            "Correo": "juanperez@mail.com"
        },
        "Cantidad_acumulada": Decimal('1000'),
        "Cantidad_a_prestar": Decimal('800'),
        "Monto_inicial": Decimal('500'),
        "Mensualidades": Decimal('6'),
        "Fecha_transaccion": "2023-05-01"
    },
    {
        "Num_Transaccion": 2,
        "Categoria": "Electrónica",
        "Articulo": {
            "Nombre": "Laptop",
            "Precio": Decimal('1000'),
            "Tipo_transaccion": True,
            "Descripciones": {
                "Ancho": Decimal('35'),
                "Alto": Decimal('25'),
                "Profundidad": Decimal('2'),
                "Peso": Decimal('1.5'),
                "Material": "Metal",
                "Rasgos": "16GB RAM"
            }
        },
        "Cliente": {
            "Nombre": "María Gómez",
            "Calle": "Calle Falsa",
            "No_int": "4",
            "No_ext": "2",
            "CP": "54321",
            "Estado": "CDMX",
            "Municipio": "Cuauhtémoc",
            "Colonia": "Roma",
            "Telefono": "5557654321",
            "Correo": "mariagomez@mail.com"
        },
        "Cantidad_acumulada": Decimal('2000'),
        "Cantidad_a_prestar": Decimal('1600'),
        "Monto_inicial": Decimal('1000'),
        "Mensualidades": Decimal('12'),
        "Fecha_transaccion": "2023-06-01"
    },
    {
        "Num_Transaccion": 3,
        "Categoria": "Electrodomésticos",
        "Articulo": {
            "Nombre": "Refrigerador",
            "Precio": Decimal('800'),
            "Tipo_transaccion": True,
            "Descripciones": {
                "Ancho": Decimal('80'),
                "Alto": Decimal('180'),
                "Profundidad": Decimal('60'),
                "Peso": Decimal('70'),
                "Material": "Metal",
                "Rasgos": "Doble puerta"
            }
        },
        "Cliente": {
            "Nombre": "Carlos López",
            "Calle": "Calle del Sol",
            "No_int": "9",
            "No_ext": "3",
            "CP": "67890",
            "Estado": "CDMX",
            "Municipio": "Benito Juárez",
            "Colonia": "Narvarte",
            "Telefono": "5556789012",
            "Correo": "carloslopez@mail.com"
        },
        "Cantidad_acumulada": Decimal('1600'),
        "Cantidad_a_prestar": Decimal('1200'),
        "Monto_inicial": Decimal('800'),
        "Mensualidades": Decimal('10'),
        "Fecha_transaccion": "2023-07-01"
    },
    {
        "Num_Transaccion": 4,
        "Categoria": "Joyería",
        "Articulo": {
            "Nombre": "Anillo de oro",
            "Precio": Decimal('200'),
            "Tipo_transaccion": True,
            "Descripciones": {
                "Ancho": Decimal('0.5'),
                "Alto": Decimal('0.2'),
                "Profundidad": Decimal('0.2'),
                "Peso": Decimal('0.05'),
                "Material": "Oro",
                "Rasgos": "18K"
            }
        },
        "Cliente": {
            "Nombre": "Ana Torres",
            "Calle": "Calle Luna",
            "No_int": "6",
            "No_ext": "1",
            "CP": "67890",
            "Estado": "CDMX",
            "Municipio": "Azcapotzalco",
            "Colonia": "Santa María",
            "Telefono": "5554321098",
            "Correo": "anatorres@mail.com"
        },
        "Cantidad_acumulada": Decimal('400'),
        "Cantidad_a_prestar": Decimal('320'),
        "Monto_inicial": Decimal('200'),
        "Mensualidades": Decimal('3'),
        "Fecha_transaccion": "2023-08-01"
    },
    {
        "Num_Transaccion": 5,
        "Categoria": "Electrónica",
        "Articulo": {
            "Nombre": "Smartphone",
            "Precio": Decimal('300'),
            "Tipo_transaccion": False,
            "Descripciones": {
                "Ancho": Decimal('7'),
                "Alto": Decimal('14'),
                "Profundidad": Decimal('0.8'),
                "Peso": Decimal('0.2'),
                "Material": "Metal",
                "Rasgos": "64GB"
            }
        },
        "Cliente": {
            "Nombre": "Luis Martínez",
            "Calle": "Calle Palma",
            "No_int": "7",
            "No_ext": "4",
            "CP": "78901",
            "Estado": "CDMX",
            "Municipio": "Miguel Hidalgo",
            "Colonia": "Polanco",
            "Telefono": "5553210987",
            "Correo": "luismartinez@mail.com"
        },
        "Cantidad_acumulada": Decimal('600'),
        "Cantidad_a_prestar": Decimal('480'),
        "Monto_inicial": Decimal('300'),
        "Mensualidades": Decimal('5'),
        "Fecha_transaccion": "2023-04-01"
    },
    {
        "Num_Transaccion": 6,
        "Categoria": "Joyería",
        "Articulo": {
            "Nombre": "Reloj de plata",
            "Precio": Decimal('150'),
            "Tipo_transaccion": True,
            "Descripciones": {
                "Ancho": Decimal('3'),
                "Alto": Decimal('3'),
                "Profundidad": Decimal('1'),
                "Peso": Decimal('0.1'),
                "Material": "Plata",
                "Rasgos": "Analogico"
            }
        },
        "Cliente": {
            "Nombre": "Elena Díaz",
            "Calle": "Calle Flor",
            "No_int": "12",
            "No_ext": "8",
            "CP": "89012",
            "Estado": "CDMX",
            "Municipio": "Iztapalapa",
            "Colonia": "Santa Cruz",
            "Telefono": "5558901234",
            "Correo": "elenadiaz@mail.com"
        },
        "Cantidad_acumulada": Decimal('300'),
        "Cantidad_a_prestar": Decimal('240'),
        "Monto_inicial": Decimal('150'),
        "Mensualidades": Decimal('6'),
        "Fecha_transaccion": "2023-09-01"
    },
    {
        "Num_Transaccion": 7,
        "Categoria": "Electrónica",
        "Articulo": {
            "Nombre": "Consola de videojuegos",
            "Precio": Decimal('400'),
            "Tipo_transaccion": True,
            "Descripciones": {
                "Ancho": Decimal('30'),
                "Alto": Decimal('10'),
                "Profundidad": Decimal('15'),
                "Peso": Decimal('2'),
                "Material": "Plástico",
                "Rasgos": "4K HDR"
            }
        },
        "Cliente": {
            "Nombre": "Pedro Ramírez",
            "Calle": "Calle Verde",
            "No_int": "10",
            "No_ext": "5",
            "CP": "67891",
            "Estado": "CDMX",
            "Municipio": "Tlalpan",
            "Colonia": "Pedregal",
            "Telefono": "5556789123",
            "Correo": "pedroramirez@mail.com"
        },
        "Cantidad_acumulada": Decimal('800'),
        "Cantidad_a_prestar": Decimal('640'),
        "Monto_inicial": Decimal('400'),
        "Mensualidades": Decimal('12'),
        "Fecha_transaccion": "2023-07-15"
    },
    {
        "Num_Transaccion": 8,
        "Categoria": "Electrodomésticos",
        "Articulo": {
            "Nombre": "Microondas",
            "Precio": Decimal('100'),
            "Tipo_transaccion": False,
            "Descripciones": {
                "Ancho": Decimal('50'),
                "Alto": Decimal('30'),
                "Profundidad": Decimal('40'),
                "Peso": Decimal('12'),
                "Material": "Metal",
                "Rasgos": "Inoxidable"
            }
        },
        "Cliente": {
            "Nombre": "Sofía Herrera",
            "Calle": "Calle Azul",
            "No_int": "11",
            "No_ext": "7",
            "CP": "12346",
            "Estado": "CDMX",
            "Municipio": "Venustiano Carranza",
            "Colonia": "Jardín Balbuena",
            "Telefono": "5551234568",
            "Correo": "sofia.herrera@mail.com"
        },
        "Cantidad_acumulada": Decimal('200'),
        "Cantidad_a_prestar": Decimal('160'),
        "Monto_inicial": Decimal('100'),
        "Mensualidades": Decimal('4'),
        "Fecha_transaccion": "2023-08-05"
    },
    {
        "Num_Transaccion": 9,
        "Categoria": "Electrónica",
        "Articulo": {
            "Nombre": "Tablet",
            "Precio": Decimal('350'),
            "Tipo_transaccion": True,
            "Descripciones": {
                "Ancho": Decimal('20'),
                "Alto": Decimal('30'),
                "Profundidad": Decimal('1'),
                "Peso": Decimal('0.5'),
                "Material": "Metal",
                "Rasgos": "128GB"
            }
        },
        "Cliente": {
            "Nombre": "Daniel Ruiz",
            "Calle": "Calle Amarilla",
            "No_int": "13",
            "No_ext": "6",
            "CP": "23456",
            "Estado": "CDMX",
            "Municipio": "Gustavo A. Madero",
            "Colonia": "Lindavista",
            "Telefono": "5552345678",
            "Correo": "daniel.ruiz@mail.com"
        },
        "Cantidad_acumulada": Decimal('700'),
        "Cantidad_a_prestar": Decimal('560'),
        "Monto_inicial": Decimal('350'),
        "Mensualidades": Decimal('7'),
        "Fecha_transaccion": "2023-06-10"
    },
    {
        "Num_Transaccion": 10,
        "Categoria": "Joyería",
        "Articulo": {
            "Nombre": "Collar de perlas",
            "Precio": Decimal('250'),
            "Tipo_transaccion": True,
            "Descripciones": {
                "Ancho": Decimal('1'),
                "Alto": Decimal('1'),
                "Profundidad": Decimal('0.5'),
                "Peso": Decimal('0.05'),
                "Material": "Perlas",
                "Rasgos": "Auténtico"
            }
        },
        "Cliente": {
            "Nombre": "Fernanda Castillo",
            "Calle": "Calle Roja",
            "No_int": "14",
            "No_ext": "8",
            "CP": "34567",
            "Estado": "CDMX",
            "Municipio": "Coyoacán",
            "Colonia": "Villa Coapa",
            "Telefono": "5553456789",
            "Correo": "fernanda.castillo@mail.com"
        },
        "Cantidad_acumulada": Decimal('500'),
        "Cantidad_a_prestar": Decimal('400'),
        "Monto_inicial": Decimal('250'),
        "Mensualidades": Decimal('6'),
        "Fecha_transaccion": "2023-05-20"
    }
]

for transaccion in transacciones:
    table.put_item(Item=transaccion)

print("Registros insertados exitosamente.")
