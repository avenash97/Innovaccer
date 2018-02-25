from future.builtins import next

import os
import csv
import re
import logging
import optparse
import sys
import csv
import dedupe
import operator
from heapq import heapify,heappop,nsmallest


from unidecode import  unidecode
from pyjarowinkler import distance

input_file = 'dataset.csv'
output_file = 'output1.csv'
settings_file = 'learned_settings'
training_file = 'example_training.json'


# Read the data from CSV file:

def readData(filename):

    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
            row_id = int(row['Id'])
            data_d[row_id] = dict(clean_row)

    return data_d

# Data Preprocessing

def preProcess(column):

    try:
        column = column.decode('utf-8')
    except AttributeError:
        pass
    column = unidecode(column)
    column = re.sub(' +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()

    if not column:
        column = None
    return column


print('importing data ...')
data_d = readData(input_file)

if os.path.exists(settings_file):
    print('reading from', settings_file)
    with open(settings_file, 'rb') as f:
        deduper = dedupe.StaticDedupe(f)
else:
    fields = [
        {'field' : 'ln', 'type': 'String'},							# Field to be taken care while training
		{'field' : 'dob', 'type': 'String'},
		{'field' : 'gn', 'type': 'Exact', 'has missing' : True},
		{'field' : 'fn', 'type': 'String', 'has missing' : True},
        ]
    deduper = dedupe.Dedupe(fields)
    deduper.sample(data_d, 15000)

    if os.path.exists(training_file):
        print('reading labeled examples from ', training_file)
        with open(training_file, 'rb') as f:
            deduper.readTraining(f)

    print('starting active labeling...')

    dedupe.consoleLabel(deduper)

    deduper.train()

    with open(training_file, 'w') as tf:
        deduper.writeTraining(tf)

    with open(settings_file, 'wb') as sf:
        deduper.writeSettings(sf)

threshold = deduper.threshold(data_d, recall_weight=1)

print('clustering...')
clustered_dupes = deduper.match(data_d, threshold)

print('# duplicate sets', len(clustered_dupes))


cluster_membership = {}
cluster_id = 0
for (cluster_id, cluster) in enumerate(clustered_dupes):
    id_set, scores = cluster
    cluster_d = [data_d[c] for c in id_set]
    canonical_rep = dedupe.canonicalize(cluster_d)
    for record_id, score in zip(id_set, scores):
        cluster_membership[record_id] = {
            "cluster id" : cluster_id,
            "canonical representation" : canonical_rep,
            "confidence": score
        }

singleton_id = cluster_id + 1

with open(output_file, 'w') as f_output, open(input_file) as f_input:
    writer = csv.writer(f_output)
    reader = csv.reader(f_input)

    #heading_row = next(reader)
    #heading_row.insert(0, 'confidence_score')
    #heading_row.insert(0, 'Cluster ID')
    canonical_keys = canonical_rep.keys()
    #for key in canonical_keys:
    #    heading_row.append('canonical_' + key)

    #writer.writerow(heading_row)

    for row in reader:
    	if row[0]=='Id':
    		continue
    	row_id = int(row[0])
    	if row_id in cluster_membership:
    		cluster_id = cluster_membership[row_id]["cluster id"]
    		canonical_rep = cluster_membership[row_id]["canonical representation"]
    		row.insert(0, cluster_membership[row_id]['confidence'])
    		row.insert(0, cluster_id)
    		for key in canonical_keys:
    			row.append(canonical_rep[key].encode('utf8'))
    	else:
    		row.insert(0, None)
    		row.insert(0, singleton_id)
    		singleton_id += 1
    	for key in canonical_keys:
    		row.append(None)
    	writer.writerow(row)
    ele = set()
    reader = []x	
    for i in filter(None,open("csv_example_output1.csv").read().split("\n")):
    	if i.split(",")[0] not in ele:
    		reader.append(i)
    		ele.add(i.split(",")[0])
    #print("\n".join(reader))		
    #reader = set(filter(None,open("csv_example_output1.csv").read().split("\n")))
    #print(reader)
    sortedlist = [ i.split(",") for i in reader]
    print(sortedlist)
    def heapsort(list_heap):
    	return nsmallest(len(list_heap),list_heap,key=lambda x: int(x[0]))
    with open('updated.csv', 'w') as myfile:
    	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    	temp = heapsort(sortedlist)
    	print(temp)
    	wr.writerows(temp)
