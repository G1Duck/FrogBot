import urllib.request
import json

api_key = 'FILLMEIN'

places = ( 'Cranham', 'Belfast' )

for place in places:
  url = 'http://api.openweathermap.org/data/2.5/weather?q={0},uk&appid={1}'.format(place, api_key)
  response = urllib.request.urlopen(url)

  result = json.loads(response.read())

  print(place, ":", result['weather'][0]['main'], ":", result['weather'][0]['description'])
