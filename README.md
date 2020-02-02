# ASeT : Automatic Semantic Tagger 

Version: 0.0.4b

Status: Beta - work in progress

Release date: 08.01.2020

Last Update: 21.01.2020

#### Authors

* **Marwan Kilani** - Swiss National Science Foundation (Mobility Grant) - Freie Universität Berlin (2019-2020)

#### How to cite

Kilani Marwan, 2020, ASeT 0.0.4 beta: Automatic Semantic Tagger, https://github.com/MKilani/ASeT

## Introduction

Note: for a detailed explanation of the functioning of ASeT, see Kilani forthcoming. What follows here is just a short summary of the functioning of the algorithm.

ASeT is a python library meant to automatically assign tags from a list of semantic fields and/or concepts to items in a list of words.

The algorithm can be used apply a same single tagging system to word lists in different languages, as long as a translation in a same single "bridge" language (e.g. English) is provided for each word in each list. The tagging will then be performed on the translation. Note that the language of the translation and the language of the tags must be the same.

In order to achieve this goal, ASeT performs recursively the following steps:

* First, it calculates the semantic distance between each entry in the lexical list and each item in the list of semantic tags. The semantic distance is automatically calculated on the basis of a standard neural-network-trained word-to-vector (word2vec) semantic model. This approach is implemented through the [gensim](https://radimrehurek.com/gensim/) Python library.

* Once the semantic distances for each word are calculated, the algorithm proceeds to select, for each word, the semantic tags that semantically more similar to the word itself. Since the semantic distance is not absolute but relative and it is affected by multiple unpredictable factors, it is not possible to simply use a threshold to define which tags are "similar enough" to be retained.  
ASeT bypasses this issue through an innovative approach that first clusters tags into discrete groups on the basis of their semantic distance from the target words and of the distance among each other, and then selects the tags belonging to the N clusters that appear to be the closest one (in relative terms, not in absolute terms). This approach relies on the observation that if one plots words (and semantic concepts) on an imaginary line according to their semantic distance from a given target term, they will not be distributed at regular, discrete intervals, but rather they will be clustered into groups according to both their relative distance from the target term and the semantic distance between each other. A practical example: let us take the target term "apple", and the semantic tags "fruit", "berry", "reed", "grass", "twigs", "hand", "head", "lake", "river", "sea", "ocean".  
If we calculate the semantic distance of each of these concepts from the target term, and then we compare such distances among each other, it will appear that these concepts are not distributed at regular intervals, but rather they form clearly distinct clusters of different size, such as ["fruit", "berry"]; ["reed", "grass", "twigs"]; ["hand", "head"]; ["lake", "river", "sea", "ocean"] on the basis of their reciprocal similarity (or lack thereof). Such cluster can thus be used as a selecting criterion to identify the words/concepts that are semantically more similar to the target term.  
Selecting the concepts belonging to the first N clusters is in fact preferable to selecting the terms above an arbitrary threshold for two main theoretical reasons: on the one hand, we can safely assume that the words/concepts belonging to the first N clusters, are **significantly** and **distinctively** more similar to the target term than any of the terms belonging to the following clusters. Otherwise, they would not form any meaningful cluster in the first place.  
On the other hand, the words/concepts of the first (or N-th) cluster will always be distinctively more similar, in relative terms, than the words of the second (or N-th + 1) cluster and following clusters (or N-th + x), and this **independently** and **irrespective** of their **absolute** semantic distance from the target term. This is an important consideration, because it implies that by selecting the words/concepts belonging to the first (or N-th) cluster for every target term, we will always be selecting the relatively most similar (or N-th most similar) words/concepts, no matter the actual semantic distance of each word/concept from its respective target term. This is something that could not be achieved by using an arbitrary, fixed threshold.  
In ASeT, clusters are calculated automatically using a simple 1D clustering function.  
Note that clusters can be formed also by one single item.

These two steps are repeated recursively for up to 3 distinct levels of semantic classification (the possibility of scaling up to a N number of levels will likely be implemented in the coming version of ASeT).

More in particular, let assume a series of semantic tags organized in the following three-level hierarchy:

| Level 1 | Level 2 | Level 3 |
|---|---|---|
| water | basin | sea |
|   |   | ocean |
|   |   | lake |
|   |   | pond |
|   | stream | river |
|   |   | wadi |
|   |   | creek |
|---|---|---|
| container | basketry | basket |
|   |   | creel |
|   |   | pannier |
|   | vessel | bottle |
|   |   | jar |
|   |   | jug |
|   |   | amphore |
|   | box | coffer |
|   |   | crate |
|   |   | chest |

And let assume we have the target word "waterfall", the algorithm will tag it proceeding recursively through the three levels, 
* first looking for the most similar cluster in the first level, in this case [water]  (assuming the algorithm is looking only for one cluster)
* then for the most similar cluster within the words/concepts pertaining to [water], in this case [stream]
* finally, for the most similar cluster within words/concepts pertaining to [stream], in this case [river, creek]

This will result in the following tagging pattern:

```
waterfall:
	Level 1: water
	Level 2: stream
	Level 3: river, creek
```

It has to be stressed that obviously, the best results are obtained when this method is used as a semi-automatic approach, where the results of the automatic tagging process are manually verified to eliminate possible spurious tags.

## Getting Started

### Prerequisites

You need Python 3.

### Installing

The python package can be installed through pip, from the testing python repository:

```shell
python3 -m pip install --index-url https://test.pypi.org/simple/ ASeT
```

ASeT is called through the method ASeT() . See **Running the test** below.

## Input

The algorithm requires the following three items:

#### Semantic Model

A ["KeyedVectors"](https://radimrehurek.com/gensim/models/keyedvectors.html) model - the word2vec pre-trained model GoogleNews-vectors-negative300 can be used - it can be download from this github repository: https://github.com/mmihaltz/word2vec-GoogleNews-vectors

#### List of semantic concepts

The list must be formatted as a list of lists, in which each entry has the following format:

```
[ID_Concept(int), concept(string), ID_superodinate_concept-Level_1(int), ID_superodinate_concept-Level_2(int)]
```

Concepts can be either single words (e.g. 'body'), or small groups of related words, in which case each word most be separated by a space (e.g. 'motion movement vehicle cart').

Concepts belonging to the first semantic level must have ID_superodinate_concept-Level_1 = -1 and ID_superodinate_concept-Level_2 = -1.

Concepts belonging to the second semantic level must have ID_superodinate_concept-Level_2 = -1.

The ID of the first item must be 0.

Using the example discussed above, this would be a valid list:

```
[
	[0, 'water', -1, -1],
	[1, 'container', -1, -1],
	[3, 'basin', 0, -1],
	[4, 'stream', 0, -1],
	[5, 'basketry', 1, -1],
	[6, 'vessel', 1, -1],
	[7, 'box', 1, -1],
	[8, 'sea', 0, 3],
	[9, 'ocean', 0, 3],
	[10, 'lake', 0, 3],
	[11, 'pond', 0, 3],
	[12, 'river', 0, 4],
	[13, 'wadi', 0, 4],
	[14, 'creek', 0, 4],
	[15, 'basket', 1, 5],
	[16, 'creel', 1, 5],
	[17, 'pannier, 1, 5],
	[19, 'bottle', 1, 6],
	[20, 'jar', 1, 6],
	[21, 'jug', 1, 6],
	[22, 'amphore', 1, 6],
	[23, 'coffer', 1, 7],
	[24, 'crate', 1, 7],
	[25, 'chest', 1, 7]
]
```

The ASeT project provides a concept lists which has only two semantic levels, and which is based on the Semantic fields (= Level 1) and concept names (= Level 2) provided by the (Concepticon)[https://concepticon.clld.org/parameters] project. The phrasing of some entries has been slightly modified to improve readability by the algorithm (e.g., the semantic field "emotions and values" has been modified into "emotion values" removing the connecting word "and"). It can be downloaded from the github repository: [Concept List](/conceptList/consepticon_1.0_multiLevel.json )

#### Lexical list

The lexical list provides the target words that need to be tagged.

The format is, once again, a list of lists, in which each item has the following form:

```
[ID_Word(int), translation(string), [form_1(string), form_2(string), etc]]
```

the translation entry must be a single string. If more translations are possible, they must be separated by a comma ','. Other separators can be declared explicitly (see below). Connecting words ("and", "of", "to", etc.), articles ("the", "a", "an") and other semantically empty terms should be avoided to avoid introducing "noise" that may reduce the performances of the algorithm.

The forms, instead, are input as individual entries in a list of strings.

The following is a valid example (using a small set of Italian words, with IPA transcriptions for the form entries):

```
[
	[0, 'mouse', ['tɔpo']],
	[1, 'garlic', ['aʎʎo']],
	[2, 'obey, abide, carry out', ['ubbidire', 'obbedire'],
	[3, 'bread', ['pane']]
]
```

## Arguments

The algorithm takes the following arguments:

* **LexicalList : [ [] ]** - First lexical list to compare -- Format: list of list: [each entry: [ ID (int), meanings (string, with separators), forms (array of strings, Unicode IPA) ]]
* **SemanticTags : [ [] ]** - List of semantic tags -- Format: list of list: [each entry: [ ID (int), meanings (string, no separators), ID top semantic level (int - if already top = -1), ID second from top semantic level (int - if already top or second from top = -1) ]]
* **pathModel : string** - Path to the semantic model. The path must include the path name of the model itself, in the format "folder1/folder2/NameModel
* **pathOutput : string** - Path to save the results (string - no extension; e.g. /my/folder/name_file_with_my_results)

The follwoing arguments are optional:

* **numberLevels : int** - Number of semantic levels to take into account (int) -- default = 2
* **semanticThreshold : double** - In case one wants to add a semantic threshold to limit the numebr of matches in addition to the clustering method, it can be set here -- Default: 0.00 (= no threshold)
* **verbose : Boolean** - Print logs while executing -- Default: True
* **splitMenings : Boolean** - Option to split meanings (like in the case of entry 2 'obey, abide, carry out' in the example above) -- Default: True
* **dividers : [ ]** - Dividers to be used to split meanings, if the previous option is set to True -- Default: [","]
* **thresholdClusters_lvl1 : int** - N-best clusters to take into account in the results for the semantic level 1 -- Default: 2
* **thresholdClusters_lvl2 : int** - N-best clusters to take into account in the results for the semantic level 1 -- Default: 2
* **thresholdClusters_lvl3 : int** - N-best clusters to take into account in the results for the semantic level 1 -- Default: 2


Concerning the last three arguments, note that the first cluster corresponds to semantic tags that have a 1.0 semantic distance from the target word, i.e. semantic tags that are perceived by the algorithm as identical with the target word itself (e.g. the semantic tag "water" in comparison with the target word "water"). If no semantic tag has a 1.0 semantic distance with the target word, i.e. if no sematic tag has a fully matches the target word, then the first cluster will be empty. For this reason, it is reasonable to always select at least the first 2 clusters.

## Output

The algorithm yields a double output, therefore two variable separated by a comma are needed to store the results:

```python
resultsSimplified, resultsJson = ASeT(wordsToTag, listSemanticTags, pathModel, pathOutput, numberLevels, numberMatchesOutput, verbose, splitMenings, dividers, semanticThreshold_lvl1, semanticThreshold_lvl2, semanticThreshold_lvl3, thresholdClusters_lvl1, thresholdClusters_lvl2, thresholdClusters_lvl3)
```

The first output is a list of dictionaries with a summary of the results with only the most relevant informations. Each entry represent a semantic tag, and it contains the following fields:

```python
"01_Entry_ID" : ID of the word being tagged.
"02_Entry_Form" : Form of the word being tagged.
"03_Entry_Meaning" : Meaning of the word being tagged.
"04_Match_Level" : Semantic level of the matching tag.
"05_Cluster_Match" : N-Cluster of the matching tag.
"06_ID_Match" : ID of the matching tag.
"07_Semantic_Tag" : Semantic tag of the matching tag.
```

The second output present the same results (plus a few additional secondary paramenters) in the form of a nested dictionary (in json format). Its structure is the following - note that the names of the entires in the dictionaries are meant to be compatible with the [ALeA](https://github.com/MKilani/ALeA) algorithm:


```python
   "000000": { # ID of the word being tagged
      "00_ID_token": int,
      "01_Meaning_token": "string",
      "02_Form_token": [
         "string"
      ],
      "03_Matches": {
         "Level_01": { # semantic level
            "000000": { # ID of the semantic tag
               "00_ID_Match": int,
               "02_Form_Match": -1,
               "03_Best_Match_Sem": [
                  "string",
                  "string"
               ],
               "05_ID_Cluster": int,
               "06_Sim_Score_Sem_Match": 0.52827501976487,
               "11_Semantic_Field": "string"
            }
         }
      }
   },
```


## Running the test

The file ASeT_tester.py provides an example of the use of the ASeT algorithm to tag a selection of Ancient Egyptian words.  
It can be downloaded from the github repository [ASeT_tester.py](/tester/ASeT_tester.py)

The file ASeT_tester.py can be run from command line with:

```shell
python3 ASeT_tester.py
```

Note that the location fo various files need to be modified within the ALeA_tester.py file before running the script. Just open it with any editor of text and follow the indications.

The results should look like this: [Results_ASeT](/tester/testerResults.txt)


The results show that the algorithm was able to identify several relevant semantic tags. The list, however, includes also a relatively small number of tags that are clearly spurious either because they are semantically too far to be relevant, or because they reflect secondary meanings of the English word that are not relevant for the semantics of the Egyptian form.  
This is not a problem: as said above, ASeT should be used within a semi-automated approach, where the results of the automatic tagging process are manually verified to select the best tags and to eliminate possible spurious tags.





