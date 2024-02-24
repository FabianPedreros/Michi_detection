import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input_prompt, image[0]])
    except:
        return st.write("Lo siento, no he podido distinguir el gato, prueba subiendo otra imagen")

    return response.text

def scale_image(uploaded_file, max_size=(800, 800)):
    if uploaded_file is not None:
        # Abre la imagen y redimensiona
        image = Image.open(uploaded_file)
        image.thumbnail(max_size)

        # Convierte la imagen redimensionada a bytes
        with BytesIO() as output_buffer:
            image.save(output_buffer, format="JPEG")  
            bytes_data = output_buffer.getvalue()

        return bytes_data
    else:
        raise FileNotFoundError("No se ha cargado un archivo")

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = scale_image(uploaded_file)
        
        image_parts = [{
            "mime_type": "image/jpeg",  
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No se ha cargado un archivo")

st.set_page_config(page_title="Identificador de michis", page_icon=":cat:")
st.header("Identifica la raza y patrones de colores de los gatos")

input_type_selected = st.radio("Como deseas cargar la imagen de tu michi?:", ["Tomar Foto", "Cargar Imagen"])

if input_type_selected == "Tomar Foto":
    uploaded_file = st.camera_input("Toma una foto...")
    image = ""
else: 
    uploaded_file = st.file_uploader("Selecciona una imagen...", type=["jpg", "jpeg", "png"])
    image = "" 
    
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)

submit = st.button("Dame información acerca de mi michi")

input_prompt = """
                Eres un veterinario experto en gatos, eres capaz de distinguir entre las distintas razas de gatos como lo pueden ser (American Curl, Azul Ruso, Angora, Bengala, Bombay, Persa, Siberiano, etc.) 
                y distingues los patrones de colores de su pelaje, pudiendo establecer si un gato es atigrado o no, los colores de su pelaje omo lo pueden ser naranja, calico, blancos, negros, etc..

                Tambien puedes establecer la edad de un gato, indicando la cantidad de meses o anos que tiene de edad, y por lo tanto establecer si se trata de un: 
                cachorro (0 a seis meses), joven (siete meses a dos anos), adulto (tres a seis anos), maduro (siete a diez anos), senior (11 a 14 anos), o anciano (15 anos o mas)

                Eres capaz de entregar informacion de interes concisa y en no mas de 100 palabras acerca de la raza, color, patron de pelaje y edad del gato, asi como de establecer si se encuentra saludable o no.

                Das consejos acerca del cuidado especifico del tipo de gato teniendo en cuenta la raza, color, patron de pelaje, edad del gato y el estado de salud. La informacion brindada
                es concisa y no excede las 100 palabras.

                Valoras la belleza del gato, por lo que puedes decir de manera tierna y amigable que tan bello es el gato.

                La informacion brindada debe partir de la imagen del gato.

                Este es el formato que usas para entregar la informacion:

                - Raza del gato:

                - Patron del pelaje:

                - Color del gato:

                - Edad aproximada:

                - Informacion de interes:

                - Consejos de cuidado:

                - Nivel de belleza:

                """

if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.header("Esta es la información de tu michi:")
        st.write(response)
    except:
        st.write("Lo siento, no he podido distinguir el gato, prueba subiendo otra imagen")
