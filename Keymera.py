import streamlit as st
import boto3
import pandas as pd
from decimal import Decimal

# Configurar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='fakeMyKeyId', aws_secret_access_key='fakeSecretAccessKey')


# Tablas de DynamoDB

empenios_table = dynamodb.Table('Empenios')
ventas_table = dynamodb.Table('Ventas')

# Función para añadir un empeño
def agregar_empeno(datos_empeno):
    empenios_table.put_item(Item=datos_empeno)

# Función para obtener todos los empeños
def obtener_empenos():
    response = empenios_table.scan()
    return response['Items']

# Funcion para eliminar un empeño
def eliminar_empeno(id_empeno, categoria):
    empenios_table.delete_item(Key={'Num_Empenio': id_empeno, 'Categoria': categoria})

# Función para obtener todas las ventas
def obtener_ventas():
    response = ventas_table.scan()
    return response['Items']

# Funcion para convertir a decimal
def convert_to_decimal(data):
    if isinstance(data, list):
        return [convert_to_decimal(i) for i in data]
    elif isinstance(data, dict):
        return {k: convert_to_decimal(v) for k, v in data.items()}
    elif isinstance(data, float):
        return Decimal(str(data))
    return data

st.title('Sistema de Empeños y Ventas')

menu = ['Listado de Empeños', 'Listado de Ventas', 'Añadir Empeño', 'Añadir Venta']
eleccion = st.sidebar.selectbox('Selecciona una opción', menu)

# CSS para la tabla
st.markdown("""
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #f2f2f2;
        }
        .actions {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

if eleccion == 'Listado de Empeños':
    st.subheader('Listado de Empeños')
    empenios = obtener_empenos()

    if empenios:
        st.write(f"<table><tr><th>Número de Empeño</th><th>Categoría</th><th>Monto Inicial</th><th>Cantidad Acumulada</th><th>Cantidad a prestar</th><th>Nombre del articulo</th><th>Precio</th><th>Alto (cm)</th><th>Ancho (cm)</th><th>Profundo (cm)</th><th>Detalles</th><th>Material</th><th>Nombre del cliente</th><th>Calle</th><th>No. Interior</th><th>No. Exterior</th><th>C.P.</th><th>Estado</th><th>Municipio o Alcaldia</th><th>Colonia</th><th>Telefono</th><th>Correo</th><th>Acciones</th></tr>", unsafe_allow_html=True)
        for empeno in empenios:
            articulos = empeno['Articulos']
            cliente = empeno['Cliente']
            medidas = articulos['Descripciones']
            st.write(f"<tr><td>{empeno['Num_Empenio']}</td><td>{empeno['Categoria']}</td><td>{empeno['Monto_inicial']}</td><td>{empeno['Cantidad acumulada']}</td><td>{empeno['Cantidad a prestar']}</td><td>{articulos['Nombre']}</td><td>{articulos['Precio']}</td><td>{medidas['Alto']}</td><td>{medidas['Ancho']}</td><td>{medidas['Profundo']}</td><td>{medidas['Rasgos']}</td><td>{medidas['Material']}</td><td>{cliente['Nombre']}</td><td>{cliente['Calle']}</td><td>{cliente['No_int']}</td><td>{cliente['No_ext']}</td><td>{cliente['CP']}</td><td>{cliente['Estado']}</td><td>{cliente['Municipio/Alcaldía']}</td><td>{cliente['Colonia']}</td><td>{cliente['Telefono']}</td><td>{cliente['Correo']}</td><td>", unsafe_allow_html=True)
            if st.button('Modificar'):
                with st.form(key=f'modificar_empeno_{empeno["Num_Empenio"]}_{empeno["Categoria"]}'):
                    nuevos_datos = {}
                    for key, value in empeno.items():
                        if key not in ["Num_Empenio", "Categoria"]:
                            if isinstance(value, dict):
                                for sub_key, sub_value in value.items():
                                    nuevos_datos[f"{key}.{sub_key}"] = st.text_input(f"{key}.{sub_key}", value=sub_value)
                            else:
                                nuevos_datos[key] = st.text_input(key, value=value)
                    if st.form_submit_button("Guardar cambios"):
                        #modificar_empeno(empeno['Num_Empenio'], empeno['Categoria'], convert_to_decimal(nuevos_datos))
                        st.success(f"Empeño {empeno['Num_Empenio']} - {empeno['Categoria']} modificado exitosamente.")
                        st.experimental_rerun()
            if st.button('Eliminar'):
                eliminar_empeno(empeno['Num_Empenio'], empeno['Categoria'])
                st.success(f"Empeño {empeno['Num_Empenio']} - {empeno['Categoria']} eliminado exitosamente.")
                st.experimental_rerun()
            st.write("</td></tr>", unsafe_allow_html=True)
        st.write("</table>", unsafe_allow_html=True)
    else:
        st.write("No hay empeños disponibles.")

elif eleccion == 'Añadir Empeño':
    st.subheader('Añadir Empeño')
    num_empenio = st.number_input('Número de empeño', min_value=0, step=1, format='%d')
    categoria = st.text_input('Categoría')
    monto_inicial = st.number_input('Monto inicial', min_value=0, step=1)
    cantidad_a_prestar = st.number_input('Cantidad a prestar', min_value=0, step=1, format='%d')
    cantidad_acumulada = st.number_input('Cantidad acumulada', min_value=0, step=1, format='%d')
    mensualidades = st.number_input('Mensualidades', min_value=0, step=1)
    fecha_empenio = st.date_input('Fecha de empeño').strftime('%Y/%m/%d')
    nombre_cliente = st.text_input('Nombre del cliente')
    calle_cliente = st.text_input('Calle del cliente')
    num_int = st.text_input('Número interior del cliente')
    num_ext = st.text_input('Número exterior del cliente')
    cp_cliente = st.text_input('Código postal del cliente')
    estado_cliente = st.text_input('Estado del Cliente')
    municipio_cliente = st.text_input('Municipio/Alcaldía del Cliente')
    colonia_cliente = st.text_input('Colonia del Cliente')
    telefono_cliente = st.text_input('Teléfono del Cliente')
    correo_cliente = st.text_input('Correo del Cliente')
    fecha_registro = st.date_input('Fecha de Registro').strftime("%Y/%m/%d")
    nombre_articulo = st.text_input('Nombre del Artículo')
    precio_articulo = st.number_input('Precio del Artículo', min_value=0, step=1, format='%d')
    alto_articulo = st.number_input('Alto del Artículo', min_value=0, step=1, format='%d')
    ancho_articulo = st.number_input('Ancho del Artículo', min_value=0, step=1, format='%d')
    profundo_articulo = st.number_input('Profundo del Artículo', min_value=0, step=1, format='%d')
    material_articulo = st.text_input('Material del Artículo')
    rasgos_articulo = st.text_input('Rasgos del Artículo')

    if st.button('Añadir Empeño'):
        nuevo_empeno = {
            'Num_Empenio': int(num_empenio),
            'Categoria': categoria,
            'Monto_inicial': monto_inicial,
            'Cantidad a prestar': cantidad_a_prestar,
            'Cantidad acumulada': cantidad_acumulada,
            'Mensualidades': mensualidades,
            'Cliente': {
                'Nombre': nombre_cliente,
                'Calle': calle_cliente,
                'No_int': num_int,
                'No_ext': num_ext,
                'CP': cp_cliente,
                'Estado': estado_cliente,
                'Municipio/Alcaldia': municipio_cliente,
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
                }
            }
        }

        agregar_empeno(nuevo_empeno)
        st.success('Empeño añadido exitosamente')