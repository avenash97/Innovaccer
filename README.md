# Innovacer Data Analytics Assignment #
Variation in names leads to difficulty in identifying a unique person and hence deduplication of records is an unsolved challenge. 
The problem becomes more complicated in cases where data is coming from multiple sources.Hence, task is to train a model to identify unique patients in the sample dataset.
* Language used -  Python
* Important Libraries Used - unidecode, pyjarowinkler, dedupe, heapq
### Approach towards Problem Statement ###
* First step started with data preprocessing by cleaning data with the help of Unidecode and Regex. 
* Second step i.e. Training is done with the help of dedupe and to define the fields dedupe will pay attention.
* Active Learning is initiated by dedupe
* Using the labeled examples, train the deduper and learn blocking predicates
* Save the weights and predicates to disk. If the settings file exists, skip  the training and learning next time.
* Find the threshold that will maximize a weighted average.
* Clustering is performed with Match function that will return sets of record IDs that dedupe believes are all referring to the same entity.
* Write the data back out to a CSV with cluster ID and later update the file with unique entities with the help of threshlod score.

###  Code Running Sequence###
1. Update the dataset name in deduplicatio.py
2. Add the fields which needs to be governed while training with dedupe.
3. Run deduplication.py using python3
