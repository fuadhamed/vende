import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Configuración de la página
st.set_page_config(page_title="Extracción de Vendedores", layout="wide")
st.title("🌐 Extracción de Vendedores")

# Función para extraer vendedores usando tu código
def extract_sellers(url):
    try:
        # Configurar Selenium
        options = Options()
        driver = webdriver.Chrome(options=options)
        
        # Abrir la URL
        driver.get(url)
        time.sleep(5)  # Esperar a que la página cargue completamente
        
        # Obtener el código fuente de la página
        page_source = driver.page_source
          # Cerrar el navegador
        
        # Parsear el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Extraer los nombres de los vendedores
        sellers = soup.find_all("b", {"class": "jsx-2325455629 title1 secondary jsx-3451706699 bold pod-title title-rebrand"})
        seller_list = [seller.text.strip() for seller in sellers]
        
        return seller_list
    except Exception as e:
        st.error(f"Error al extraer datos: {e}")
        return []

# Interfaz de usuario
st.header("🔍 Ingresa una URL para extraer vendedores")
url = st.text_input("URL", placeholder="https://www.falabella.com/falabella-cl/category/cat3180021/Camas-infantiles")

if url:
    st.write(f"Extrayendo vendedores de: {url}")
    
    # Extraer vendedores
    sellers = extract_sellers(url)
    
    if sellers:
        # Mostrar los vendedores en una tabla
        st.subheader("📊 Vendedores Extraídos")
        df = pd.DataFrame(sellers, columns=["Vendedor"])
        st.dataframe(df)
        
        # Permitir descargar los datos
        st.subheader("📥 Descargar Datos")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar como CSV",
            data=csv,
            file_name="vendedores_extraidos.csv",
            mime="text/csv"
        )
    else:
        st.warning("No se encontraron vendedores en la página.")