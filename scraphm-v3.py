import urllib.request
from bs4 import BeautifulSoup
import json
import lxml.html as lh
import pandas as pd
import requests
import re
import numpy as np
import skfuzzy as fuzz

url = "https://static.zara.net/static/sizeGuide/kids_studio/sizeguide_kids_studio_-1.html?v.1.0.1"
page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

#if nak use beutiful soup
request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(request).read()
soup = BeautifulSoup(html,'html.parser')
kids = soup.findAll("table")
print(kids)

#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <table>..</table> of HTML
table = doc.xpath('//table')
# print(table)
# exit()
caption = doc.xpath("//*[@class='js-toggle-trigger toggle-button has-image']")

onetable=[] 

#loop table dan clean supaya kita boleh simpan data untuk digunakan kemudian
for tab in table:   
    col=[]
    i=0	
    tr = tab.xpath('.//tr') #table row
	
    try:
        for t in tr[0]: #table row pertama (age)
            i+=1
            name=t.text_content().lower()
            #print(name)
            col.append((name,[]))
    except IndexError:
        print("")

    for j in range(1,len(tr)):
        #T is our j'th row
        T=tr[j]

        #i is the index of our column
        i=0
		
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content().lower() 
            # print(data)
            #Check if row is empty
            if i>0:
                if 'kg' in data:
                    data = data.replace("kg","")

                if '<' in data:
                    data = data.replace("<","")
		
                if '/' in data:
                    data = data.replace("/", "-")

                if '-' in data:
                    data = data.replace("½", ".5")
                    data = data.replace("¼", ".25")
                    data = data.replace("¾", ".75")
                    data = data.replace("x", "")
                    data=data.replace(',','.')
                    data=data.replace('″','')
                    data=re.split(r'\s|-', data)
                    # data.replace('-', ' ').split(' ')
                    try:
                        data = [float(i) for i in data] #change to float untuk numerical value untuk calculation
                    except:
                        pass
                else:

                    data=data.replace("½",".5")
                    data=data.replace("¼",".25")
                    data=data.replace("¾",".75")
                    data=data.replace("x","")
                    if ".," in data:
                        data = data.replace(',','')
                    else:
                        data=data.replace(',','.')
                    try:
                        data=float(data)
                    except:
                        pass

            #Append the data to the empty list of the i'th column
            # print(data)
            col[i][1].append(data)
            #Increment i for the next column
            i+=1


    onetable.append(col)
#print(onetable)
#exit()
onetable[0].append("unisex")
onetable[1].append("unisex")
onetable[2].append("girls")
onetable[3].append("boys")
onetable[4].append("unisex")
onetable[5].append("girls")
onetable[6].append("boys")
onetable[7].append("socks")
onetable[8].append("baby") 
onetable[9].append("unisex")
onetable[10].append("gloves")
onetable[11].append("gloves")
onetable[12].append("hats")
onetable[13].append("hats")
onetable[14].append("belts")

# transpose table 
onetablev2=[]
for x in range(len(onetable)):

    Dict = {title:column for (title,column) in onetable[x][0:(len(onetable[x])-1)]}
    col = []
    listH = []
    df = pd.DataFrame(Dict)
    h = list(df.columns.values); 
    listH.append(h)
    v = df.values.tolist();
    listH.extend(v)

    for y in range(len(listH)):
        try:
            get1stcol = listH[y][0]
            data = listH[y][1:(len(listH[y])-1)]
            col.append([get1stcol, []])
            col[y][1].extend(data)
            y = y + 1
        except:
            pass

    onetablev2.append(col)
    x=x+1

onetablev2[0].append("unisex")
onetablev2[1].append("unisex")
onetablev2[2].append("girls")
onetablev2[3].append("boys")
onetablev2[4].append("unisex")
onetablev2[5].append("girls")
onetablev2[6].append("boys")
onetablev2[7].append("socks")
onetablev2[8].append("baby") 
onetablev2[9].append("unisex")
onetablev2[10].append("gloves")
onetablev2[11].append("gloves")
onetablev2[12].append("hats")
onetablev2[13].append("hats")
onetablev2[14].append("belts")


onetablev2.append("zara")

#print(onetablev2)
# exit()

# with open('hmkidsv2.json', 'w', encoding='utf-8') as f:
# 	json.dump(onetable, f, ensure_ascii=False, indent=4)

# with open('hmkidsv2.json', 'w', encoding='utf-8') as f:
# 	json.dump(onetablev2, f, ensure_ascii=False, indent=4)

with open('zarakids-training.json', 'w', encoding='utf-8') as f:
	json.dump(onetablev2, f, ensure_ascii=False, indent=4)

#end of scrapping

# weight = np.asarray([20]) #cth usee data dimasukkan guna array sebab requirement fuzzy
# height = np.asarray([110])
# inseam = np.asarray([60])
# chest = np.asarray([58])
# waist = np.asarray([54])
# hip = np.asarray([60])
# foot = np.asarray([21])

# evaluate(onetablev2, weight, height, inseam, chest, waist, hip, foot)

def evaluate(brandChart, weight, height, inseam, chest, waist, hip, foot, gender):

    #initialization
    evalfinalsize = {}
    evalfinalpercent = {}
    evalfinalfit = {}
    finalsize = []
    finalpercentsize = []
	
    # loop through table
    for loopCategory in brandChart:
        evalsize = {}

        evaluateweight = [] # weight
        evaluateheight = [] # height
        evaluateinseam = [] # inseam
        evaluatechest = [] # chest
        evaluatewaist = [] # waist
        evaluatehip = [] # hip
        evaluatefoot = [] # foot

        # loop through rows in table
        for part in loopCategory:
			
            if 'weight kg' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]

                    # check if size is one value or multiple values
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    # check if size is one value or multiple values
                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(weight, [round(lower,2), round(middle,2), j])
                        evaluateweight.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(weight, [round(lower,2), round(middle,2), j[1]])
                            evaluateweight.append(fuzzy)

            if 'eur/height cm' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(height, [round(lower,2), round(middle,2), j])
                        evaluateheight.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(height, [round(lower,2), round(middle,2), j[1]])
                            evaluateheight.append(fuzzy)
				
            #print(evaluateheight)
            

            if 'inside cm' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(inseam, [round(lower,2), round(middle,2), j])
                        evaluateinseam.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(inseam, [round(lower,2), round(middle,2), j[1]])
                            evaluateinseam.append(fuzzy)

            if 'chest cm' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(chest, [round(lower,2), round(middle,2), j])
                        evaluatechest.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(chest, [round(lower,2), round(middle,2), j[1]])
                            evaluatechest.append(fuzzy)
			
            if 'waist cm' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(waist, [round(lower,2), round(middle,2), j])
                        evaluatewaist.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(waist, [round(lower,2), round(middle,2), j[1]])
                            evaluatewaist.append(fuzzy)

            if 'hip cm' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(hip, [round(lower,2), round(middle,2), j])
                        evaluatehip.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(hip, [round(lower,2), round(middle,2), j[1]])
                            evaluatehip.append(fuzzy)

            if 'length cm' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(foot, [round(lower,2), round(middle,2), j])
                        evaluatefoot.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(foot, [round(lower,2), round(middle,2), j[1]])
                            evaluatefoot.append(fuzzy)
                # print(evaluatefoot)
                # print(foot)
                # print("endd")

        # find length of array baseline
        if len(evaluateheight) > 0:
            arrlength = len(evaluateheight)
        elif len(evaluatewaist) > 0:
            arrlength = len(evaluatewaist)
        elif len(evaluatefoot) > 0:
            arrlength = len(evaluatefoot)
        else:
            arrlength = 0

        # list of evaluation for all parts (weight, height, etc) per category 
        listOfEvaluation = []
		
        for x in range(arrlength):
            if len(evaluateheight) == 0:
                k = 0
            else:
                k = evaluateheight[x]
            if len(evaluateweight) == 0:
                l = 0
            else:
                l = evaluateweight[x]
            if len(evaluatewaist) == 0:
                m = 0
            else:
                m = evaluatewaist[x]
            if len(evaluateinseam) == 0:
                n = 0
            else:
                n = evaluateinseam[x]
            if len(evaluatechest) == 0:
                o = 0
            else:
                o = evaluatechest[x]
            if len(evaluatehip) == 0:
                p = 0
            else:
                p = evaluatehip[x]
            if len(evaluatefoot) == 0:
                r = 0
            else:
                r = evaluatefoot[x]
			
            # compile parts evaluation per category
            partsEvaluation = [k, l, m, n, o, p, r]

            # find minimum value 
            size = min((y for y in partsEvaluation if y > 0), default=0)
            listOfEvaluation.append(partsEvaluation)

            # assign the minimum value to the size category eg -  'xl': array([0.38578487]
            evalsize[loopCategory[0][1][x]] = size

        # print("list of evaluation")
        # print(listOfEvaluation)

        # print("size evaluation")
        # print(evalsize)

        if evalsize:
            # find max value from all sizes
            # eg. {'7-8': 0, '8-9': array([0.93612872]), '9-10': array([0.67567568]), '10-11': array([0.59831723]), '11-12': array([0.50686378]), '12-13': array([0.43966109]), '13-14': array([0.38819248])}

            if max(evalsize.values()) != 0:
                # evalfinalfit[loopCategory[-1]] =  listOfEvaluation[list(evalsize).index(max(evalsize, key=evalsize.get, default=0))]
                print(loopCategory[-1])
                evalfinalpercent[loopCategory[-1]] = round(float(max(evalsize.values()) * 100))  # maximum value
                evalfinalsize[loopCategory[-1]] = [max(evalsize, key=evalsize.get, default=0), round(float(max(evalsize.values()) * 100))]

    print("eval final size")
    print(evalfinalsize)
    print("eval final percent")
    print(evalfinalpercent)
    # print("eval final fit")
    # print(evalfinalfit)

    # based on the chosen gender, remove the part for the opposite gender
    if gender == 'girl':
        invalid = {"boys", "big boys", "little boys", "boys fit", "baby", "belts boys", "belts unisex", "unisex"}
    elif gender == 'boy':
        invalid = {"girls", "big girls", "little boys", "girls fit", "baby", "belts girls", "belts unisex", "unisex"}

    evalfinalsize = without_keys(evalfinalsize, invalid)
    evalfinalpercent = without_keys(evalfinalpercent, invalid)

    #append brand name for the result
    finalsize.append(evalfinalsize)
    finalsize.append(brandChart[-1])
    finalpercentsize.append(evalfinalpercent)
    finalpercentsize.append(brandChart[-1])

    print("final percent size")
    print(finalpercentsize)

    print("final size")
    print(finalsize)

    return finalsize, finalpercentsize


def without_keys(array, keys):
    return {k:v for k,v in array.items() if k not in keys}


weight = np.asarray([25])
height = np.asarray([128])
inseam = np.asarray([62])
chest = np.asarray([65])
waist = np.asarray([62])
hip = np.asarray([76])
foot = np.asarray([24])
gender = "boy"

evaluate(onetablev2, weight, height, inseam, chest, waist, hip, foot, gender)
