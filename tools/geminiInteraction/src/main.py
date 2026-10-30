import datetime

from google import genai
from google.genai import types

import json
import typing_extensions as typing
import textwrap

class Interact():
	INSTRUCT="Based on the input given, generate 4 questions which a user might interested in asking you which are relevant to the context of the current weather report you are receiving. The output question must be a single short sentence, ending in a question mark. Sample categories of questions include (but are not limited to): appropriate clothing or gear to wear or carry, preparing for exposure to elements, outdoor (or indoor) activities, weather safety information, record highs and lows, seasonability of current conditions for the current and nearby locations, historically significant weather events, astrological events and sky visibility."
	INPUT=[
	"""
	{
		"location": "Los Angeles city, CA",
		"dateTime": "2025-04-10T23:37:53.836Z",
		"temperature": "70.0F",
		"skyConditions": "clear",
		"weather": null,
		"humidity": "56%",
		"wind": "from the SSW (210 degrees) at 8 MPH (7 KT):0"
	}
	""",
	"""
	{
		"location": "Gainesville city, GA",
		"dateTime": "2025-04-11T00:03:23.603Z",
		"temperature": "53.1F",
		"skyConditions": "overcast",
		"weather": "heavy rain with thunder; Lightning observed",
		"humidity": "82%",
		"wind": "from the N (010 degrees) at 14 MPH (12 KT) gusting to 29 MPH (25 KT):0"
	}
	""",
	"""
	{
		"location": "Everett city, WA",
		"dateTime": "2025-04-11T00:03:08.191Z",
		"temperature": "55.0F",
		"skyConditions": "mostly cloudy",
		"weather": null,
		"humidity": "74%",
		"wind": "from the S (190 degrees) at 26 MPH (23 KT) gusting to 45 MPH (39 KT):0"
	}
	"""
	]
	SCHEMA="""
	{
	  "type": "array",
	  "items": {
	    "type": "object",
	    "properties": {
	      "category": {
	        "type": "string",
	        "enum": [
	          "tmyk",
	          "lifestyle",
	          "prepper",
	          "wildcard"
	        ]
	      },
	      "question": {
	        "type": "string"
	      }
	    },
	    "required": [
	      "category",
	      "question"
	    ]
	  }
	}"""
	MODEL_ID = "gemini-2.0-flash-lite"

	def __init__(self):
		pass

	def main(self):
		GOOGLE_API_KEY = ""
		with open("API.KEY", "r") as fd:
			GOOGLE_API_KEY = fd.readline()

		client = genai.Client(api_key=GOOGLE_API_KEY)

		print(textwrap.fill(self.__class__.INSTRUCT, width=80))
		loadJSON = json.loads(self.__class__.SCHEMA)
		print(json.dumps(loadJSON, indent=4))

		config = types.GenerateContentConfig(
			response_mime_type='application/json',
			system_instruction=self.__class__.INSTRUCT,
			response_schema=json.loads(self.__class__.SCHEMA),
		)

		print(config)

		responses = []
		for i in range(len(self.__class__.INPUT)):
			thisResponse = client.models.generate_content(
				model=self.__class__.MODEL_ID,
				contents=self.__class__.INPUT[i],
				config=config
			)
			responses.append(thisResponse)
		import datetime
		nowEpoch = datetime.datetime.now().strftime("%s")

		print(responses)

		with open(f'geminiResponses.{nowEpoch}.txt',"w+") as fd:
			for response in responses:
				print(response, "\n\n", response, json.dumps(response.parsed,
				      indent=4))
				fd.write(json.dumps(response.parsed,indent=4))

if __name__ == '__main__':
	Interact().main()
