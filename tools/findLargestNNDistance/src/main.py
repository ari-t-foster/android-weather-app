import math
import struct

import numpy as np
import scipy.spatial
import typing
import os
import json
import itertools

from scipy.spatial import cKDTree


class Ingest():
    def __init__(self,rootStaging: bool = False, fileStaging: bool = False):
        ROOT_PATH = {"DEFAULT": "../../", "STAGING": "../cs427-team10-project/", }
        FILE_PATH = {"DEFAULT": "app/src/main/resources/parsedPlaces.json",
            "STAGING": "tools/ripPlaces/parsedPlaces.json", }
        self.path = os.path.join(os.getcwd(),ROOT_PATH["STAGING"] if rootStaging else ROOT_PATH["DEFAULT"],FILE_PATH["STAGING"] if fileStaging else FILE_PATH["DEFAULT"])

    def doIngest(self):
        with open(self.path, 'r') as file:
            self.places = json.load(file)
        return self.places

    def print(self):
        for i in range(100):
            print(self.places[i])


class Report():
    def __init__(self,placesList):
        self.OUTFILE = "k10nn_sint32.bin"
        self.OUTPATH = os.path.join(os.getcwd(), self.OUTFILE)
        self.placesList = placesList
        self.row2placeName = dict()
        self.centroids = []
        self.cull()

    def cull(self):
        for i,row in enumerate(self.placesList):
            rowDict = dict(row)
            placeName = list(rowDict.keys())[0]
            self.row2placeName[i] = placeName
            self.centroids.append(rowDict[placeName]['centroid'])
        self.npar = np.array(self.centroids)
        self.makeKD()

    def makeKD(self):
        self.kdTree = cKDTree(self.npar)

    def kNearestForI(self,k=10):
        dist,idxs = self.kdTree.query(self.npar,k)
        with open(self.OUTPATH, "w+b") as fd:
            for i,n in enumerate(idxs):
                fd.write(struct.pack(">10i",*n.tolist()))

    def nn(self):
        dist,idxs = self.kdTree.query(self.npar,k=2)
        nnDist = dist[:,1]
        maxI = np.argmax(nnDist)
        maxD = nnDist[maxI]
        nnI = idxs[maxI,1]

        print("The pair of points with the maximum nearest neighbor distance:")
        print("Point 1 (index {}) [place name: {}]: {} (rads) {} (degs)".format(maxI, self.row2placeName[maxI], self.npar[maxI], [math.degrees(coord) for coord in self.npar[maxI]]))
        print("Point 2 (index {}) [place name: {}]: {} (rads) {} (degs)".format(nnI, self.row2placeName[nnI], self.npar[nnI], [math.degrees(coord) for coord in self.npar[nnI]]))
        print("Maximum nearest neighbor distance: {} (rads) {} (degs)".format(maxD, math.degrees(maxD)))


if __name__ == '__main__':
    instance = Report(Ingest().doIngest())
    instance.nn()
