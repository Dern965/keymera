import streamlit as st
import boto3
from botocore.exceptions import ClientError

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

# Función para eliminar un empeño
def eliminar_empeno(id_empeno, categoria):
    empenios_table.delete_item(Key={'Num_Empenio': id_empeno, 'Categoria': categoria})

# Función para modificar un empeño
def modificar_empeno(num_empenio, categoria, nuevos_datos):
    nuevos_datos['Num_Empenio'] = num_empenio
    nuevos_datos['Categoria'] = categoria
    agregar_empeno(nuevos_datos)
    eliminar_empeno(num_empenio, categoria)

st.title('Sistema de Empeños y Ventas')

menu = ['Listado de Empeños', 'Añadir Empeño']
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

                if st.button(f'Modificar {empeno["Num_Empenio"]}'):
                    with st.form(key=f'modificar_empeno_{empeno["Num_Empenio"]}_{empeno["Categoria"]}'):
                        nuevos_datos = {}
                        for key, value in empeno.items():
                            if key not in ["Num_Empenio", "Categoria"]:
                                if isinstance(value, dict):
                                    nuevos_datos[key] = {}
                                    for sub_key, sub_value in value.items():
                                        nuevos_datos[key][sub_key] = st.text_input(f"{key}.{sub_key}", value=sub_value)
                                else:
                                    nuevos_datos[key] = st.text_input(key, value=value)
                        if st.form_submit_button("Guardar cambios"):
                            modificar_empeno(empeno['Num_Empenio'], empeno['Categoria'], nuevos_datos)
                            st.success(f"Empeño {empeno['Num_Empenio']} - {empeno['Categoria']} modificado exitosamente.")
                            st.rerun()
                if st.button(f'Eliminar {empeno["Num_Empenio"]}'):
                    eliminar_empeno(empeno['Num_Empenio'], empeno['Categoria'])
                    st.success(f"Empeño {empeno['Num_Empenio']} - {empeno['Categoria']} eliminado exitosamente.")
                    st.rerun()
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

    menu2 = ['Venta', 'Empeño']  # False = Venta, True = Empeño
    st.write('Selecciona si es un artículo de empeño o venta')
    eleccion2 = st.selectbox('Selecciona una opción', menu2)
    opc = eleccion2 == 'Empeño'

    if st.button('Añadir Empeño'):
        nuevo_empeno = {
            'Num_Empenio': int(num_empenio),
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
                'Tipo_transaccion': opc
            }
        }

        agregar_empeno(nuevo_empeno)
        st.success('Empeño añadido exitosamente')
