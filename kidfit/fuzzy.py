import numpy as np
import skfuzzy as fuzz
from django.shortcuts import render
import requests
import json


def output(request):

    # get measurements from form requests
    weight = np.asarray([float(request.POST.get('weight'))])
    height = np.asarray([float(request.POST.get('height'))])
    inseam = np.asarray([float(request.POST.get('inseam'))])
    chest = np.asarray([float(request.POST.get('chest'))])
    waist = np.asarray([float(request.POST.get('waist'))])
    hip = np.asarray([float(request.POST.get('hip'))])
    foot = np.asarray([float(request.POST.get('foot'))])
    measurement = request.POST.get('measurement', 'centimeters')

    # convert inches requests to cm
    if measurement == "inches":
        weight = weight * 0.453592
        height = height * 2.54
        inseam = inseam * 2.54
        chest = chest * 2.54
        waist = waist * 2.54
        hip = hip * 2.54
        foot = foot * 2.54

    # check if user choose inches or centimeters
    inch = None
    cent = None

    if measurement == "inches":
        inch = 1
    elif measurement == "centimeters":
        cent = 1

    # get gender
    gender = request.POST.get('gender')

    # initialization
    evalfinalsize = {}
    size = []
    percentsize = []
    finalsize = []
    finalpercentsize = []

    # calculate polo size chart
    with open('static/polokidsv2.json', 'r') as x:
        brandChart = json.load(x)

    finalsize, finalpercentsize = evaluate(
        brandChart, weight, height, inseam, chest, waist, hip, foot, gender)
    size.append(finalsize)
    percentsize.append(finalpercentsize)

    # calculate h&m size chart
    with open('static/hmkidsv2.json', 'r') as x:
        brandChart = json.load(x)

    finalsize, finalpercentsize = evaluate(
        brandChart, weight, height, inseam, chest, waist, hip, foot, gender)
    size.append(finalsize)
    percentsize.append(finalpercentsize)

    # calculate guess size chart
    with open('static/guess.json', 'r') as x:
        brandChart = json.load(x)

    finalsize, finalpercentsize = evaluate(
        brandChart, weight, height, inseam, chest, waist, hip, foot, gender)
    size.append(finalsize)
    percentsize.append(finalpercentsize)

    # R LANGUAGE REFERENCE
    # print(size)
    # print(percentsize)
    # evalfinalsize =
    # retrieve loop through one part for one table
    # compare minimum all part for one size
    # compare maximum for all size

    # T2height = fuzz.trimf(x, [88, 89.75, 93])
    # T3height = fuzz.trimf(x, [88, 96.5, 100])
    # T4height = fuzz.trimf(x, [88, 104.22, 108])
    # T5height = fuzz.trimf(x, [88, 111.94, 116])
    # T6height = fuzz.trimf(x, [88, 118.71, 123])
    # T7height = fuzz.trimf(x, [88, 129.31, 134])

    # T2weight = fuzz.trimf(y, [13, 13.51, 14])
    # T3weight = fuzz.trimf(y, [13, 15.44, 16])
    # T4weight = fuzz.trimf(y, [13, 17.37, 18])
    # T5weight = fuzz.trimf(y, [13, 19.3, 20])
    # T6weight = fuzz.trimf(y, [13, 21.23, 22])
    # T7weight = fuzz.trimf(y, [13, 24.125, 25])

    # T2waist = fuzz.trimf(z, [42.5, 48.25, 50])
    # T3waist = fuzz.trimf(z, [42.5, 49.22, 51])
    # T4waist = fuzz.trimf(z, [42.5, 50.18, 52])
    # T5waist = fuzz.trimf(z, [42.5, 51.15, 53])
    # T6waist = fuzz.trimf(z, [42.5, 53.08, 55])
    # T7waist = fuzz.trimf(z, [42.5, 54.04, 56])

    # T2=min(T2height,T2weight,T2waist)
    # T3=min(T3weight,T3weight,T3weight)
    # T4=min(T4height,T4weight,T4waist)
    # T5=min(T5height,T5weight,T5waist)
    # T6=min(T6height,T6weight,T6waist)
    # T7=min(T7height,T7weight,T7waist)

    # print(T2, T3, T4, T5, T6, T7)

    # BestFit=max(T2, T3, T4,T5, T6, T7)

    # print(BestFit)
    # [{'boys': '7', 'girls': '6x'}, 'ralph lauren']
    # 'BestFit':evalfinalsize,
    # , 'boys':finalsize[0]["boys"], 'girls':finalsize[0]["girls"]
    # counter = 0

    highest_percentage_belts = None  # initialize for highest matching for belts
    highest_percentage = 0

    for item in size:  # filter for highest matching for belts
        for key, value in item[0].items():
            if 'belts' in key:
                percentage = float(value[1])
                if percentage > highest_percentage:  # select the highest percentage
                    highest_percentage = percentage
                    highest_percentage_belts = item

    highest_belts = {
        'highest_belts_item': highest_percentage_belts,  # insert so it can be return
    }

    highest_percentage_shoes = None  # repitition for highest matching shoes
    highest_percentage = 0

    for item in size:
        for key, value in item[0].items():
            if 'shoes' in key:
                percentage = float(value[1])
                if percentage > highest_percentage:
                    highest_percentage = percentage
                    highest_percentage_shoes = item


    # print("percentsize")
    # print(percentsize)
    print("size")
    print(size)

    return render(request, 'base.html', {'size': size, 'highest_belts': highest_belts, 'highest_shoes': highest_shoes, 'weight': float(request.POST.get('weight', 0)), 'height': float(request.POST.get('height', 0)), 'inseam': float(request.POST.get('inseam', 0)), 'chest': float(request.POST.get('chest', 0)), 'waist': float(request.POST.get('waist', 0)), 'hip': float(request.POST.get('hip', 0)), 'foot': float(request.POST.get('foot', 0)), 'inch': inch, 'cent': cent, 'gender': gender})



def evaluateBoth(brandChart, weight, height, inseam, chest, waist, hip, foot, gender):

    # initialization
    evalfinalsize = {}
    evalfinalpercent = {}
    evalfinalfit = {}
    finalsize = []
    finalpercentsize = []

    for loopCategory in brandChart:
        evalsize = {}

        evaluateweight = []  # weight
        evaluateheight = []  # height
        evaluateinseam = []  # inseam
        evaluatechest = []  # chest
        evaluatewaist = []  # waist
        evaluatehip = []  # hip
        evaluatefoot = []  # foot

        # loop through rows in table
        for part in loopCategory:

            if 'weight cm' in part[0]:
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
                        fuzzy = fuzz.trimf(
                            weight, [round(lower, 2), round(middle, 2), j])
                        evaluateweight.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(
                                weight, [round(lower, 2), round(middle, 2), j[1]])
                            evaluateweight.append(fuzzy)

            if 'height cm' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(
                            height, [round(lower, 2), round(middle, 2), j])
                        evaluateheight.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(
                                height, [round(lower, 2), round(middle, 2), j[1]])
                            evaluateheight.append(fuzzy)

            if 'inside cm' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(
                            inseam, [round(lower, 2), round(middle, 2), j])
                        evaluateinseam.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(
                                inseam, [round(lower, 2), round(middle, 2), j[1]])
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
                        fuzzy = fuzz.trimf(
                            chest, [round(lower, 2), round(middle, 2), j])
                        evaluatechest.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(
                                chest, [round(lower, 2), round(middle, 2), j[1]])
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
                        fuzzy = fuzz.trimf(
                            waist, [round(lower, 2), round(middle, 2), j])
                        evaluatewaist.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(
                                waist, [round(lower, 2), round(middle, 2), j[1]])
                            evaluatewaist.append(fuzzy)

            if 'low hip cm' in part[0]:
                for x in range(len(part[1])):
                    j = part[1][x]
                    if isinstance(part[1][0], float):
                        lower = 0.85*part[1][0]
                    else:
                        lower = 0.85*part[1][0][1]

                    if isinstance(j, float):
                        middle = 0.965*j
                        fuzzy = fuzz.trimf(
                            hip, [round(lower, 2), round(middle, 2), j])
                        evaluatehip.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(
                                hip, [round(lower, 2), round(middle, 2), j[1]])
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
                        fuzzy = fuzz.trimf(
                            foot, [round(lower, 2), round(middle, 2), j])
                        evaluatefoot.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(
                                foot, [round(lower, 2), round(middle, 2), j[1]])
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
                # maximum value
                evalfinalpercent[loopCategory[-1]
                                 ] = round(float(max(evalsize.values()) * 100))
                evalfinalsize[loopCategory[-1]] = [max(
                    evalsize, key=evalsize.get, default=0), round(float(max(evalsize.values()) * 100))]

    # print("eval final size")
    # print(evalfinalsize)
    # print("eval final percent")
    # print(evalfinalpercent)
    # print("eval final fit")
    # print(evalfinalfit)

    # based on the chosen gender, remove the part for the opposite gender
    if gender == 'girl':
        invalid = {"boys", "big boys", "little boys", "boys fit",
                   "baby", "belts boys", "belts unisex", "unisex"}
    elif gender == 'boy':
        invalid = {"girls", "big girls", "little boys", "girls fit",
                   "baby", "belts girls", "belts unisex", "unisex"}

    evalfinalsize = without_keys(evalfinalsize, invalid)
    evalfinalpercent = without_keys(evalfinalpercent, invalid)

    # append brand name for the result
    finalsize.append(evalfinalsize)
    finalsize.append(brandChart[-1])
    finalpercentsize.append(evalfinalpercent)
    finalpercentsize.append(brandChart[-1])

    # print("final percent size")
    # print(finalpercentsize)

    # print("final size")
    # print(finalsize)

    return finalsize, finalpercentsize


def without_keys(array, keys):
    return {k: v for k, v in array.items() if k not in keys}
