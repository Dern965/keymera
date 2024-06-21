import streamlit as st
import boto3
from botocore.exceptions import ClientError
from streamlit_option_menu import option_menu
import pandas as pd

#Configuración de DynamoDB local
dynamodb_r = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='fakeMyKeyId', aws_secret_access_key='fakeSecretAccessKey')
dynamodb_c = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='fakeMyKeyId', aws_secret_access_key='fakeSecretAccessKey')

# Tabla Transacciones
Tabla_Transacciones = dynamodb_r.Table('Transacciones')

def Crear_Tabla():
    try:
        Transacciones_table = dynamodb_r.create_table(
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
        Transacciones_table.wait_until_exists()
        print("Tabla 'Transacciones' creada.")
    except dynamodb_r.meta.client.exceptions.ResourceInUseException:
        print("La tabla 'Transacciones' ya existe.")


def agregar_transaccion(datos_transaccion):
    Tabla_Transacciones.put_item(Item=datos_transaccion)
    
def obtener_transacciones():
    response = Tabla_Transacciones.scan()
    return response['Items']
    
def actualizar_transaccion(num_transaccion, categoria, nombre_articulo, precio_articulo, tipo_transaccion, ancho, alto, profundidad, peso, material, rasgos, nombre_cliente, calle, no_int, no_ext, cp, estado, municipio, colonia, telefono, correo, cantidad_acumulada, cantidad_a_prestar, monto_inicial, mensualidades, fecha_transaccion):
    response = dynamodb_c.update_item(
        TableName='Transacciones',
        Key={
            'Num_Transaccion': {'N': str(num_transaccion)},
            'Categoria': {'S': categoria}
        },
        ExpressionAttributeNames={
            '#A': 'Articulo',
            '#CA': 'Cantidad_acumulada',
            '#CAP': 'Cantidad_a_prestar',
            '#C': 'Cliente',
            '#MI': 'Monto_inicial',
            '#FT': 'Fecha_transaccion',
            '#ME': 'Mensualidades'
        },
        ExpressionAttributeValues={
            ':a': {'M': {
                    'Nombre': {'S': nombre_articulo},
                    'Precio': {'N': str(precio_articulo)},
                    'Tipo_transaccion': {'BOOL': tipo_transaccion},
                    'Descripciones': {'M': {
                        'Ancho': {'N': str(ancho)},
                        'Alto': {'N': str(alto)},
                        'Profundidad': {'N': str(profundidad)},
                        'Peso': {'N': str(peso)},
                        'Material': {'S': material},
                        'Rasgos': {'S': rasgos}
                    }}
                }},
            ':c': {'M': {
                    'Nombre': {'S': nombre_cliente},
                    'Calle': {'S': calle},
                    'No_int': {'S': no_int},
                    'No_ext': {'S': no_ext},
                    'CP': {'S': cp},
                    'Estado': {'S': estado},
                    'Municipio': {'S': municipio},
                    'Colonia': {'S': colonia},
                    'Telefono': {'S': telefono},
                    'Correo': {'S': correo}
                }},
            ':ca': {'N': str(cantidad_acumulada)},
            ':cap': {'N': str(cantidad_a_prestar)},
            ':mi': {'N': str(monto_inicial)},
            ':ft': {'S': fecha_transaccion},
            ':me': {'N': str(mensualidades)}
        },
        UpdateExpression='SET #A = :a, #CA = :ca, #CAP = :cap, #C = :c, #MI = :mi, #FT = :ft, #ME = :me',
        ReturnValues='ALL_NEW'
    )
    return response

def borrar_transaccion(num_transaccion, categoria):
    Tabla_Transacciones.delete_item(Key={'Num_Transaccion': num_transaccion, 'Categoria': categoria})

def num_transaccion_existe(num_transaccion):
    if not num_transaccion:
        return 1
    transacciones_ordenadas = sorted(transacciones, key=lambda x: int(x['Num_Transaccion']))
    for i in range(1,len(transacciones_ordenadas)+1):
        if i != int(transacciones_ordenadas[i-1]['Num_Transaccion']):
            return i
    return len(transacciones_ordenadas)+1

def ejecutar_consulta(query):
    try:
        response = dynamodb_c.execute_statement(Statement=query)
        return response['Items']
    except Exception as e:
        print(f"Error ejecutando consulta: {e}")
        return None

# Crear el menu lateral
with st.sidebar:
    selected_option = option_menu(
        menu_title="Sistema Gestor de Empeños",
        options=["Transacciones", "Modificar Transaccion", "Nueva Transacción", "Consultas relevantes"],
        icons=["house", "file-earmark-plus", "file-earmark-text", "pencil-square"],
        menu_icon="cast",
        default_index=0
    )

if selected_option == "Transacciones":
    st.subheader("Transacciones")
    Crear_Tabla()
    transacciones = obtener_transacciones()

    if transacciones:
        transacciones = sorted(transacciones, key=lambda x: int(x['Num_Transaccion']))
        for transaccion in transacciones:
            with st.expander(f"Transacción: {transaccion['Num_Transaccion']} - Categoría: {transaccion['Categoria']}"):
                articulo = transaccion['Articulo']
                cliente = transaccion['Cliente']
                descripciones = articulo['Descripciones']
                
                st.markdown("### Información del Artículo")
                st.markdown(f"**Nombre:** {articulo['Nombre']}")
                st.markdown(f"**Precio:** {articulo['Precio']}")
                st.markdown(f"**Tipo de Transacción:** {'Empeño' if articulo['Tipo_transaccion'] else 'Venta'}")
                
                st.markdown("#### Descripciones del Artículo")
                st.markdown(f"- **Ancho:** {descripciones['Ancho']}")
                st.markdown(f"- **Alto:** {descripciones['Alto']}")
                st.markdown(f"- **Profundidad:** {descripciones['Profundidad']}")
                st.markdown(f"- **Peso:** {descripciones['Peso']}")
                st.markdown(f"- **Material:** {descripciones['Material']}")
                st.markdown(f"- **Rasgos:** {descripciones['Rasgos']}")
                
                st.markdown("### Información del Cliente")
                st.markdown(f"**Nombre:** {cliente['Nombre']}")
                st.markdown(f"**Calle:** {cliente['Calle']}")
                st.markdown(f"**Número Interior:** {cliente['No_int']}")
                st.markdown(f"**Número Exterior:** {cliente['No_ext']}")
                st.markdown(f"**Código Postal:** {cliente['CP']}")
                st.markdown(f"**Estado:** {cliente['Estado']}")
                st.markdown(f"**Municipio:** {cliente['Municipio']}")
                st.markdown(f"**Colonia:** {cliente['Colonia']}")
                st.markdown(f"**Teléfono:** {cliente['Telefono']}")
                st.markdown(f"**Correo Electrónico:** {cliente['Correo']}")
                
                st.markdown("### Información de la Transacción")
                st.markdown(f"**Cantidad Acumulada:** {transaccion['Cantidad_acumulada']}")
                st.markdown(f"**Cantidad a Prestar:** {transaccion['Cantidad_a_prestar']}")
                st.markdown(f"**Monto Inicial:** {transaccion['Monto_inicial']}")
                st.markdown(f"**Mensualidades:** {transaccion['Mensualidades']}")
                st.markdown(f"**Fecha de la Transacción:** {transaccion['Fecha_transaccion']}")
                
                if st.button(f"Borrar {transaccion['Num_Transaccion']}"):
                    borrar_transaccion(transaccion['Num_Transaccion'], transaccion['Categoria'])
                    st.success("Transacción borrada exitosamente.")
                    st.experimental_rerun()
    else:
        st.write("No hay transacciones registradas.")

if selected_option == "Modificar Transaccion":
    st.subheader("Modifique la transacción")
    transacciones = obtener_transacciones()

    if transacciones:
        transacciones = sorted(transacciones, key=lambda x: int(x['Num_Transaccion']))
        for i, transaccion in enumerate(transacciones):
            with st.expander(f"Transacción: {transaccion['Num_Transaccion']} - Categoría: {transaccion['Categoria']}"):
                articulo = transaccion['Articulo']
                cliente = transaccion['Cliente']
                descripciones = articulo['Descripciones']
                
                st.markdown("### Información del Artículo")
                nuevo_articulo_nombre = st.text_input("Nombre del artículo", value=articulo['Nombre'], key=f"nuevo_articulo_nombre_{i}")
                nuevo_articulo_precio = st.number_input("Precio del artículo", value=int(articulo['Precio']), key=f"nuevo_articulo_precio_{i}")
                nuevo_articulo_tipo_transaccion = st.checkbox("¿Es un artículo a empeñar?", value=articulo['Tipo_transaccion'], key=f"nuevo_articulo_tipo_transaccion_{i}")
                
                st.markdown("#### Descripciones del Artículo")
                nuevo_articulo_ancho = st.number_input("Ancho", value=int(descripciones['Ancho']), key=f"nuevo_articulo_ancho_{i}")
                nuevo_articulo_alto = st.number_input("Alto", value=int(descripciones['Alto']), key=f"nuevo_articulo_alto_{i}")
                nuevo_articulo_profundidad = st.number_input("Profundidad", value=int(descripciones['Profundidad']), key=f"nuevo_articulo_profundidad_{i}")
                nuevo_articulo_peso = st.number_input("Peso", value=int(descripciones['Peso']), key=f"nuevo_articulo_peso_{i}")
                nuevo_articulo_material = st.text_input("Material", value=descripciones['Material'], key=f"nuevo_articulo_material_{i}")
                nuevo_articulo_rasgos = st.text_input("Rasgos", value=descripciones['Rasgos'], key=f"nuevo_articulo_rasgos_{i}")
                
                st.markdown("### Información del Cliente")
                nuevo_cliente_nombre = st.text_input("Nombre del cliente", value=cliente['Nombre'], key=f"nuevo_cliente_nombre_{i}")
                nuevo_cliente_calle = st.text_input("Calle", value=cliente['Calle'], key=f"nuevo_cliente_calle_{i}")
                nuevo_cliente_no_int = st.text_input("Número interior", value=cliente['No_int'], key=f"nuevo_cliente_no_int_{i}")
                nuevo_cliente_no_ext = st.text_input("Número exterior", value=cliente['No_ext'], key=f"nuevo_cliente_no_ext_{i}")
                nuevo_cliente_cp = st.text_input("Código Postal", value=cliente['CP'], key=f"nuevo_cliente_cp_{i}")
                nuevo_cliente_estado = st.text_input("Estado", value=cliente['Estado'], key=f"nuevo_cliente_estado_{i}")
                nuevo_cliente_municipio = st.text_input("Municipio", value=cliente['Municipio'], key=f"nuevo_cliente_municipio_{i}")
                nuevo_cliente_colonia = st.text_input("Colonia", value=cliente['Colonia'], key=f"nuevo_cliente_colonia_{i}")
                nuevo_cliente_telefono = st.text_input("Teléfono", value=cliente['Telefono'], key=f"nuevo_cliente_telefono_{i}")
                nuevo_cliente_correo = st.text_input("Correo electrónico", value=cliente['Correo'], key=f"nuevo_cliente_correo_{i}")
                
                st.markdown("### Información de la Transacción")
                nueva_cantidad_acumulada = st.number_input("Cantidad acumulada", value=int(transaccion['Cantidad_acumulada']), key=f"nueva_cantidad_acumulada_{i}")
                nueva_cantidad_a_prestar = st.number_input("Cantidad a prestar", value=int(transaccion['Cantidad_a_prestar']), key=f"nueva_cantidad_a_prestar_{i}")
                nuevo_monto_inicial = st.number_input("Monto inicial", value=int(transaccion['Monto_inicial']), key=f"nuevo_monto_inicial_{i}")
                nuevas_mensualidades = st.number_input("Mensualidades", value=int(transaccion['Mensualidades']), key=f"nuevas_mensualidades_{i}")
                nueva_fecha_transaccion = st.text_input("Fecha de la transacción", value=transaccion['Fecha_transaccion'], key=f"nueva_fecha_transaccion_{i}")

                if st.button(f"Modificar {transaccion['Num_Transaccion']}", key=f"modificar_{transaccion['Num_Transaccion']}"):
                    actualizar_transaccion(
                        transaccion['Num_Transaccion'],
                        transaccion['Categoria'],
                        nuevo_articulo_nombre,
                        nuevo_articulo_precio,
                        nuevo_articulo_tipo_transaccion,
                        nuevo_articulo_ancho,
                        nuevo_articulo_alto,
                        nuevo_articulo_profundidad,
                        nuevo_articulo_peso,
                        nuevo_articulo_material,
                        nuevo_articulo_rasgos,
                        nuevo_cliente_nombre,
                        nuevo_cliente_calle,
                        nuevo_cliente_no_int,
                        nuevo_cliente_no_ext,
                        nuevo_cliente_cp,
                        nuevo_cliente_estado,
                        nuevo_cliente_municipio,
                        nuevo_cliente_colonia,
                        nuevo_cliente_telefono,
                        nuevo_cliente_correo,
                        nueva_cantidad_acumulada,
                        nueva_cantidad_a_prestar,
                        nuevo_monto_inicial,
                        nuevas_mensualidades,
                        nueva_fecha_transaccion
                    )
                    st.success("Transacción actualizada exitosamente.")

if selected_option == "Nueva Transacción":
    transacciones = obtener_transacciones()
    numeros_transacciones = num_transaccion_existe(transacciones)

    st.subheader(f"Nueva Transacción No:{numeros_transacciones}")
    st.markdown("Llene los campos para agregar una nueva transacción.")
    col1, col2 = st.columns(2)

    

    with col1:
        st.markdown("### Información del Artículo")
        num_transaccion = numeros_transacciones
        categoria = st.text_input("Categoría")
        articulo_nombre = st.text_input("Nombre del artículo")
        articulo_precio = st.number_input("Precio del artículo", min_value=0, step=1, format="%d")
        articulo_tipo_transaccion = st.checkbox("¿Es un artículo a empeñar?")
        
        st.markdown("#### Descripciones del Artículo")
        articulo_ancho = st.number_input("Ancho", min_value=0, step=1, format="%d")
        articulo_alto = st.number_input("Alto", min_value=0, step=1, format="%d")
        articulo_profundidad = st.number_input("Profundidad", min_value=0, step=1, format="%d")
        articulo_peso = st.number_input("Peso", min_value=0, step=1, format="%d")
        articulo_material = st.text_input("Material")
        articulo_rasgos = st.text_input("Rasgos")

    with col2:
        st.markdown("### Información del Cliente")
        cliente_nombre = st.text_input("Nombre del cliente")
        cliente_calle = st.text_input("Calle")
        cliente_no_int = st.text_input("Número interior")
        cliente_no_ext = st.text_input("Número exterior")
        cliente_cp = st.text_input("Código Postal")
        cliente_estado = st.text_input("Estado")
        cliente_municipio = st.text_input("Municipio")
        cliente_colonia = st.text_input("Colonia")
        cliente_telefono = st.text_input("Teléfono")
        cliente_correo = st.text_input("Correo electrónico")
        
        st.markdown("### Información de la Transacción")
        cantidad_acumulada = st.number_input("Cantidad acumulada", min_value=0, step=1, format="%d")
        cantidad_a_prestar = st.number_input("Cantidad a prestar", min_value=0, step=1, format="%d")
        monto_inicial = st.number_input("Monto inicial", min_value=0, step=0, format="%d")
        mensualidades = st.number_input("Mensualidades", min_value=1, step=1, format="%d")
        fecha_transaccion = st.date_input("Fecha de la transacción").strftime("%Y/%m/%d")

    if st.button("Agregar transacción"):
        datos_transaccion = {
            'Num_Transaccion': num_transaccion,
            'Categoria': categoria,
            'Articulo': {
                'Nombre': articulo_nombre,
                'Precio': articulo_precio,
                'Tipo_transaccion': articulo_tipo_transaccion,
                'Descripciones': {
                    'Ancho': articulo_ancho,
                    'Alto': articulo_alto,
                    'Profundidad': articulo_profundidad,
                    'Peso': articulo_peso,
                    'Material': articulo_material,
                    'Rasgos': articulo_rasgos
                }
            },
            'Cliente': {
                'Nombre': cliente_nombre,
                'Calle': cliente_calle,
                'No_int': cliente_no_int,
                'No_ext': cliente_no_ext,
                'CP': cliente_cp,
                'Estado': cliente_estado,
                'Municipio': cliente_municipio,
                'Colonia': cliente_colonia,
                'Telefono': cliente_telefono,
                'Correo': cliente_correo
            },
            'Cantidad_acumulada': cantidad_acumulada,
            'Cantidad_a_prestar': cantidad_a_prestar,
            'Monto_inicial': monto_inicial,
            'Mensualidades': mensualidades,
            'Fecha_transaccion': fecha_transaccion
        }
        agregar_transaccion(datos_transaccion)
        st.success("Transacción agregada exitosamente.")

if selected_option == "Consultas relevantes":
    st.subheader("Consultas relevantes")

    # Consulta 1: Productos más empeñados y vendidos en los últimos meses
    consulta_1 = """
    SELECT Categoria, Fecha_transaccion
    FROM Transacciones
    WHERE Fecha_transaccion >= '2023-05-01' AND Fecha_transaccion <= '2023-08-01';
    """
    resultado_1 = ejecutar_consulta(consulta_1)
    if resultado_1:
        df1 = pd.DataFrame([{
            'Categoria': item['Categoria']['S'],
            'Fecha_transaccion': item['Fecha_transaccion']['S']
        } for item in resultado_1])
        total_transacciones_1 = df1.groupby('Categoria').size().reset_index(name='TotalTransacciones')
        st.write("Productos más empeñados y vendidos en los últimos meses:")
        st.dataframe(total_transacciones_1)
    else:
        st.write("No se encontraron resultados para la consulta 1.")

    # Consulta 2: Total de transacciones por categoría en un mes
    consulta_2 = """
    SELECT Categoria, Fecha_transaccion
    FROM Transacciones
    WHERE Fecha_transaccion >= '2023-08-01' AND Fecha_transaccion <= '2023-08-31';
    """
    resultado_2 = ejecutar_consulta(consulta_2)
    if resultado_2:
        df2 = pd.DataFrame([{
            'Categoria': item['Categoria']['S'],
            'Fecha_transaccion': item['Fecha_transaccion']['S']
        } for item in resultado_2])
        total_transacciones_2 = df2.groupby('Categoria').size().reset_index(name='TotalTransacciones')
        st.write("Total de transacciones por categoría en agosto de 2023:")
        st.dataframe(total_transacciones_2)
    else:
        st.write("No se encontraron resultados para la consulta 2.")

    # Consulta 3: Elementos empeñados que aún no han sido vendidos
    consulta_3 = """
    SELECT *
    FROM Transacciones
    WHERE Articulo.Tipo_transaccion = true;
    """
    resultado_3 = ejecutar_consulta(consulta_3)
    if resultado_3:
        st.write("Elementos empeñados que aún no han sido vendidos:")
        st.dataframe(pd.DataFrame(resultado_3))
    else:
        st.write("No se encontraron resultados para la consulta 3.")