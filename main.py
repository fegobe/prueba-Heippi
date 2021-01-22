import requests

respuesta= requests.get('http://ddragon.leagueoflegends.com/cdn/11.1.1/data/es_MX/champion.json').json()


for i in respuesta['data']:
    print (respuesta['data'][i]['name'])

