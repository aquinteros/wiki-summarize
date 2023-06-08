
# def createPage(databaseID, headers, page_name, summary, url, sections, language):
#         """crea una página en una database de notion y pobla la página con los datos del artículo de wikipedia"""
        
#         resumen, categoria, tags = get_summary(page_name, summary, language)
        
#         createUrl = 'https://api.notion.com/v1/pages'
#         newPageData = {
#             "parent": { "database_id": databaseID },
#             "object": "page",
#             "properties": {
#                 "Title": {
#                     "title": [
#                         {
#                             "text": {
#                                 "content": page_name
#                             }
#                         }
#                     ]
#                 },
#                 "Tags": {
#                         "multi_select":[
#                         ]
#                     },
#                 "Category": {
#                     "select": {
#                         "name": categoria
#                     }
#                 },
#                 "Reviewed": {
#                         "checkbox": False
#                     },
#                 "URL": {
#                     "url": url
#                 },
#                 "Lan": {
#                     "select": {
#                         "name": str.upper(language)
#                     }
#                 },
#                 }
#             }
        
#         for tag in tags:
#             newPageData["properties"]["Tags"]["multi_select"].append({"name": tag})
            
#         data = json.dumps(newPageData)

#         res_insert = requests.request("POST", createUrl, headers=headers, data=data)

#         newPageID = json.loads(res_insert.content)["id"]
        
#         newPageData = {
#             "children": [
#                 {
#                     "object": "block",
#                     "type": "heading_1",
#                     "heading_1": {
#                         "rich_text": [
#                             {
#                                 "type": "text",
#                                 "text": {
#                                     "content": page_name
#                                 }
#                             }
#                         ]
#                     }
#                 },
#                 {
#                     "object": "block",
#                     "type": "paragraph",
#                     "paragraph": {
#                         "rich_text": [
#                             {
#                                 "type": "text",
#                                 "text": {
#                                     "content": resumen
#                                 }
#                             }
#                         ]
#                     }
#                 }
#             ]
#         }

#         excluded_titles = ['Referencias', 'Véase también', 'Enlaces externos', 'Fuentes', 'Notas', 'Bibliografía', 'Notes', 'References', 'External links', 'See also', 'Further reading' ,'Sources']

#         for section in sections:
#             if section.title not in excluded_titles:
#                 newPageData["children"].append({
#                         "object": "block",
#                         "type": "heading_2",
#                         "heading_2": {
#                             "rich_text": [
#                                 {
#                                     "type": "text",
#                                     "text": {
#                                         "content": section.title
#                                     }
#                                 }
#                             ]
#                         }
#                     })
#                 newPageData["children"].append({
#                         "object": "block",
#                         "type": "paragraph",
#                         "paragraph": {
#                             "rich_text": [
#                                 {
#                                     "type": "text",
#                                     "text": {
#                                         "content": get_section_summary(page_name, section.full_text, language)
#                                     }
#                                 }
#                             ]
#                         }
#                     })

#         data = json.dumps(newPageData)

#         updateURL = f'https://api.notion.com/v1/blocks/{newPageID}/children'
#         res_update = requests.request("PATCH", updateURL, headers=headers, data=data)
#         # return res_update.status_code, res_insert.status_code
#         return str(res_insert.status_code) + " " + str(res_update.status_code)

# def flow_to_notion(page_name, headers, lan='en'):
# 	"""Función que ejecuta el flujo completo para importar una página de wikipedia a Notion"""
    
# 	page_name, exists, summary, url, sections = import_wiki_page(page_name, lan)

# 	if exists:
# 		result = createPage(notion_database_id, headers, page_name, summary, url, sections, lan)
# 	else:
# 		result = "No existe la página"

# 	return result