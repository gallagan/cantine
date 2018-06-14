from sanic import Sanic
from sanic import response
import aiohttp
import asyncio
import re
import json
import requests
import string
import urllib

app = Sanic(__name__)
# -*- coding: UTF-8

#CONFIG
VERSION = '0.1.1'

entree = ""
plat = ""
garniture = ""
fromage = ""
dessert = ""
gouter = ""

from datetime import date

weekNumber = date.today().isocalendar()[1]
dayNumber = date.today().isocalendar()[2]

try:
    r = requests.get('https://cantine-json.firebaseio.com/menus.json', timeout=120)
except:
    exit('ERREUR API')


data = json.loads(json.dumps(r.json()))

if dayNumber > 5:
  weekNumber = weekNumber+1
  dayNumber = 0
else:
  dayNumber = dayNumber-1


codeSemaine = "2018-"+str(weekNumber)


x = 0

for jsondata in data['json']:
    try:
    	if jsondata['codeSemaine'] == codeSemaine:
          x = 0
          for jsonentree in jsondata['menus'][dayNumber]['repas'][0]['famillesPlat'][0]['plats']:
              #print(jsonentree['name'].encode('utf-8'))
              x = x+1
              if x > 1:
              	entree = entree + ' et ' + jsonentree['name'].encode('utf-8')
              else:
                entree = jsonentree['name'].encode('utf-8')
          x = 0
          for jsonplat in jsondata['menus'][dayNumber]['repas'][0]['famillesPlat'][1]['plats']:
              #print(jsonplat['name'].encode('utf-8'))
              x = x+1
              if x > 1:
              	plat = plat + ' et ' + jsonplat['name'].encode('utf-8')
              else:
                plat = jsonplat['name'].encode('utf-8')
          x = 0
          for jsongarniture in jsondata['menus'][dayNumber]['repas'][0]['famillesPlat'][2]['plats']:
              #print(jsongarniture['name'].encode('utf-8'))
              x = x+1
              if x > 1:
              	garniture = garniture + ' et ' + jsongarniture['name'].encode('utf-8')
              else:
                garniture = jsongarniture['name'].encode('utf-8')
          x = 0
          for jsonfromage in jsondata['menus'][dayNumber]['repas'][0]['famillesPlat'][3]['plats']:
              #print(jsonfromage['name'].encode('utf-8'))
              x = x+1
              if x > 1:
                fromage = fromage + ' et ' + jsonfromage['name'].encode('utf-8')
              else:
              	fromage = jsonfromage['name'].encode('utf-8')
          x = 0
          for jsondessert in jsondata['menus'][dayNumber]['repas'][0]['famillesPlat'][4]['plats']:
              #print(jsondessert['name'].encode('utf-8'))
              x = x+1
              if x > 1:
              	dessert = dessert + ' et ' + jsondessert['name'].encode('utf-8')
              else:
              	dessert = jsondessert['name'].encode('utf-8')
          #print('Entree: ' + entree + ' - Plat: ' + plat + ' - Garniture: ' + garniture + ' - Fromage: ' + fromage + ' - Dessert: ' + dessert)

          for jsongouter_full in jsondata['menus'][dayNumber]['repas'][1]['famillesPlat']:
            #x=0
            for jsongouter in jsongouter_full['plats']:
             	gouter = gouter + jsongouter['name'].encode('utf-8') + ', '

          gouter = gouter + '##'
          gouter = gouter.replace(', ##', '.')
          json = "En entrée : "+entree+", pour le plat, "+plat+" accompagné de "+garniture+". Pour le fromage / laitage, "+fromage+" et enfin, en dessert, "+dessert+". Et pour le goûter, "+gouter+"."
          json='{"retour":"'+json+'"}'
          INDEX=json
          #print json
    except:
      	#print('Pas de menu disponible')


#INDEX = """<!DOCTYPE html>
#<title>json-head</title>
#<h1>json-head</h1>
#<p>JSON (and JSON-P) API for running a HEAD request against a URL.
#<ul>
#    <li><a href="/?url=http://www.google.com/">/?url=http://www.google.com/</a>
#    <li><a href="/?url=http://www.yahoo.com/&amp;callback=foo">/?url=http://www.yahoo.com/&amp;callback=foo</a>
#    <li><a href="/?url=https://www.google.com/&amp;url=http://www.yahoo.com/">/?url=https://www.google.com/&amp;url=http://www.yahoo.com/</a>
#</ul>
#<p>Background: <a href="https://simonwillison.net/2017/Oct/14/async-python-sanic-now/">Deploying an asynchronous Python microservice with Sanic and Zeit Now</a></p>
#<p>Source code: <a href="https://github.com/simonw/json-head">github.com/simonw/json-head</a></p>
#"""

callback_re = re.compile(r'^[a-zA-Z_](\.?[a-zA-Z0-9_]+)+$')
is_valid_callback = callback_re.match


async def head(session, url):
    try:
        async with session.head(url) as response:
            return {
                'ok': True,
                'headers': dict(response.headers),
                'status': response.status,
                'url': url,
            }
    except Exception as e:
        return {
            'ok': False,
            'error': str(e),
            'url': url,
        }


@app.route('/')
async def handle_request(request):
    return response.html(INDEX)
    #urls = request.args.getlist('url')
    #callback = request.args.get('callback')
    #if urls:
    #    if len(urls) > 10:
    #        return response.json([{
    #            'ok': False,
    #            'error': 'Max 10 URLs allowed'
    #        }], status=400)
    #    async with aiohttp.ClientSession() as session:
    #        head_infos = await asyncio.gather(*[
    #            head(session, url) for url in urls
    #        ])
    #        if callback and is_valid_callback(callback):
    #            return response.text(
    #                '{}({})'.format(callback, json.dumps(head_infos, indent=2)),
    #                content_type='application/javascript',
    #                headers={'Access-Control-Allow-Origin': '*'},
    #            )
    #        else:
    #            return response.json(
    #                head_infos,
    #                headers={'Access-Control-Allow-Origin': '*'},
    #            )
    #else:
    #    return response.html(INDEX)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8006)
