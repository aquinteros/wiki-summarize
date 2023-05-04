
import pandas as pd
import wikipediaapi
import openai
import json
import requests

from vars import openai_key, notion_token, notion_database_id

openai.api_key = openai_key

concept = 'Minecraft'
language = 'en'

categorias = pd.read_csv('resources/cat.csv', header=None, index_col=0).index.tolist()

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    """function to return content from the openai api prompt"""
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]

def import_wiki_page(page_name , language = 'en'):
	"""Importa una página de wikipedia"""
	wiki = wikipediaapi.Wikipedia(language)
	page = wiki.page(page_name)
	exists = page.exists()
	summary = page.summary
	url = page.fullurl
	sections = page.sections
	return page_name, exists, summary, url, sections

def get_summary(page_name, summary):
	"""Trae summary de una página de wikipedia"""

	prompt = f"""
	Tu tarea es generar un resumen corto de un Artículo de wikipedia sobre {page_name} delimitado en triple comillas simples en no más de 40 palabras
	Conserva el tono informativo e impersonal del artículo.
	Omite información de poca relevancia.
	Clasifíca el artículo en una de las siguientes categorías: {categorias}
	Deriva una lista de como máximo 3 keywords principales del artículo
    El idioma del output es siempre el mismo idioma que el artículo.
	El formato de salida SIEMPRE debe ser JSON con los siguientes valores de llave:	[summary, category, keywords].
	Artículo: '''{summary}'''
	"""

	response = json.loads(get_completion(prompt))

	return response['summary'], response['category'], response['keywords']

def get_section_summary(page_name, section):
	"""Trae summary de una sección de wikipedia"""
	
	prompt = f"""
	Tu tarea es generar un resumen corto de una sección de un Artículo de wikipedia sobre {page_name} delimitada en triple comillas simples en no más de 40 palabras
	Conserva el tono informativo e impersonal de la sección.
	Omite información de poca relevancia, no incluyas información de otras secciones.
	El formato de salida debe ser texto plano en el ideoma original del artículo.
	Artículo: '''{section}'''
	"""

	response = get_completion(prompt)

	return response

def createPage(databaseID, headers, page_name, summary, url, sections, language):
    """crea una página en una database de notion"""
    
    resumen, categoria, tags = get_summary(page_name, summary)
    
    createUrl = 'https://api.notion.com/v1/pages'
    newPageData = {
        "parent": { "database_id": databaseID },
        "object": "page",
        "properties": {
            "Título": {
                "title": [
                    {
                        "text": {
                            "content": page_name
                        }
                    }
                ]
            },
            "Tags": {
                    "multi_select":[
                    ]
                },
            "Categoría": {
                "select": {
                    "name": categoria
                }
            },
            "Revisada": {
                    "checkbox": False
                },
            "URL": {
                "url": url
            },
            "Idioma": {
				"select": {
					"name": str.upper(language)
				}
			},
            }
        }
    
    for tag in tags:
        newPageData["properties"]["Tags"]["multi_select"].append({"name": tag})
        
    data = json.dumps(newPageData)

    res_insert = requests.request("POST", createUrl, headers=headers, data=data)
    print(res_insert.status_code)

    newPageID = json.loads(res_insert.content)["id"]
    
    newPageData = {
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": page_name
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": resumen
                            }
                        }
                    ]
                }
            }
        ]
    }

    excluded_titles = ['Referencias', 'Véase también', 'Enlaces externos', 'Notas', 'Bibliografía', 'Notes', 'References', 'External links', 'See also', 'Further reading']

    for section in sections:
        if section.title not in excluded_titles:
            newPageData["children"].append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": section.title
                                }
                            }
                        ]
                    }
                })
            newPageData["children"].append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": get_section_summary(page_name, section.full_text)
                                }
                            }
                        ]
                    }
                })

    data = json.dumps(newPageData)

    updateURL = f'https://api.notion.com/v1/blocks/{newPageID}/children'
    res_update = requests.request("PATCH", updateURL, headers=headers, data=data)
    print(res_update.status_code)

headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

page_name, exists, summary, url, sections = import_wiki_page(concept, language)

if exists:
    createPage(notion_database_id, headers, page_name, summary, url, sections, language)
