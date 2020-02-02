
import datetime
import json

from .semanticComparison_tagged_multiLevel import semanticComparison_tagged_multiLevel

from .progbar import progbar

def ASeT(LexicalList, SemanticTags, pathModel, pathOutput, numberLevels = 2, numberMatchesOutput=None, verbose = True, splitMenings = True, dividers = [","], semanticThreshold_lvl1 = 0.1, semanticThreshold_lvl2 = 0.45, semanticThreshold_lvl3 = 0.45, thresholdClusters_lvl1 = 2, thresholdClusters_lvl2 = 2, thresholdClusters_lvl3 = 2): #, pathTime, pathSemanticOutput, pathSemanticInput, parseSemantics = True,
    """
    :param LexicalList: first lexical list to compare
            -- format: list of list: [each entry: [ ID (int), meanings (string, with separators), forms (array of strings, unicode IPA) ]]
    :param SemanticTags: list of semantic tags
            -- format: list of list: [each entry: [ ID (int), meanings (string, no separators), ID top semantic level (int - if already top = -1), ID second from top semantic level (int - if already top or second from top = -1) ]]
    :param pathModel: path to saved semantic model (string)
    :param pathOutput: path to save the results (string - no extention; e.g. /my/folder/name_file_with_my_results)
    :param numberLevels: number of semantic levels to take into account (int)
            -- default = 2
    :param numberMatchesOutput: number of matches to be output by the semantic model (int)
            -- default: None = unassigned = return all matches
    :param semanticThreshold: Threshold to accept a semantic match (float)
            -- default: 0.45
    :param verbose: print data during execution (boolean)
            -- default: True
    :param splitMenings: split meaning according to dividers, compare each individualy (boolean)
            -- default: True
    :param dividers: dividers used to split meanings (array of strings [string, string]
            -- default: [","]
    :param thresholdClusters_lvl1: N-best clusters to take into account in the results for the semantic level 1 (int)
            -- default: 2
    :param thresholdClusters_lvl2: N-best clusters to take into account in the results for the semantic level 2 (int)
            -- default: 2
    :param thresholdClusters_lvl3: N-best clusters to take into account in the results for the semantic level 3 (int)
            -- default: 2
    """



    #=========

    #time = open(pathTime, "a")

    #time.write("start: " + str(datetime.datetime.now()) + "\n")
    #time.close()

    #=========

    splitMeanings = True
    dividers = [","]

    semanticSelection = ""

    #if parseSemantics == True:



    json_semanticSelection = semanticComparison_tagged_multiLevel(LexicalList, SemanticTags,
                                                                  pathModel, 1, None, numberMatchesOutput, verbose, semanticThreshold_lvl1, splitMeanings, dividers, thresholdClusters_lvl1)

    if numberLevels > 1:
        json_semanticSelection = semanticComparison_tagged_multiLevel(LexicalList, SemanticTags, pathModel,\
                                                                      2, json_semanticSelection, numberMatchesOutput,\
                                                                      verbose, semanticThreshold_lvl2, splitMenings,\
                                                                      dividers, thresholdClusters_lvl2)

    if numberLevels > 2:
        json_semanticSelection = semanticComparison_tagged_multiLevel(LexicalList, SemanticTags, pathModel,\
                                                                      3, json_semanticSelection, numberMatchesOutput,\
                                                                      verbose, semanticThreshold_lvl3, splitMenings,\
                                                                      dividers, thresholdClusters_lvl3)

    print("============")

    #else:

     #   print("Load semantic analysis")

      #  pathSemanticInput = pathSemanticOutput

       # fileRead = open(pathSemanticInput, "r")
        #json_semanticSelection = fileRead.read()

    print ("- - - - - - - - - ")

    #print (json_semanticSelection)

    semanticSelectionResults = json.loads(json_semanticSelection)

    resultsSimplified = []
    resultsSimplifiedString = ""

    for ID_token in semanticSelectionResults:
        entryResult = {}
        entry = semanticSelectionResults[ID_token]
        for level in entry["03_Matches"]:
            for match in entry["03_Matches"][level]:
                entryResult["01_Entry_ID"] = str(ID_token)
                entryResult["02_Entry_Form"] = ", ".join(entry["02_Form_token"])
                entryResult["03_Entry_Meaning"] = entry["01_Meaning_token"]
                entryResult["04_Match_Level"] = str(level)
                entryResult["05_Cluster_Match"] = str(entry["03_Matches"][level][match]["05_ID_Cluster"])
                entryResult["06_ID_Match"] = str(entry["03_Matches"][level][match]["00_ID_Match"])
                entryResult["07_Semantic_Tag"] = entry["03_Matches"][level][match]["11_Semantic_Field"]
                entryResult["08_Semantic_Similarity"] = str(entry["03_Matches"][level][match]['06_Sim_Score_Sem_Match'])

                prefix = ""
                for z in range(0, int(level.replace("Level_", ""))-1):
                    prefix = prefix + "\t"
                if verbose == True:
                    print (prefix + entryResult["01_Entry_ID"] + " - '" + ", ".join(entry["02_Form_token"]) + "' - " + entryResult["03_Entry_Meaning"] + " :: lvl: " + entryResult["04_Match_Level"] + " Nr. Cluster: " + entryResult["05_Cluster_Match"] + " , Tag: " + entryResult["06_ID_Match"] + " - " + entryResult["07_Semantic_Tag"] + " - Sim. Score: " + entryResult["08_Semantic_Similarity"])
                resultsSimplifiedString = resultsSimplifiedString + prefix + entryResult["01_Entry_ID"] + " - '" + ", ".join(entry["02_Form_token"]) + "' - " + entryResult["03_Entry_Meaning"] + " :: lvl: " + entryResult["04_Match_Level"] + " Nr. Cluster: " + entryResult["05_Cluster_Match"] + " , Tag: " + entryResult["06_ID_Match"] + " - " + entryResult["07_Semantic_Tag"] + " Sim. Score: " + entryResult["08_Semantic_Similarity"] + "\n"
            if verbose == True:
                if not level == sorted(entry["03_Matches"].keys())[-1]:
                      print ("- - - - - - - - -")
                resultsSimplifiedString = resultsSimplifiedString + "- - - - - - - - -" + "\n"
        if verbose == True:
            print("= = = = = =")
            resultsSimplifiedString = resultsSimplifiedString + "= = = = = =" + "\n"

        resultsSimplified.append(entryResult)

    Results = open(
        pathOutput + ".json",
        "w")  

    Results.write(json_semanticSelection)
    Results.close()

    ResultsSimplified = open(
        pathOutput + "_simplified.txt",
        "w")  

    ResultsSimplified.write(resultsSimplifiedString)
    ResultsSimplified.close()

    #if verbose == True:
    #    print()
    #    print(json_semanticSelection)

    return resultsSimplified, json_semanticSelection