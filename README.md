# Android Weather App

## Description
This public repository contains selected Python tooling for geographic data preparation, spatial analysis, and Gemini integration experiments. The related Android application itself was developed collaboratively and is not included in this archive. The completed application and its updated Gemini integration are demonstrated through recorded workflows.

## Project Case Study and Demo Videos
[Project Case Study (including demo videos of the CityWeather App)](https://scienceopera.net/projects/android-weather-app)

## Android CityWeather App Attribution

### UIUC CS427 Team 10 Project, the Android CityWeather App
- **Group Members (Team 10):** Rohith Sanjay, Ari Foster, Caleb Satvedi, Arnav Jaiswal, John Randolph, Ryan Thammakhoune, Victoria Tiki, Aayush Bandopadhyay
- This repository contains an archive of tooling used in the development, debugging, and production of the Team 10 Project, the CityWeather App, not a buildable Android application.

## Licensing / Upstream data attribution
- All .py scripts in this repo were sole authored by me, Ari Foster, and are source available under BSD-3-Clause. See the `LICENSES/BSD-android-weather-app.txt` file.
- The derivative data in the `tools/ripPlaces/output_data/` directory was sourced from data released by the `weather-util` project. See the `LICENSES/ISC-weather-util.txt` file. Also, see the `THIRD_PARTY_NOTICES.md` file for more information.

## Tree Listing and Summary
```
├── geminiPythonAgent
│   ├── logs
│   │   ├── geminiResponses_1793147473
│   │   │   ├── gemini_output.1793147460.log
│   │   │   ├── geminiResponses.1793147473.jsonl
│   │   │   └── geminiResponses_VALIDATED.1793147473.jsonl
│   │   └── geminiResponses_1793152027
│   │       ├── gemini_output_simpler.1793152016.log
│   │       └── geminiResponses.1793152027.jsonl
│   └── src
│       ├── gemini.20261027.py
│       └── gemini.20261027.simplerschema.py
├── LICENSE
├── LICENSES
│   ├── BSD-android-weather-app.txt
│   └── ISC-weather-util.txt
├── README.md
├── THIRD_PARTY_NOTICES.md
└── tools
    ├── findLargestNNDistance
    │   └── src
    │       └── main.py
    ├── geminiInteraction
    │   ├── logs
    │   │   └── geminiResponses.1744337149.txt
    │   └── src
    │       └── main.py
    └── ripPlaces
        ├── output_data
        │   ├── parsedPlaces.json.gz
        │   └── parsedPlacesNames.json
        └── src
            └── ripPlaces.py
```
- `geminiPythonAgent/src/`
Contains the latest code/experiment for developing and implementing the modernization effort, enabling interaction code and JSON schema to be retrofitted with the existing codebase to facilitate the working demos of the app with the latest Gemini 3.8 Flash model. Note that it requires a Google API key to function (not provided).

- `geminiPythonAgent/logs/`
Contains log output from tool runs demonstrating the end-to-end data flows and behavior of API calls with the Gemini Interaction framework.

- `tools/`
Contains the original tooling which contributed to the initial release of the Android CityWeather App.

- `tools/findLargestNNDistance/`
Computes the maximum nearest-neighbor distance among geographic points using a K-d tree and great-circle distance calculations. Used to calibrate the application's city/place search parameters.

- `tools/geminiInteraction/`
Code/experiment for developing a JSON schema-constrained response framework for the app. Used the Gemini 2.0 Flash model.

- `tools/ripPlaces/`
Tooling to extract place names and corresponding spherical coordinates for mappoints from USA Public Domain data via data files made available by the Debian weather-util package.

- `tools/ripPlaces/output_data/`
Place and placename data JSON files exported from the tool.
