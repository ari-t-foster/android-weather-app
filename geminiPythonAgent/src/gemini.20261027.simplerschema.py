from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
import textwrap
import time
import json

minifyPrintJSON = lambda x: json.dumps(json.loads(x), indent=None, separators=(',',':'))
prettyPrintJSON = lambda x: json.dumps(json.loads(x), indent=2)
wrap80 = lambda x: textwrap.fill(x, width=80)

MODEL="gemini-3.8-flash"

INSTRUCT = """
Based on the input given, generate exactly 4 sets of questions and answers which a user might interested in asking and finding out the answer to, and which are relevant to the context of the current weather report you are receiving. The output question must be a single short sentence, ending in a question mark. Sample categories of questions include (but are not limited to): appropriate clothing or gear to wear or carry, preparing for exposure to elements, outdoor (or indoor) activities, weather safety information, record highs and lows, seasonability of current conditions for the current and nearby locations, historically significant weather events, astrological events and sky visibility.
Base answers only on supplied weather observations. Do not invent forecasts, historical records, or future conditions. If sufficient data is unavailable, select a different question.
"""

print(wrap80(INSTRUCT))

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

class WeatherQAPair(BaseModel):
    question: str = Field(description="Weather question")
    answer: str = Field(description="Weather answer")

class WeatherQAQuadrant(BaseModel):
    quadrant: List[WeatherQAPair] = Field(min_length=4, max_length=4)

GENERATED_SCHEMA = WeatherQAQuadrant.model_json_schema()

print(f"\n\nINSTRUCT VERBIAGE:\n\n{wrap80(INSTRUCT)}")
print(f"\n\nGENERATED SCHEMA (RAW):\n\n{GENERATED_SCHEMA}")
print(f"\n\nGENERATED SCHEMA (PPRINTED):\n\n{prettyPrintJSON(json.dumps(GENERATED_SCHEMA))}")

SCHEMA="""
{
  "type": "object",
  "required": [
    "quadrant"
  ],
  "properties": {
    "quadrant" : {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "question": {
            "type": "string"
          },
          "answer": {
            "type": "string"
          }
        },
        "required": [
          "question",
          "answer"
        ]
      },
      "minItems": 4,
      "maxItems": 4
    }
  }
}
"""

print(f"\n\nOWN SCHEMA (RAW):\n\n{SCHEMA}")
print(f"\n\nOWN SCHEMA (PPRINTED):\n\n{prettyPrintJSON(SCHEMA)}")

def read_key():
    SECRET_GOOGOO_MAN = ""
    with open("KEYKEY.KEY", "r") as fd:
        SECRET_GOOGOO_MAN = fd.readline()
    
    if SECRET_GOOGOO_MAN == "":
        raise RuntimeError("No tickey, no laundry.")

    return SECRET_GOOGOO_MAN

client = genai.Client(api_key=read_key())

usages = []
responses = []
for i,v in enumerate(INPUT):
    d = json.loads(v)
    dx = json.dumps(d, separators=(",",":"))

    interaction = client.interactions.create(
        model=MODEL,
        system_instruction=INSTRUCT,
        input=dx,
        generation_config={
            "thinking_level": "low",
        },
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": json.loads(SCHEMA)
        },
    )

    usages.append(interaction.usage)
    responses.append(interaction.output_text)

nowEpoch = (int)(time.time())

print(f"\n\nRAW RESPONSE OUTPUT TEXT:\n\n{responses}")
print(f"\n\nRAW RESPONSE USAGE::\n\n:{usages}")

for i,resp in enumerate(responses):
    print(f"\n\nRESPONSE {i}/{len(responses)}:\n\n{prettyPrintJSON(resp)}")

with open(f'geminiResponses_VALIDATED.{nowEpoch}.jsonl',"w",encoding="utf-8") as fd_validated:
    with open(f'geminiResponses.{nowEpoch}.jsonl',"w",encoding="utf-8") as fd:
        for response in responses:
            fd.write(
                json.dumps(
                    json.loads(response),
                    separators=(",",":"),
                    ensure_ascii=False
                ) + "\n"
            )
