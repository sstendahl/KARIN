import sys
import csv
from samples import Sample

def loadSampleList(self):
    samplelist = []
    with open('samplelist.csv', 'r') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
            else:
                newSample = Sample(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                   row[10], row[11], row[12], row[13], row[14], row[15],
                                   row[16])  # SampleID, Date, BG pressure
                samplelist.append(newSample)
    return samplelist

