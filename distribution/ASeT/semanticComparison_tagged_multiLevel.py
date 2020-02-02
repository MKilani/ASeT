from gensim.test.utils import datapath
from gensim.models import KeyedVectors
from gensim.similarities import WmdSimilarity
from operator import itemgetter
import datetime

from .progbar import progbar
from .clusteringFunction import clusteringFunction

import json

import copy
#from timeit import default_timer as timer


def all_same(items):
    return all(x == items[0] for x in items)


def semanticComparison_tagged_multiLevel(LexicalList, SemanticTags, pathModel, semanticLevel, previousDataset_json = None, numberMatchesOutput=None, verbose=False, semanticThreshold=0.45, splitMenings = True, dividers = [","], thresholdClusters = None): #, PathTime, pathSemanticOutput,

    dicOne = copy.deepcopy(LexicalList)
    dicTwo = SemanticTags

    print("*- Semantic comparison -*")
    print("-> Start")


    print("-> Load Model")

    # load the google word2vec model
    temp_file = datapath(pathModel)
    model = KeyedVectors.load(temp_file)

    print("-> Model loaded")

    # print time model loaded
    #time = open(PathTime, "a")

    #time.write("Model loaded: " + str(datetime.datetime.now()) + "\n")
    #time.close()

    #==================

    # prepare new dictionary to store the data:
    dicOne_Matches = copy.deepcopy(dicOne)

    for i in range(0,len(dicOne_Matches)):
        dicOne_Matches[i].append([])



    # split the components of the dictionaries into arrays
    lexicalID_One = []
    lexicalDefinitionsBase_One = []
    lexicalDefinitions_One = []
    lexicalItems_One = []
    ID_entryLexicalItems_One = []
    ID_meaningItem_One = []

    lexicalID_Two = []
    lexicalDefinitionsBase_Two = []
    lexicalDefinitions_Two = []
    lexicalItems_Two = []
    ID_entryLexicalItems_Two = []
    ID_meaningItem_Two = []

    # note: the definition must be put into an array - hence the split - otherwise the semantic model doesn't work
    ID_entry_One = 0
    ID_meaning_One = 0


    for entry in dicOne_Matches:

        lexicalID_One.append(entry[0])
        #lexicalDefinitions_One.append(entry[1].split(" "))
        lexicalItems_One.append(entry[2])

        if splitMenings == False:
            lexicalDefinitions_One.append(entry[1].split(" "))
            ID_entryLexicalItems_One.append(ID_entry_One)
            ID_meaningItem_One.append(ID_meaning_One)
            ID_meaning_One = ID_meaning_One + 1
            # xxx index best match
        else:

            stringMeaning_One = entry[1]

            for divider in dividers:

                stringMeaning_One = stringMeaning_One.replace(divider, "£")

            stringMeaning_One = stringMeaning_One.replace("  ", " ")
            stringMeaning_One = stringMeaning_One.replace("  ", " ")
            stringMeaning_One = stringMeaning_One.replace("  ", " ")
            stringMeaning_One = stringMeaning_One.replace("£ ", "£")
            stringMeaning_One = stringMeaning_One.replace(" £", "£")
            stringMeaning_One_split = stringMeaning_One.split("£")

            for meaning in stringMeaning_One_split:
                lexicalDefinitionsBase_One.append(meaning)

                lexicalDefinitions_One.append(meaning.split(" "))
                ID_entryLexicalItems_One.append(ID_entry_One)
                ID_meaningItem_One.append(ID_meaning_One)
                ID_meaning_One = ID_meaning_One + 1

        ID_entry_One = ID_entry_One + 1





    ID_entry_Two = 0
    ID_meaning_Two = 0

    ID_level_0 = -1
    ID_level_1 = -1

    currentLevel = 0




    for entry in dicTwo:

        lexicalID_Two.append(entry[0])
        # lexicalDefinitions_Two.append(entry[1].split(" "))
        lexicalItems_Two.append(entry[2])

        if splitMenings == False:
            lexicalDefinitions_Two.append(entry[1].split(" "))
            ID_entryLexicalItems_Two.append(ID_entry_Two)
            ID_meaningItem_Two.append(ID_meaning_Two)
            ID_meaning_Two = ID_meaning_Two + 1
            # xxx index best match
        else:

            stringMeaning_Two = entry[1]

            for divider in dividers:
                stringMeaning_Two = stringMeaning_Two.replace(divider, "£")

            stringMeaning_Two = stringMeaning_Two.replace("  ", " ")
            stringMeaning_Two = stringMeaning_Two.replace("  ", " ")
            stringMeaning_Two = stringMeaning_Two.replace("  ", " ")
            stringMeaning_Two = stringMeaning_Two.replace("£ ", "£")
            stringMeaning_Two = stringMeaning_Two.replace(" £", "£")
            stringMeaning_Two_split = stringMeaning_Two.split("£")

            for meaning in stringMeaning_Two_split:
                lexicalDefinitionsBase_Two.append(meaning)

                lexicalDefinitions_Two.append(meaning.split(" "))
                ID_entryLexicalItems_Two.append(ID_entry_Two)
                ID_meaningItem_Two.append(ID_meaning_Two)

                ID_meaning_Two = ID_meaning_Two + 1

        ID_entry_Two = ID_entry_Two + 1


    if numberMatchesOutput == None:
        numberMatchesOutput = len(lexicalDefinitions_Two) * len(lexicalDefinitions_One)


    #compile the index
    print("-> Compile semantic index")
    index = WmdSimilarity(lexicalDefinitions_Two, model, numberMatchesOutput)
    print("-> Semantic index compiled")

    #use dicOne as a key to sort dictionary two


    listMatchesTemp = []
    indexKey = 0

    if semanticThreshold == None:
        semanticThreshold = 0


    #set up progress bar
    indexBar = -1
    print("Progress:")

    # se livello 2 o 3, devi compilare una lista dei campi 1 o 2 attestati nella forma
    DictFields = {}  # [ID item] : [level 2, level 1]
    for entry in dicTwo:
        DictFields[entry[0]] = [entry[2], entry[3]]

    dictValidFields = {}

    for key in lexicalDefinitions_One:

        indexBar = indexBar + 1
        progbar(indexBar, len(lexicalDefinitions_One) - 1, 20)

        key_A = ID_entryLexicalItems_One[indexKey]

        key_A_orig = key_A

        key_A = str(key_A)

        if len(key_A) == 1:
            key_A = "00000" + key_A
        if len(key_A) == 2:
            key_A = "0000" + key_A
        if len(key_A) == 3:
            key_A = "000" + key_A
        if len(key_A) == 4:
            key_A = "00" + key_A
        if len(key_A) == 5:
            key_A = "0" + key_A



        validFields = []
        if semanticLevel > 1:
            previousDataset = json.loads(previousDataset_json)

        if semanticLevel == 1:
            for key_Dict in DictFields:
                if DictFields[key_Dict][0] == -1:
                    validFields.append(key_Dict)

        if semanticLevel == 2:
            token = previousDataset[key_A]
            for match_key in token["03_Matches"]["Level_01"]:
                match = token["03_Matches"]["Level_01"][match_key]
                validFields.append(match["00_ID_Match"])

        if semanticLevel == 3:
            token = previousDataset[key_A]
            for match_key in token["03_Matches"]["Level_02"]:
                match = token["03_Matches"]["Level_02"][match_key]
                validFields.append(match["00_ID_Match"])

        if not indexKey in dictValidFields:
            dictValidFields[indexKey] = validFields.copy()

        indexKey = indexKey + 1

    indexKey = 0

    indexBar = -1
    print()
    print("Progress:")

    for key in lexicalDefinitions_One:
        indexBar = indexBar + 1
        query = [key]
        resultsQuery = index[query]
        resultsQueryWithIndexes = list(enumerate(resultsQuery))

        #rimuovere quelli che non sono rilevanti





        for i in range(0, len(resultsQueryWithIndexes)):
            index_itemQuerry = resultsQueryWithIndexes[i][1][0]
            if semanticLevel == 1:
                if not index_itemQuerry in dictValidFields[indexKey] and not resultsQueryWithIndexes[i][1][1] == 1:
                    resultsQueryWithIndexes[i] = None
            elif semanticLevel == 2:
                if not DictFields[index_itemQuerry][0] in dictValidFields[indexKey] and not resultsQueryWithIndexes[i][1][1] == 1:
                    resultsQueryWithIndexes[i] = None
            elif semanticLevel == 3:
                if not DictFields[index_itemQuerry][1] in dictValidFields[indexKey] and not resultsQueryWithIndexes[i][1][1] == 1:
                    resultsQueryWithIndexes[i] = None

        resultsQueryWithIndexes = list(filter(None, resultsQueryWithIndexes))



        #DictFields = {}  # [ID item] : [level 2, level 1]
        #validFields = []

        #resultsQuerySorted = sorted(resultsQueryWithIndexes, key=itemgetter(1))
        #print (resultsQueryWithIndexes[0][1][1])
        #resultsQuerySortedReversed = resultsQuerySorted[::-1]
        resultsQuerySortedReversed= []
        for item in resultsQueryWithIndexes:
            resultsQuerySortedReversed.append(item[1])


        if len(lexicalDefinitions_One) > 1:
            progbar(indexBar, len(lexicalDefinitions_One)-1, 20)
        else:
            progbar(indexBar, len(lexicalDefinitions_One), 20)
            #print("Entry DicOne: " + str(key))
            #print("Sorted results DicTwo: " + str(resultsQuerySortedReversed))

        newMatchBatch = []



        for item in resultsQuerySortedReversed:

            newMatch = []

            #if item[1] >= semanticThreshold:

            indexEntryMeaningA = ID_entryLexicalItems_One[indexKey]
            indexEntryMeaningB = ID_entryLexicalItems_Two[item[0]]

            indexMeaningA = ID_meaningItem_One[indexKey]
            indexMeaningB = ID_meaningItem_Two[item[0]]

            newMatch.append(indexEntryMeaningA)
            newMatch.append(indexMeaningA)
            newMatch.append(indexEntryMeaningB)
            newMatch.append(indexMeaningB)
            newMatch.append(item[1])



            if not newMatch == []:
                #newMatch[3] = indexKey
                listMatchesTemp.append(newMatch)

                #newMatch.append(item[0])
                #newMatch.append(dicTwo[item[0]][1])
                #newMatch.append(dicTwo[item[0]][2])
                #newMatch.append(item[1])
                #if verbose == True:
                #    print("Matches: " + str(newMatch))

                #newMatchBatch.append(newMatch)
            else:
                listMatchesTemp.append(newMatch)


        #dicOne_Matches[indexKey].append(newMatchBatch)
        indexKey = indexKey + 1

    print ()

    # convert into a serialized json object
    json_results_temp = json.dumps(listMatchesTemp, sort_keys=True, indent=3, ensure_ascii=False)

    #semanticSelectionFile = open(pathSemanticOutput.replace("semantics_TLA-TLA.txt", "semantics_matches_TLA-TLA.txt"),
    #                             "w+")
    #semanticSelectionFile.write(json_results_temp)
    #semanticSelectionFile.close()

    #clean array - keep only the top value (item[5]) for each item in listMatchesTemp sharing the same item[0] and item[3]

    listMatchesTempDict = {}

    # set up progress bar
    indexBar = -1
    print("Progress:")

    for i in range(0, len(listMatchesTemp)):
        indexBar = indexBar + 1
        progbar(indexBar, len(listMatchesTemp) - 1, 20)

        dictTemp = {}
        if not listMatchesTemp[i] == []:
            try:
                listMatchesTempDict[listMatchesTemp[i][0]][listMatchesTemp[i][2]]
            except KeyError:
                try:
                    listMatchesTempDict[listMatchesTemp[i][0]]
                except KeyError:
                    dictTemp[listMatchesTemp[i][2]] = listMatchesTemp[i]
                    listMatchesTempDict[listMatchesTemp[i][0]] = dictTemp
                else:
                    dictTemp[listMatchesTemp[i][2]] = listMatchesTemp[i]
                    listMatchesTempDict[listMatchesTemp[i][0]].update(dictTemp)
            else:
                if listMatchesTemp[i][4] > listMatchesTempDict[listMatchesTemp[i][0]][listMatchesTemp[i][2]][4]:
                    listMatchesTempDict[listMatchesTemp[i][0]][listMatchesTemp[i][2]] = listMatchesTemp[i]

    print()

    listMatchesTempCleaned = []

    for key_1 in listMatchesTempDict:
        for key_2 in listMatchesTempDict[key_1]:
            listMatchesTempCleaned.append(listMatchesTempDict[key_1][key_2])

    listMatchesTempCleanedOrganized = []


    listMatchesTempCleanedsplit = []


    previousItem = -1

    batches = -1
    for item in listMatchesTempCleaned: #listMatchesTempCleanedOrganized:
        if not previousItem == item[0]:
            previousItem = item[0]
            batches = batches+1
            listMatchesTempCleanedsplit.append([])
            listMatchesTempCleanedsplit[batches].append(item)
        else:
            if listMatchesTempCleanedsplit[batches][-1][4] > item[4]:

                listMatchesTempCleanedsplit[batches].append(item)
            else:
                for n in range(0, len(listMatchesTempCleanedsplit[batches])):
                    if listMatchesTempCleanedsplit[batches][n][4] <= item[4]:
                        listMatchesTempCleanedsplit[batches].insert(n, item)
                        break



    # idendify clusters

    #thresholdClusters = 2

    # set up progress bar
    indexBar = -1
    print("Calculate clusters:")
    print("Progress:")

    for z in range(0,len(listMatchesTempCleanedsplit)):
        entry = listMatchesTempCleanedsplit[z].copy()

        indexBar = indexBar + 1
        if len(lexicalDefinitions_One) > 1:
            progbar(indexBar, len(dicOne_Matches) - 1, 20)
        else:
            progbar(indexBar, len(dicOne_Matches), 20)

        upperLevel = {}

        if semanticLevel == 1:
            for item in entry:
                if not DictFields[item[2]][0] in upperLevel:
                    upperLevel[-1] = [item]
                else:
                    upperLevel[-1].append(item)

        if semanticLevel == 2:
            for item in entry:
                if not DictFields[item[2]][0] in upperLevel:
                    upperLevel[DictFields[item[2]][0]] = [item]
                else:
                    upperLevel[DictFields[item[2]][0]].append(item)

        if semanticLevel == 3:
            for item in entry:
                if not DictFields[item[2]][1] in upperLevel:
                    upperLevel[DictFields[item[2]][1]] = [item]
                else:
                    upperLevel[DictFields[item[2]][1]].append(item)

        for key in upperLevel:
            currentList = []


            clusterList = []
            clustersSame = []

            for match in entry:
                if semanticLevel <= 2:
                    levelIndex = 0
                if semanticLevel == 3:
                    levelIndex = 1


                if DictFields[match[2]][levelIndex] == key:
                    if match[4] == 1.0:
                        currentList.append(1)
                        clusterList.append(match[4])
                    else:
                        currentList.append(0)
                        clusterList.append(match[4])
                else:
                    currentList.append(-1)
                    clusterList.append(-1)


            if len(clusterList) > 3:
                listOthers = []
                clusterListTemp = []
                for n in range (0, len(clusterList)):
                    if clusterList[n] == -1:
                        listOthers.append(n)
                    else:
                        clusterListTemp.append(clusterList[n])

                listOfClusters_temp = []

                areItemsListClusterDifferent = all_same(clusterListTemp)

                if (len(clusterListTemp) > 3 and areItemsListClusterDifferent == False):

                    listOfClusters_temp = clusteringFunction(clusterListTemp)
                else:
                    for item in clusterListTemp:
                        listOfClusters_temp.append(1)

                for n in range(0, len(listOthers)):
                    listOfClusters_temp.insert(listOthers[n], -1)


            else:
                listOfClusters_temp = []
                for item in clusterList:
                    listOfClusters_temp.append(0)

            listOfClusters = listOfClusters_temp

            nr_item = 0
            for nr_item in range(0, len(currentList)):
                if currentList[nr_item] == 1:
                    indexCluster = 0
                    break
                if currentList[nr_item] == 0:
                    indexCluster = 1
                    break
                if len(entry[nr_item]) == 5:#
                    entry[nr_item].append(-1)#

            for nr_item in range(0, len(entry)):
                if len(entry[nr_item]) == 5:
                    if indexCluster < thresholdClusters:
                        entry[nr_item].append(indexCluster)
                        lastIndexCluster = listOfClusters[nr_item]

                        break



            for i in range(nr_item +1, len(listOfClusters)):

                if len(lexicalDefinitions_One) > 1 and len(listMatchesTempCleanedsplit) > 1:
                    progbar(indexBar, len(listMatchesTempCleanedsplit) - 1, 20)
                else:
                    progbar(indexBar, len(listMatchesTempCleanedsplit), 20)


                if not currentList[i] == -1:
                    if not listOfClusters[i] == lastIndexCluster:
                        lastIndexCluster = listOfClusters[i]
                        indexCluster = indexCluster + 1
                    if thresholdClusters == None or indexCluster < thresholdClusters:
                        entry[i].append(indexCluster)
                else:
                    entry[i] = entry[i]


        listMatchesTempCleanedsplit[z] = entry.copy()

    for z in range(0, len(listMatchesTempCleanedsplit)):
        entry = listMatchesTempCleanedsplit[z].copy()
        for i in range(0, len(entry)):
            if len(entry[i]) == 5 or entry[i][-1] == -1:
                entry[i] = []
        listMatchesTempCleanedsplit[z] = entry.copy()


    print ()

    #remove empty match, that are below the cluster threshold
    for i in range(0, len(listMatchesTempCleanedsplit)):
        listMatchesTempCleanedsplit[i] = list(filter(None, listMatchesTempCleanedsplit[i]))


    #if verbose == True:
    #    print("Final dataset: " + str(dicOne_Matches))




    #convert into a serialized json object
    json_results_temp = json.dumps(listMatchesTempCleanedsplit, sort_keys=True, indent=3, ensure_ascii=False)

    #semanticSelectionFile = open(pathSemanticOutput.replace("semantics_TLA-TLA.txt", "semantics_batches_TLA-TLA.txt"), "w+")
    #semanticSelectionFile.write(json_results_temp)
    #semanticSelectionFile.close()

    #dicOne_Matches[i].append([])
    # set up progress bar
    indexBar = -1
    print("Clean data:")
    print("Progress:")
    indexToken = 0
    for z in range(0, len(dicOne_Matches)):
        token = dicOne_Matches[z]

        indexBar = indexBar + 1

        if len(lexicalDefinitions_One) > 1:
            progbar(indexBar, len(dicOne_Matches) - 1, 20)
        else:
            progbar(indexBar, len(dicOne_Matches), 20)


        for batchMatches in listMatchesTempCleanedsplit:

            if not batchMatches == []:
                matchesToAdd = []
                newMatchToAdd = []
                if indexToken == batchMatches[0][0]:
                    #for each match -> edit and append

                    for match in batchMatches:
                        newMatchToAdd = []
                        matchID_item = match[2]
                        matchID_meaning = match[3]

                        newMatchToAdd.append(matchID_item)
                        newMatchToAdd.append(dicTwo[matchID_item][1])
                        newMatchToAdd.append(dicTwo[matchID_item][2])
                        newMatchToAdd.append(match[4])
                        matchesMeaning = []
                        matchesMeaning.append(lexicalDefinitionsBase_One[match[1]])
                        matchesMeaning.append(lexicalDefinitionsBase_Two[match[3]])
                        newMatchToAdd.append(matchesMeaning)
                        #add index cluster
                        newMatchToAdd.append(match[5])
                        matchesToAdd.append(newMatchToAdd)
                    token[3] = matchesToAdd
                #else:
                    #token[3] = [[]]

            dicOne_Matches[z] = token.copy()
        indexToken = indexToken +1

    print ()

    # format the results into a json object
    results = {}

    ID_token = -1

    # set up progress bar
    indexBar = -1
    print("Progress:")



    for item in dicOne_Matches:

        indexBar = indexBar + 1
        if len(lexicalDefinitions_One) > 1:
            progbar(indexBar, len(dicOne_Matches) - 1, 20)
        else:
            progbar(indexBar, len(dicOne_Matches), 20)



        ID_token = ID_token + 1

        ID_token_str = str(ID_token)

        if len(ID_token_str) == 1:
            ID_token_normalized = "00000" + ID_token_str
        if len(ID_token_str) == 2:
            ID_token_normalized = "0000" + ID_token_str
        if len(ID_token_str) == 3:
            ID_token_normalized = "000" + ID_token_str
        if len(ID_token_str) == 4:
            ID_token_normalized = "00" + ID_token_str
        if len(ID_token_str) == 5:
            ID_token_normalized = "0" + ID_token_str


        tokenTemp = {}
        tokenTemp["00_ID_token"] = int(item[0])
        tokenTemp["01_Meaning_token"] = item[1]
        tokenTemp["02_Form_token"] = item[2]

        batchTemp = {}
        ID_match = -1
        for match in item[3]:
            #if match == []:#
            #    batchTemp = {}#
            #else:

            if match[3] >= semanticThreshold:

                ID_match = ID_match +1
                matchTemp = {}
                matchTemp['00_ID_Match'] = int(lexicalID_Two[match[0]])
                #matchTemp['01_Meaning_Match'] = "x"
                #matchTemp['02_Form_Match'] = match[2]
                matchTemp['03_Best_Match_Sem'] = match[4]
                matchTemp['05_ID_Cluster'] = match[5]
                matchTemp['06_Sim_Score_Sem_Match'] = match[3]
                matchTemp['11_Semantic_Field'] = match[1]

                ID_match_str = str(ID_match)

                if len(ID_match_str) == 1:
                    ID_match_normalized = "00000"+ID_match_str
                if len(ID_match_str) == 2:
                    ID_match_normalized = "0000"+ID_match_str
                if len(ID_match_str) == 3:
                    ID_match_normalized = "000"+ID_match_str
                if len(ID_match_str) == 4:
                    ID_match_normalized = "00"+ID_match_str
                if len(ID_match_str) == 5:
                    ID_match_normalized = "0"+ID_match_str


                batchTemp[ID_match_normalized] = matchTemp

        if semanticLevel == 1:
            levelTemp = {}
            levelTemp["Level_01"] = batchTemp
            tokenTemp["03_Matches"] = levelTemp
            results[ID_token_normalized] = tokenTemp
        else:
            if semanticLevel == 2:
                previousDataset[ID_token_normalized]["03_Matches"]["Level_02"] = batchTemp

            if semanticLevel == 3:
                previousDataset[ID_token_normalized]["03_Matches"]["Level_03"] = batchTemp

    if semanticLevel > 1:
        results = previousDataset

    print ()

    print ( "Wait... converting to json...")
    #convert into a serialized json object
    json_results = json.dumps(results, sort_keys=True, indent=3, ensure_ascii=False)

    #semanticSelectionFile = open(pathSemanticOutput, "w+")
    #semanticSelectionFile.write(json_results)
    #semanticSelectionFile.close()

    #if verbose == True:
    #    print(json_results)

    print("* End *")
    return json_results



