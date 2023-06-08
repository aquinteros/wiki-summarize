from resources.functions import *

def run():

    st.sidebar.markdown("""
        # About
        This app uses OpenAI's API to generate a summary of a Wikipedia article in a markdown format \n
        Easy to ingest into your Notion Database, Obsidian Vault, or any other markdown editor \n
        # How to Use
        To use it, you must have an OpenAI account and an API key. \n
        You can get your api key from this URL: <https://platform.openai.com/account/api-keys> \n
        Search the title of the Wikipedia article you want to summarize and click the "Import" button
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
        Email me at: [alvaro.quinteros.a@gmail.com](mailto:alvaro.quinteros.a@gmail.com) \n
        Or open a GitHub issue at: <https://github.com/aquinteros/wiki-summarize>
        """
    )
        
    st.title("Wiki Summary")

    st.text("Makes a summary of a Wikipedia article in a markdown format")

    page_name = st.text_input("Page Name")

    language = st.selectbox("Lang", ['en', 'es'])
    
    model_list = []
    
    if api_key_input:
        set_openai_api_key(api_key_input)
        models = pd.json_normalize(openai.Engine.list(), record_path=['data'])
        model_list = models[(models['owner'] == 'openai') & (models['ready'] == True)].id
    
    model = st.selectbox("Model", model_list, index=len(model_list)-1)
    
    if st.button("Summarize"):
        
        if api_key_input:

            output = return_summary(page_name, model, language)

            st.download_button('Download Markdown', output, page_name + ".md", "Download")

            st.markdown(output)
            
        else:
            st.error("Please enter your OpenAI API key")

if __name__ == "__main__":
    run()
