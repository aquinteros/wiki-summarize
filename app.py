from resources.functions import *

def run():

    st.sidebar.markdown("""
        # About
        This app uses OpenAI's API to generate a summary of a Wikipedia article in a markdown format \n
        Easy to ingest into your Notion Database, Obsidian Vault, or any other markdown editor \n
        # How to Use
        To use it, you must have an OpenAI account and an API key. \n
        You can get your api key from this URL: <https://platform.openai.com/account/api-keys> \n
        Copy the URL of the Wikipedia article you want to summarize and click the "Summarize" button \n
        You can later download the result in a markdown format \n
        """
    )

    api_key_input = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="Paste your OpenAI API key 'sk-...'",
        value=st.session_state.get("OPENAI_API_KEY", ""),
    )
    
    st.sidebar.markdown("""
        Got any questions? \n
        Email me at: \n
        """
    )
    
    with st.sidebar:
        mention(
            label="alvaro.quinteros.a@gmail.com",
            icon="📧",
            url="mailto:alvaro.quinteros.a@gmail.com"
        )
    
    st.sidebar.markdown("""
        Or open an issue in the GitHub repo: \n
        """
    )  
    
    with st.sidebar:
        mention(
            label="wiki-summarize",
            icon="github",
            url="https://github.com/aquinteros/wiki-summarize"
        )
    
    colored_header("Wiki Summary", color_name='blue-70', description="Summarize Wikipedia articles in a markdown format")
    
    button(username="aquinteros", floating=False, width=221)

    URL = st.text_input("URL")
    
    url_parse = urlparse(URL)
    
    page_name = url_parse.path.split('/')[-1]
    language = url_parse.netloc.split('.')[0]
    
    model_list = []
    
    if api_key_input:
        validation = set_openai_api_key(api_key_input)
        if validation is True:
            models = pd.json_normalize(openai.Engine.list(), record_path=['data'])
            model_list = models[(models['owner'] == 'openai') & (models['ready'] == True)].id
        else:
            st.error('API key is not valid')
            st.error(validation)
            st.stop()
    
    model = st.selectbox("Model", model_list, index=len(model_list)-1)
    
    if st.button("Summarize"):
        
        if api_key_input:

            progress = st.progress(0)
            
            output = return_summary(page_name, model, progress, language)
            
            progress.progress(100)

            st.download_button('Download Markdown', output, page_name + ".md", "Download")

            st.markdown(output)
            
        else:
            st.error("Please enter your OpenAI API key")

if __name__ == "__main__":
    run()
