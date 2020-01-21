import json

from ASeT import ASeT


#---- you neet to modify the following three arguments

pathModel = "/path/to/folder/model/NameModel" # (e.g. name model: generated_model_google )
pathListSemanticTags = "/path/to/folder/concepts_list/consepticon_1.0_multiLevel.txt"

pathOutput = "/path/to/folder/to/print/results/NameOutput" # no extension

#---- 

#---- Egyptian words to tag

wordsToTag = [[0, "a tree, oak", ["ʔln"]], [3, "head", ["tp"]], [4, "mountain peak, mountain top", ["rʔʃ"]],[5, "rush, hurry", ["ħfʣ"]], [6, "donkey", ["ʕʔ"]]] #


fileRead = open(pathListSemanticTags, "r")
listSemanticTags_json = fileRead.read()
listSemanticTags = json.loads(listSemanticTags_json)


#Arguments:

verbose = True
numberMatchesOutput = None
splitMenings = True
dividers = [","]

numberLevels = 2

semanticThreshold_lvl1=0.1
semanticThreshold_lvl2=0.45
thresholdClusters_lvl3 = None

thresholdClusters_lvl1 = 2
thresholdClusters_lvl2 = 2
semanticThreshold_lvl3 = None

resultsSimplified, resultsJson = ASeT( \
    wordsToTag,  \
    listSemanticTags, \
    pathModel, \
    pathOutput, \
    numberLevels, \
    numberMatchesOutput, \
    verbose, \
    splitMenings, \
    dividers, \
    semanticThreshold_lvl1, \
    semanticThreshold_lvl2, \
    semanticThreshold_lvl3, \
    thresholdClusters_lvl1, \
    thresholdClusters_lvl2, \
    thresholdClusters_lvl3)

print(resultsSimplified)
print(resultsJson)

