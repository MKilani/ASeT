# ASeT : Automatic Semantic Tagger 

Version: 0.0.1

Status: Beta

Release date: 08.01.2020

#### Authors

* **Marwan Kilani** - Swiss National Science Foundation (Mobility Grant) - Freie Universität Berlin (2019-2020)

#### How to cite

Kilani Marwan, 2020, ASeT : Automatic Semantic Tagger, https://github.com/MKilani/ASeT

## Introduction

Note: for a detailed explaination of the functioning of ASeT, see Kilani forthcoming. What follows here is just a short summary of the functioning of the algorithm.

ASeT is a python library meant to automatically assign tags from a list of semantic fields and/or concepts to items in a list of words.

The algorithm can be used apply a same single tagging system to word lists in different languages, as long as a translation in a same single "bridge" language (e.g. English) is provided for each word in each list. The tagging will then be performed on the translation. Note that the language of the translation and the language of the tags must be the same.

In order to achieve this goal, ASeT performs recursively the following steps:

* First, it calculates the semantic distance between each entry in the lexical list and each item in the list of semantic tags. The semantic distance is automatically calculated on the basis of a standard neural-network-trained word-to-vector (word2vec) semantic model. This approach is implemented through the [gensim](https://radimrehurek.com/gensim/) Python library. By default, the algorithm uses the xxx model, that is a semantic model trained on xxx.

* Once the semantic distances for each word are calculated, the algorithm proceeds to select, for each word, the semantic tags that semantically more similar to the word itself. Since the semantic distance is not not absolute but relative and it is affected by multiple unpredictable factors, it is not possible to simply use a threshold to define which tags are "similar enough" to be retained. ASeT bypasses this issue through an innovative approach that first clusters tags into discrete groups on the basis of their semantic distance from the target words and of the distance among each other, and then selects the tags belonging to the N clusters that appear to be the closest one (in relative terms, not in absolute terms). This approach relies on the observation that if one plots words (and semantic concepts) on an imaginary line according to their semantic distance from a given target term, they will not be distributed at regular, discrete intervals, but rather they will be clustered into groups according to both their relative distance from the targed term and the semantic distance between each other. A practical example: let us take the target term "apple", and the semantic tags "fruit", "berry", "reed", "grass", "twigs", "hand", "head", "lake", "river", "sea", "ocean". If we calculate the semantic distance of each of these concepts from the target term, and then we compare such distances among each other, it will appear that these concepts are not distributed at regular intervals, but rather they form clearly distinct clusters of different size, such as ["fruit", "berry"]; ["reed", "grass", "twigs"]; ["hand", "head"]; ["lake", "river", "sea", "ocean"] on the basis of their reciprocal similarity (or lack thereof). Such cluster can thus be used as a selecting criterion to identify the words/concepts that are semantically more similar to the target term. Selecting the concepts belonging to the first N clusters is in fact preferable to selecting the terms above an arpitrary threshold for two main theoretical reasons: on the one hand, we can safely assume that the words/concepts belonging to the first N clusters, are **significantly** and **distinctively** more similar to the target term than any of the terms belonging to the following clusters. Otherwise, they would not form any meaningful cluster in the first place. On the other hand, the words/concepts of the first (or N-th) cluster will always be distinctively more similar, in relative terms, than the words of the second (or N-th + 1) cluster and following clusters (or N-th + x), and this **indipendently** and **irrespective** of their **absolute** semantic distance from the target term. This is an important consideration, because it implies that by selecting the words/concepts belonging to the first (or N-th) cluster for every target term, we will always be selecting the relatively most similar (or N-th most similar) words/concepts, no matter the actual semantic distance of each word/concept from its respective target term. This is something that could not be achieved by using an arbitrary, fixed threshold.  
In ASeT, clusters are calculated authomatically using a simple 1D clustering function.  
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

And let assume we have the target word "waterfall", the algorithm will tag it proceding recursively through the three levels, 
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

The python package can be installed through pip:

```shell
python3 pip ASeT
```

ASeT is called through the method semanticTagger_multiLevel() . Here a minimal working example:

```python
xxx
```

## Input

The algorithm requires the following three items:

#### Semantic Model

A ["KeyedVectors"](https://radimrehurek.com/gensim/models/keyedvectors.html) model - the word2vec pre-trained model GoogleNews-vectors-negative300 can be used - it can be downlaod from this github repository: https://github.com/mmihaltz/word2vec-GoogleNews-vectors

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

The ASeT project provides a concept lists which has only two semantic levels, and which is based on the Semantic fields (= Level 1) and concept names (= Level 2) provided by the (Concepticon)[https://concepticon.clld.org/parameters] project. The phrasing of some entries has been slightly modified to improve readability by the algorithm (e.g., the semantic field "emotions and values" has been modified into "emodion values" removing the connecting word "and"). It can be downlaoded from the github repository: [Concept List](/conceptList/ConcepticonList)

#### Lexical list

The lexical list provides the targed words that need to be tagged.

The format is, once again, a list of lists, in which each item has the following form:

```
[ID_Word(int), translation(string), [form_1(string), form_2(string), etc]]
```

the translation entry must be a single string. If more translations are possible, they must be separated by a comma ','. Other separators can be declared explicitely (see below). Connecting words ("and", "of", "to", etc.), articles ("the", "a", "an") and other semantically empty terms should be avoided to avoid introducing "noise" that may reduce the performances of the algorithm.

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

* **LexicalList : [ [] ]** - List of words to be tagged (see above).
* **SemanticTags : [ [] ]** - List of semantic tags
* **pathModel : string** - path to the semantic model. The path must include the path name of the model itself, in the format "folder1/folder2/NameModel.
* **pathSemanticOutput : string** - path to the location where to save the output of ASeT. The path must include the path name of the model itself, in the format "folder1/folder2/NameOfOutput.

The follwoing arguments are optional:

* **numberMatchesOutput : int** - gensim allows to limits the number of best outputs when calculating semantic distances using a WmdSimilarity function ( which is the one used by ASeT - see [gensim.similarities.WmdSimilarity](https://tedboy.github.io/nlps/generated/generated/gensim.similarities.WmdSimilarity.html) ) . With None, no limit is appliaed. Default: None
* **semanticThreshold : double** - in case one wants to add a semantic threshold to limit the numebr of matches in addition to the clustering method, it can be set here. Default: 0.00 (= no threshold)
* **verbose : boolean** - Print logs while executing. Default: False
* **splitMenings : boolean** - Option to split meanings (like in the case of entry 2 'obey, abide, carry out' in the example above). Default: True
* **dividers : [ ]** - Dividers to be used to split meanings, if the previous option is set to True. Default: [","]
* **thresholdClusters_lvl1** - Number of most similar clusters to be retained from Level 1 - Default: 2
* **thresholdClusters_lvl2** - . Default: 2
* **thresholdClusters_lvl3** - . Default: 2

Concernign the last three arguments, note that the first cluster corresponds to semantic tags that have a 1.0 semantic distance from the target word, i.e. semantic tags that are perceived by the algorithm as identical with the target word itself (e.g. the semantic tag "water" in comparison with the target word "water"). If no semantic tag has a 1.0 semantic distance with the target word, i.e. if no sematic tag has a fully matches the target word, then the first cluster will be empty. For this reason, it is reasonable to always select at least the first 2 clusters.

## Output

Coming soon.

## Example

Coming soon.

## Running the tests

Coming soon.





