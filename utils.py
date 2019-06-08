import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "get-meanings-lasbbk"


from PyDictionary import PyDictionary

dictionary=PyDictionary()

from pymongo import MongoClient
m_client=MongoClient("mongodb+srv://test:test@cluster0-bx7xl.mongodb.net/test?retryWrites=true&w=majority")

db=m_client.get_database('dictionary_db')
records=db.dictionary_records

def get_meanings(parameters):
	word = parameters.get('dict_type')
	return word

def get_translate(parameters):
	language=parameters.get('dict_2type')
	print(language)
	return language


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def fetch_reply(msg, session_id):
	response = detect_intent_from_text(msg, session_id)
	if response.intent.display_name == 'get_meanings':
		meaning = get_meanings(dict(response.parameters))
		#records.insert_one({'Word':meaning})
		actualMean = dictionary.meaning(meaning)
		res = "{}".format(actualMean['Noun'])
		dictdb={
			'word':meaning,
			'meaning':res
		}
		records.insert_one(dictdb)
		return res
	if response.intent.display_name == 'get_translate':
		meaning = get_meanings(dict(response.parameters))
		translate = get_translate(dict(response.parameters))
		print(meaning+"is"+translate)
		actualtranslate=dictionary.translate(meaning,translate)
		res = "{}".format(actualtranslate)
		return res
	else:
		return response.fulfillment_text