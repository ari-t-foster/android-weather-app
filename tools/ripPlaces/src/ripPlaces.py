#!/usr/bin/env python3

import gzip
import json
import os
from typing import List, Dict

def doPlacesParse(placesFile : str) -> List[Dict]:
    recordDict = dict()
    outputDict = dict()

    chompRest = True
    with gzip.open(placesFile, 'rt') as inStream:
        for line in inStream:
            stripped = line.strip()
            # blank line
            if not stripped: continue
            if stripped[0] == '#': continue
            elif stripped[0] == '[':
                recordDict.clear()
                chompRest = False
                continue
            if stripped.find('=') != -1:
                if chompRest: continue
                key, val = stripped.split(' = ')
                if key == 'centroid':
                    # too much data
                    #continue

                    centroidList = []
                    centroidVal = val.split(',')
                    for tupElem in centroidVal:
                        centroidList.append(float(tupElem.strip().lstrip('(').rstrip(')')))
                    recordDict[key] = centroidList
                elif key == 'description':
                    descriptionStr = val.strip()
                    chompRest = descriptionStr in outputDict
                    if chompRest: continue
                    recordDict[key] = descriptionStr
                elif key == 'station':
                    stationStr = val.split(',')[0]
                    stationStr = stationStr.strip().lstrip('(').lstrip("'").rstrip("'")
                    recordDict[key] = stationStr
                elif key == 'zone':
                    zoneStr = val.split(',')[0]
                    zoneStr = zoneStr.strip().lstrip('(').lstrip("'").rstrip("'")
                    recordDict[key] = zoneStr
                    if not chompRest and 'description' in recordDict:
                        outputDict[recordDict['description']] = {
                            'centroid' : recordDict['centroid'],
                            'station' : recordDict['station'],
                            'zone' : recordDict['zone']
                        }
                        recordDict.clear()
                        chompRest = False

    return [ {k : outputDict[k]} for k in sorted(outputDict.keys()) ]

def main():
    zonesFile = '/usr/share/weather-util/zones.gz'
    placesFile = '/usr/share/weather-util/places.gz'

    outFile = os.path.join(os.getcwd(), 'parsedPlaces.json')
    outFileGz = os.path.join(os.getcwd(), 'parsedPlaces.json.gz')
    outFileNames = os.path.join(os.getcwd(), 'parsedPlacesNames.json')

    parsedPlaces = doPlacesParse(placesFile)
    jsonArgs = {'indent':0, 'separators':(',',':')}
    print("Finished parsing places...")

    with open( outFile, 'w' ) as f:
        json.dump(parsedPlaces, f, **jsonArgs)

    print("Wrote JSON output to:", outFile)

    with gzip.open( outFileGz, 'wt' ) as f:
        json.dump(parsedPlaces, f, **jsonArgs)

    print("Wrote compressed JSON output to:", outFileGz)

    namesOnly = [list(k.keys())[0] for k in parsedPlaces]

    with open( outFileNames, 'wt' ) as f:
        json.dump(namesOnly, f, **jsonArgs)

    print("Wrote place names only to:", outFileNames)

# entry point for cmdline
if __name__ == '__main__': main()

