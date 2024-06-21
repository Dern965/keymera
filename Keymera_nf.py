import streamlit as st
import boto3
import pandas as pd
from botocore.exceptions import ClientError

# Configurar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='fakeMyKeyId', aws_secret_access_key='fakeSecretAccessKey')
dynamodb_client = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='fakeMyKeyId', aws_secret_access_key='fakeSecretAccessKey')

# Tablas de DynamoDB
empenios_table = dynamodb.Table('Empenios')

# Función para añadir un empeño
def agregar_empeno(datos_empeno):
    try:
        empenios_table.put_item(Item=datos_empeno)
        return True
    except ClientError as e:
        st.error(f"Error al agregar el empeño: {e.response['Error']['Message']}")
        return False

# Función para obtener todos los empeños
def obtener_empenos():
    try:
        response = empenios_table.scan()
        return response['Items']
    except ClientError as e:
        st.error(f"Error al obtener los empeños: {e.response['Error']['Message']}")
        return []

# Función para eliminar un empeño
def eliminar_empeno(id_empeno, categoria):
    try:
        empenios_table.delete_item(Key={'Num_Empenio': id_empeno, 'Categoria': categoria})
        return True
    except ClientError as e:
        st.error(f"Error al eliminar el empeño: {e.response['Error']['Message']}")
        return False

# Función para crear la entrada de actualización de DynamoDB
def create_update_item_input(num_empenio, categoria, nuevos_datos):
    return {
        "TableName": "Empenios",
        "Key": {
            "Num_Empenio": {"N": str(num_empenio)},
            "Categoria": {"S": categoria}
        },
        "UpdateExpression": "SET #09a80 = :09a80, #09a81 = :09a81, #09a82 = :09a82, #09a83 = :09a83, #09a84 = :09a84, #09a85 = :09a85, #09a86 = :09a86",
        "ExpressionAttributeNames": {
            "#09a80": "Cantidad_acumulada",
            "#09a81": "Articulos",
            "#09a82": "Cliente",
            "#09a83": "Monto_inicial",
            "#09a84": "Cantidad_a_prestar",
            "#09a85": "Mensualidades",
            "#09a86": "Fecha_empenio"
        },
        "ExpressionAttributeValues": {
            ":09a80": {"N": str(nuevos_datos['Cantidad_acumulada'])},
            ":09a81": {
                "M": {
                    "Nombre": {"S": nuevos_datos['Articulos']['Nombre']},
                    "Precio": {"N": str(nuevos_datos['Articulos']['Precio'])},
                    "Descripciones": {
                        "M": {
                            "Alto": {"N": str(nuevos_datos['Articulos']['Descripciones']['Alto'])},
                            "Ancho": {"N": str(nuevos_datos['Articulos']['Descripciones']['Ancho'])},
                            "Profundo": {"N": str(nuevos_datos['Articulos']['Descripciones']['Profundo'])},
                            "Material": {"S": nuevos_datos['Articulos']['Descripciones']['Material']},
                            "Rasgos": {"S": nuevos_datos['Articulos']['Descripciones']['Rasgos']}
                        }
                    },
                    "Tipo_transaccion": {"BOOL": nuevos_datos['Articulos']['Tipo_transaccion']}
                }
            },
            ":09a82": {
                "M": {
                    "Nombre": {"S": nuevos_datos['Cliente']['Nombre']},
                    "Calle": {"S": nuevos_datos['Cliente']['Calle']},
                    "No_int": {"S": nuevos_datos['Cliente']['No_int']},
                    "No_ext": {"S": nuevos_datos['Cliente']['No_ext']},
                    "CP": {"S": nuevos_datos['Cliente']['CP']},
                    "Estado": {"S": nuevos_datos['Cliente']['Estado']},
                    "Municipio_Alcaldia": {"S": nuevos_datos['Cliente']['Municipio_Alcaldia']},
                    "Colonia": {"S": nuevos_datos['Cliente']['Colonia']},
                    "Telefono": {"S": nuevos_datos['Cliente']['Telefono']},
                    "Correo": {"S": nuevos_datos['Cliente']['Correo']},
                    "Fecha_registro": {"S": nuevos_datos['Cliente']['Fecha_registro']}
                }
            },
            ":09a83": {"N": str(nuevos_datos['Monto_inicial'])},
            ":09a84": {"N": str(nuevos_datos['Cantidad_a_prestar'])},
            ":09a85": {"N": str(nuevos_datos['Mensualidades'])},
            ":09a86": {"S": nuevos_datos['Fecha_empenio']}
        }
    }

# Función para ejecutar la actualización del ítem en DynamoDB
def execute_update_item(cliente,input):
    try:
        response =cliente.update_item(**input)
        st.success("Empeño modificado exitosamente.")
    except ClientError as error:
        st.error(f"Error al modificar el empeño: {error.response['Error']['Message']}")
    except BaseException as error:
        st.error(f"Error desconocido al modificar el empeño: {error}")

# Función para modificar un empeño
def modificar_empeno(num_empenio, categoria, nuevos_datos):
    update_item_input = create_update_item_input(num_empenio, categoria, nuevos_datos)
    execute_update_item(dynamodb_client,update_item_input)

# Función para obtener el siguiente número de empeño
def obtener_siguiente_num_empenio():
    empenios = obtener_empenos()
    if empenios:
        num_empenios_existentes = [int(empeno['Num_Empenio']) for empeno in empenios]
        num_empenios_existentes.sort()
        for i in range(1, len(num_empenios_existentes) + 1):
            if i not in num_empenios_existentes:
                return i
        return max(num_empenios_existentes) + 1
    else:
        return 1

st.title('Sistema de Empeños y Ventas')

menu = ['Listado de Empeños']
eleccion = st.sidebar.selectbox('Selecciona una opción', menu)

if eleccion == 'Listado de Empeños':
    st.subheader('Listado de Empeños')
    empenios = obtener_empenos()

    if empenios:
        for empeno in empenios:
            with st.expander(f"Empeño {empeno['Num_Empenio']} - {empeno['Categoria']}"):
                articulos = empeno['Articulos']
                cliente = empeno['Cliente']
                medidas = articulos['Descripciones']
                st.write(f"**Número de Empeño:** {empeno['Num_Empenio']}")
                st.write(f"**Categoría:** {empeno['Categoria']}")
                st.write(f"**Monto Inicial:** {empeno['Monto_inicial']}")
                st.write(f"**Cantidad Acumulada:** {empeno['Cantidad_acumulada']}")
                st.write(f"**Cantidad a Prestar:** {empeno['Cantidad_a_prestar']}")
                st.write(f"**Mensualidades:** {empeno['Mensualidades']}")
                st.write(f"**Nombre del Artículo:** {articulos['Nombre']}")
                st.write(f"**Precio:** {articulos['Precio']}")
                st.write(f"**Alto (cm):** {medidas['Alto']}")
                st.write(f"**Ancho (cm):** {medidas['Ancho']}")
                st.write(f"**Profundo (cm):** {medidas['Profundo']}")
                st.write(f"**Material:** {medidas['Material']}")
                st.write(f"**Rasgos:** {medidas['Rasgos']}")
                st.write(f"**Tipo de Transacción:** {'Empeño' if articulos['Tipo_transaccion'] else 'Venta'}")
                st.write(f"**Fecha de Empeño:** {empeno['Fecha_empenio']}")
                st.write(f"**Nombre del Cliente:** {cliente['Nombre']}")
                st.write(f"**Calle:** {cliente['Calle']}")
                st.write(f"**No. Interior:** {cliente['No_int']}")
                st.write(f"**No. Exterior:** {cliente['No_ext']}")
                st.write(f"**C.P.:** {cliente['CP']}")
                st.write(f"**Estado:** {cliente['Estado']}")
                st.write(f"**Municipio o Alcaldía:** {cliente['Municipio_Alcaldia']}")
                st.write(f"**Colonia:** {cliente['Colonia']}")
                st.write(f"**Teléfono:** {cliente['Telefono']}")
                st.write(f"**Correo:** {cliente['Correo']}")

                if st.button(f'Modificar {empeno["Num_Empenio"]}', key=f'modificar_btn_{empeno["Num_Empenio"]}'):
                    nuevo_monto_inicial = st.number_input('Monto inicial', min_value=0, step=1, key=f'nuevo_monto_inicial_{empeno["Num_Empenio"]}')
                    nueva_cantidad_a_prestar = st.number_input('Cantidad a prestar', min_value=0, step=1, key=f'nueva_cantidad_a_prestar_{empeno["Num_Empenio"]}')
                    nueva_cantidad_acumulada = st.number_input('Cantidad acumulada', min_value=0, step=1, key=f'nueva_cantidad_acumulada_{empeno["Num_Empenio"]}')
                    nuevas_mensualidades = st.number_input('Mensualidades', min_value=0, step=1, key=f'nuevas_mensualidades_{empeno["Num_Empenio"]}')
                    nueva_fecha_empenio = st.date_input('Fecha de empeño', key=f'nueva_fecha_empenio_{empeno["Num_Empenio"]}').strftime('%Y/%m/%d')
                    nuevo_nombre_cliente = st.text_input('Nombre del cliente', key=f'nuevo_nombre_cliente_{empeno["Num_Empenio"]}')
                    nueva_calle_cliente = st.text_input('Calle del cliente', key=f'nueva_calle_cliente_{empeno["Num_Empenio"]}')
                    nuevo_num_int = st.text_input('Número interior del cliente', key=f'nuevo_num_int_{empeno["Num_Empenio"]}')
                    nuevo_num_ext = st.text_input('Número exterior del cliente', key=f'nuevo_num_ext_{empeno["Num_Empenio"]}')
                    nuevo_cp_cliente = st.text_input('Código postal del cliente', key=f'nuevo_cp_cliente_{empeno["Num_Empenio"]}')
                    nuevo_estado_cliente = st.text_input('Estado del Cliente', key=f'nuevo_estado_cliente_{empeno["Num_Empenio"]}')
                    nuevo_municipio_cliente = st.text_input('Municipio/Alcaldía del Cliente', key=f'nuevo_municipio_cliente_{empeno["Num_Empenio"]}')
                    nueva_colonia_cliente = st.text_input('Colonia del Cliente', key=f'nueva_colonia_cliente_{empeno["Num_Empenio"]}')
                    nuevo_telefono_cliente = st.text_input('Teléfono del Cliente', key=f'nuevo_telefono_cliente_{empeno["Num_Empenio"]}')
                    nuevo_correo_cliente = st.text_input('Correo del Cliente', key=f'nuevo_correo_cliente_{empeno["Num_Empenio"]}')
                    nueva_fecha_registro = st.date_input('Fecha de Registro', key=f'nueva_fecha_registro_{empeno["Num_Empenio"]}').strftime("%Y/%m/%d")
                    nuevo_nombre_articulo = st.text_input('Nombre del Artículo', key=f'nuevo_nombre_articulo_{empeno["Num_Empenio"]}')
                    nuevo_precio_articulo = st.number_input('Precio del Artículo', min_value=0, step=1, key=f'nuevo_precio_articulo_{empeno["Num_Empenio"]}')
                    nuevo_alto_articulo = st.number_input('Alto del Artículo', min_value=0, step=1, key=f'nuevo_alto_articulo_{empeno["Num_Empenio"]}')
                    nuevo_ancho_articulo = st.number_input('Ancho del Artículo', min_value=0, step=1, key=f'nuevo_ancho_articulo_{empeno["Num_Empenio"]}')
                    nuevo_profundo_articulo = st.number_input('Profundo del Artículo', min_value=0, step=1, key=f'nuevo_profundo_articulo_{empeno["Num_Empenio"]}')
                    nuevo_material_articulo = st.text_input('Material del Artículo', key=f'nuevo_material_articulo_{empeno["Num_Empenio"]}')
                    nuevos_rasgos_articulo = st.text_input('Rasgos del Artículo', key=f'nuevos_rasgos_articulo_{empeno["Num_Empenio"]}')

                    menu_mod = ['Venta', 'Empeño']  # False = Venta, True = Empeño
                    elec_mod = st.selectbox('Selecciona una opción', menu_mod, key=f'elec_mod_{empeno["Num_Empenio"]}')

                    if elec_mod == 'Empeño':
                        opc_mod = True
                    else:
                        opc_mod = False

                    nuevos_datos = {
                        'Monto_inicial': nuevo_monto_inicial,
                        'Cantidad_a_prestar': nueva_cantidad_a_prestar,
                        'Cantidad_acumulada': nueva_cantidad_acumulada,
                        'Mensualidades': nuevas_mensualidades,
                        'Fecha_empenio': nueva_fecha_empenio,
                        'Cliente': {
                            'Nombre': nuevo_nombre_cliente,
                            'Calle': nueva_calle_cliente,
                            'No_int': nuevo_num_int,
                            'No_ext': nuevo_num_ext,
                            'CP': nuevo_cp_cliente,
                            'Estado': nuevo_estado_cliente,
                            'Municipio_Alcaldia': nuevo_municipio_cliente,
                            'Colonia': nueva_colonia_cliente,
                            'Telefono': nuevo_telefono_cliente,
                            'Correo': nuevo_correo_cliente,
                            'Fecha_registro': nueva_fecha_registro
                        },
                        'Articulos': {
                            'Nombre': nuevo_nombre_articulo,
                            'Precio': nuevo_precio_articulo,
                            'Descripciones': {
                                'Alto': nuevo_alto_articulo,
                                'Ancho': nuevo_ancho_articulo,
                                'Profundo': nuevo_profundo_articulo,
                                'Material': nuevo_material_articulo,
                                'Rasgos': nuevos_rasgos_articulo
                            },
                            'Tipo_transaccion': opc_mod
                        }
                    }

                    if st.button('Guardar cambios', key=f'guardar_cambios_{empeno["Num_Empenio"]}'):
                        modificar_empeno(empeno['Num_Empenio'], empeno['Categoria'], nuevos_datos)
                        st.success('Empeño modificado exitosamente')
                        st.rerun()

                if st.button(f'Eliminar {empeno["Num_Empenio"]}', key=f'eliminar_btn_{empeno["Num_Empenio"]}'):
                    if eliminar_empeno(empeno['Num_Empenio'], empeno['Categoria']):
                        st.success(f"Empeño {empeno['Num_Empenio']} - {empeno['Categoria']} eliminado exitosamente.")
                        st.rerun()
                    else:
                        st.error("Error al eliminar el empeño.")
    else:
        st.write("No hay empeños disponibles.")

    # Añadir Empeño
    with st.expander("Añadir Empeño"):
        siguiente_num_empenio = obtener_siguiente_num_empenio()
        st.write(f"Siguiente Número de Empeño: {siguiente_num_empenio}")
        categoria = st.text_input('Categoría', key='categoria_nuevo')
        monto_inicial = st.number_input('Monto inicial', min_value=0, step=1, key='monto_inicial_nuevo')
        cantidad_a_prestar = st.number_input('Cantidad a prestar', min_value=0, step=1, format='%d', key='cantidad_a_prestar_nuevo')
        cantidad_acumulada = st.number_input('Cantidad acumulada', min_value=0, step=1, format='%d', key='cantidad_acumulada_nuevo')
        mensualidades = st.number_input('Mensualidades', min_value=0, step=1, key='mensualidades_nuevo')
        fecha_empenio = st.date_input('Fecha de empeño', key='fecha_empenio_nuevo').strftime('%Y/%m/%d')
        nombre_cliente = st.text_input('Nombre del cliente', key='nombre_cliente_nuevo')
        calle_cliente = st.text_input('Calle del cliente', key='calle_cliente_nuevo')
        num_int = st.text_input('Número interior del cliente', key='num_int_nuevo')
        num_ext = st.text_input('Número exterior del cliente', key='num_ext_nuevo')
        cp_cliente = st.text_input('Código postal del cliente', key='cp_cliente_nuevo')
        estado_cliente = st.text_input('Estado del Cliente', key='estado_cliente_nuevo')
        municipio_cliente = st.text_input('Municipio/Alcaldía del Cliente', key='municipio_cliente_nuevo')
        colonia_cliente = st.text_input('Colonia del Cliente', key='colonia_cliente_nuevo')
        telefono_cliente = st.text_input('Teléfono del Cliente', key='telefono_cliente_nuevo')
        correo_cliente = st.text_input('Correo del Cliente', key='correo_cliente_nuevo')
        fecha_registro = st.date_input('Fecha de Registro', key='fecha_registro_nuevo').strftime("%Y/%m/%d")
        nombre_articulo = st.text_input('Nombre del Artículo', key='nombre_articulo_nuevo')
        precio_articulo = st.number_input('Precio del Artículo', min_value=0, step=1, format='%d', key='precio_articulo_nuevo')
        alto_articulo = st.number_input('Alto del Artículo', min_value=0, step=1, format='%d', key='alto_articulo_nuevo')
        ancho_articulo = st.number_input('Ancho del Artículo', min_value=0, step=1, format='%d', key='ancho_articulo_nuevo')
        profundo_articulo = st.number_input('Profundo del Artículo', min_value=0, step=1, format='%d', key='profundo_articulo_nuevo')
        material_articulo = st.text_input('Material del Artículo', key='material_articulo_nuevo')
        rasgos_articulo = st.text_input('Rasgos del Artículo', key='rasgos_articulo_nuevo')

        menu2 = ['Venta', 'Empeño']  # False = Venta, True = Empeño
        elec2 = st.selectbox('Selecciona una opción', menu2, key='elec2')

        if elec2 == 'Empeño':
            opc2 = True
        else:
            opc2 = False

        if st.button('Añadir Empeño', key='anadir_empeno'):
            nuevo_empeno = {
                'Num_Empenio': siguiente_num_empenio,
                'Categoria': categoria,
                'Monto_inicial': monto_inicial,
                'Cantidad_a_prestar': cantidad_a_prestar,
                'Cantidad_acumulada': cantidad_acumulada,
                'Mensualidades': mensualidades,
                'Fecha_empenio': fecha_empenio,
                'Cliente': {
                    'Nombre': nombre_cliente,
                    'Calle': calle_cliente,
                    'No_int': num_int,
                    'No_ext': num_ext,
                    'CP': cp_cliente,
                    'Estado': estado_cliente,
                    'Municipio_Alcaldia': municipio_cliente,
                    'Colonia': colonia_cliente,
                    'Telefono': telefono_cliente,
                    'Correo': correo_cliente,
                    'Fecha_registro': fecha_registro
                },
                'Articulos': {
                    'Nombre': nombre_articulo,
                    'Precio': precio_articulo,
                    'Descripciones': {
                        'Alto': alto_articulo,
                        'Ancho': ancho_articulo,
                        'Profundo': profundo_articulo,
                        'Material': material_articulo,
                        'Rasgos': rasgos_articulo
                    },
                    'Tipo_transaccion': opc2
                }
            }

            if agregar_empeno(nuevo_empeno):
                st.success('Empeño añadido exitosamente')
                st.rerun()
            else:
                st.error('Error al añadir el empeño.')
