import watson_developer_cloud
import requests
import json
import pprint

conversation = watson_developer_cloud.ConversationV1(
  username = '0967e618-5534-4a0e-87b8-329a7849af63',
  password = 'TZIJR0ywVlsw',
  version = '2017-05-26'
)

def wat(q):
    mr = conversation.message(
		workspace_id = 'e1e56ea1-f07e-4fdd-8b86-67d9954078cf',
		message_input = {
			'text' : q
		}
	)
    text = mr["output"]["text"][0]
    return text

def wolf(q):
    if "graph" in q:
        payload = {'i' : q}
        r = requests.get('http://api.wolframalpha.com/v1/simple?appid=2HAULH-VTUJJEJ65R', params = payload)
        return r.url
    else:
        payload = {'i' : q, 'output' : 'json'}
        queryCheck = requests.get("http://www.wolframalpha.com/queryrecognizer/query.jsp?appid=DEMO&mode=Default", params = payload)
        if queryCheck.json()['query'][0]['accepted'] == "true":
            result = requests.get("http://api.wolframalpha.com/v1/result?appid=2HAULH-VTUJJEJ65R", params = payload)
            if result.text != "No short answer available" and result.text != "Wolfram|Alpha did not understand your input":
                return result.text
        return "Sorry, I don't understand what you're trying to ask."

def poke(q):
    response = requests.get('https://pokeapi.co/api/v2/pokemon/' + q)
    p = response.json()
    sprite = p['sprites']['front_default']
    base = p['stats']

    #Getting main ability information and creating Dict
    abDict = {}
    abilities = p['abilities']
    mainAbility = ""
    for ab in abilities:
        if not ab['is_hidden']:
            mainAbility = ab['ability']['name']
    abResponse = requests.get('https://pokeapi.co/api/v2/ability/' + mainAbility)
    abObject = abResponse.json()
    abText = abObject["effect_entries"][0]["short_effect"]
    abDict['name'], abDict['desc'] = mainAbility, abText

    #Parsing Base Stats
    base_dict = {}
    for i in base:
        name = i['stat']['name']
        base_dict[name] = i['base_stat']

    return(base_dict, q, sprite,abDict)
