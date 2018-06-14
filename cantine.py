from sanic import Sanic
from sanic import response
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

@app.route('/')


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
          return response.text(json)
    except:
      	return response.text('Pas de menu disponible')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8006)
