# wiki-to-notion
Simple interface to import articles from wikipedia, getting the summary of each component and migrating it over to a notion database

To configure locally you have to enable the endpoint and submit the corresponding keys in the vars.py file, the requirements are:

openai_key = '#####' -> your openai user key (https://platform.openai.com/account/api-keys)

notion_token = '####' -> integration token (https://www.notion.so/my-integrations)

notion_database_id = '####' -> unique id from the database

You also need to grant access to the integration in the connections parameter of the database

Executing the py file will create a new page within the database with the desired columns

The required columns in de db are:

Title (page name)
Reviewed (checkbox)
Category (select)
Tags (multi-select)
Lan (select)
URL (url)
