from fugashi import Tagger
import csv

tagger = Tagger('-Owakati')

##############################
##      GLOBAL METHODS      ##
##############################

# BubbleSort algorithm (GREATEST to LEAST).
def BubbleSort(list): 
    length = len(list)
    
    for outerIndex in range(length - 1):
        swapped = False
        
        for innerIndex in range(0, length - outerIndex - 1):
            if list[innerIndex + 1][-1] > list[innerIndex][-1]:
                swapped = True
                list[innerIndex + 1], list[innerIndex] = list[innerIndex], list[innerIndex + 1]

        if not swapped:
            return list
    
    return list


def TranslatePOS(POS):
    POStypes = ["補助記号", "助詞", "助動詞", "動詞", "副詞", "接頭辞", "代名詞", "接続詞", "名詞", "形容詞", "接尾辞", "連体詞", "感動詞", "記号", "形状詞"]
    POStranslations = ["Auxiliary Symbol", "Particle", "Auxiliary Verb", "Verb", "Adverb", "Prefix", "Pronoun", "Conjunction", "Noun", "い-Adjective", "Suffix", "Adnominal", "Interjection", "Code", "な-Adjective"]
    
    for index in range(len(POStypes)):
        if (POS == POStypes[index]):
            POS = POStranslations[index]
    
    return POS


def GetLemmaAndPOS(list):
    length = len(list)
    terms = []
    
    for index in range(length - 1):
        incremented = False
        
        for term in terms:
            if(list[index][1] == term[0]):
                term[2] += 1
                incremented = True
                break
            
        if(incremented == False):
            # TODO: Setup so only first POS entry gets added.
            terms.append([list[index][1]]+[list[index][2]]+[1])
    
    return terms


def ParseScript(script):
    text = []
    
    tagger.parse(script)

    for word in tagger(script):
        POS = ""
        
        for index in range(len(word.pos)):
            if(word.pos[index] == ","):
                break
            else:
                POS += word.pos[index]
        
        part = TranslatePOS(POS)
        text.append([word]+[word.feature.lemma]+[part])
    
    return text


def FindOccurrences(text):
    list = []

    for word in text:
        location = 0
        wordAdd = True
        firstTerm = str(word[0])
        
        for term in list:
            secondTerm = str(term[0])
            
            if(firstTerm == secondTerm):
                print("Match Found at: ", location)
                list[location][3] += 1
                wordAdd = False
                break
            else:
                location += 1
        
        if wordAdd:
            list.append(word+[1])
    
    return list


###################################
##      Processing The Data      ##
###################################

# Persona 4 Data...
P4script = open("Text Files/Persona4.txt", "r").read()
P4text = ParseScript(P4script)
P4textTrans = TranslatePOS(P4text)
P4list = FindOccurrences(P4textTrans)
P4lemma = GetLemmaAndPOS(P4textTrans)

P4listSorted = BubbleSort(P4list)
with open("CSV Files/Persona4Words.csv", "w") as CSV:
    P4output = csv.writer(CSV)
    P4output.writerow(["Word", "Lemma", "POS", "# Occurrences"])
    P4output.writerows(P4listSorted)

P4lemmaSorted = BubbleSort(P4lemma)
with open("CSV Files/Persona4Lemma.csv", "w") as CSV:
    P4lemmaOutput = csv.writer(CSV)
    P4lemmaOutput.writerow(["Lemma", "POS", "# Occurrences"])
    P4lemmaOutput.writerows(P4lemmaSorted)

# Persona 5 Data...
P5script = open("Text Files/Persona5.txt", "r").read()
P5text = ParseScript(P5script)
P5textTrans = TranslatePOS(P5text)
P5list = FindOccurrences(P5textTrans)
P5lemma = GetLemmaAndPOS(P5textTrans)

P5listSorted = BubbleSort(P5list)
with open("CSV Files/Persona5Words.csv", "w") as CSV:
    P5output = csv.writer(CSV)
    P5output.writerow(["Word", "Lemma", "POS", "# Occurrences"])
    P5output.writerows(P5listSorted)

P5lemmaSorted = BubbleSort(P5lemma)
with open("CSV Files/Persona5Lemma.csv", "w") as CSV:
    P5lemmaOutput = csv.writer(CSV)
    P5lemmaOutput.writerow(["Lemma", "POS", "# of Occurrences"])
    P5lemmaOutput.writerows(P5lemmaSorted)


# Compare word occurrences || Persona 4 base.
P4comp = P4listSorted.copy()
for index1 in P4comp:
    wordFound = False
    
    for index2 in P5listSorted:
        if (str(index1[0]) == str(index2[0])):
            index1 += [index2[-1]]
            wordFound = True
            P5listSorted.remove(index2)
    
    if(not wordFound):
        index1 += [0]

for index in P5listSorted:
    P4comp.append([index[0]] + [index[1]] + [index[2]] + [0] + [index[3]])

with open("CSV Files/Persona4WordsComparison.csv", "w") as CSV:
    P4compOutput = csv.writer(CSV)
    P4compOutput.writerow(["Word", "Lemma", "POS", "P4 Occurrences", "P5 Occurrences"])
    P4compOutput.writerows(P4comp)

# Compare lemma occurrences || Persona 4 base.
P4lemmaComp = P4lemmaSorted.copy()
for index1 in P4lemmaComp:
    wordFound = False
    
    for index2 in P5lemmaSorted:
        if (str(index1[0]) == str(index2[0])):
            index1 += [index2[-1]]
            wordFound = True
            P5lemmaSorted.remove(index2)

    if(not wordFound):
        index1 += [0]

for index in P5lemmaSorted:
    P4comp.append([index[0]] + [index[1]] + [0] + [index[2]])

with open("CSV Files/Persona4LemmaComparison.csv", "w") as CSV:
    P4lemmaCompOutput = csv.writer(CSV)
    P4lemmaCompOutput.writerow(["Lemma", "POS", "P4 Occurrences", "P5 Occurrences"])
    P4lemmaCompOutput.writerows(P4lemmaComp)


# Compare word occurrences || Persona 5 base.
P5comp = BubbleSort(P4comp)

with open("CSV Files/Persona5WordsComparison.csv", "w") as CSV:
    P5compOutput = csv.writer(CSV)
    P5compOutput.writerow(["Word", "Lemma", "POS", "P4 Occurrences", "P5 Occurrences"])
    P5compOutput.writerows(P5comp)

# Compare lemma occurrences || Persona 5 base.
P5lemmaComp = BubbleSort(P4lemmaComp)

with open("CSV Files/Persona5LemmaComparison.csv", "w") as CSV:
    P5lemmaCompOutput = csv.writer(CSV)
    P5lemmaCompOutput.writerow(["Lemma", "POS", "P4 Occurrences", "P5 Occurrences"])
    P5lemmaCompOutput.writerows(P5lemmaComp)