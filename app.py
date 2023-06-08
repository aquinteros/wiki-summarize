from resources.functions import *

def run():

    # headers = {
    # "Authorization": "Bearer " + notion_token,
    # "Content-Type": "application/json",
    # "Notion-Version": "2022-06-28"
    # }
    
    headers = {
        "Authorization": st.secrets["openai_key"],
        "Content-Type": "application/json",
    }

    st.title("Wiki Summary")

    st.text("Importa un resumen de una página de Wikipedia a Notion")

    page_name = st.text_input("Nombre de la página")

    language = st.selectbox("Idioma", ['en', 'es'])

    if st.button("Importar"):

        output = return_summary(page_name, language)
        
        st.download_button('Descarga MD', output, page_name + ".md", "Descargar")

        st.markdown(output)

if __name__ == "__main__":
    run()