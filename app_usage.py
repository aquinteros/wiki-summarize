import requests

concepto = 'Patricio Bañados'
lan = 'ES'

concepto = concepto.replace(' ', '%20')
url = 'http://3.18.221.79:5000/wtn?concept=' + concepto + '&language=' + lan

print(url)

response = requests.get(url)

print(response)