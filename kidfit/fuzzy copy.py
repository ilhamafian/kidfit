import numpy as np
import skfuzzy as fuzz
from django.shortcuts import render
import requests
import json


def output(request):
    category = int(request.POST.get('category'))
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
    topsize = []
    bottomsize = []
    percentsize = []
    finalsize = []
    finalpercentsize = []

    if category == 1:

        # get measurements from form requests
        weight = np.asarray([float(request.POST.get('weight'))])
        height = np.asarray([float(request.POST.get('height'))])
        inseam = np.asarray([float(request.POST.get('inseam'))])
        chest = np.asarray([float(request.POST.get('chest'))])
        waist = np.asarray([float(request.POST.get('waist'))])
        hip = np.asarray([float(request.POST.get('hip'))])
        foot = np.asarray([float(request.POST.get('foot'))])

        # calculate polo size chart
        with open('static/polokidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateTop(
            brandChart, weight, height, chest, waist, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        finalsize, finalpercentsize = evaluateBottom(
            brandChart, weight, height, inseam, waist, hip, foot, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate h&m size chart
        with open('static/hmkidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateTop(
            brandChart, weight, height, chest, waist, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        finalsize, finalpercentsize = evaluateBottom(
            brandChart, weight, height, inseam, waist, hip, foot, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate guess size chart
        with open('static/guess.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateTop(
            brandChart, weight, height, chest, waist, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        finalsize, finalpercentsize = evaluateBottom(
            brandChart, weight, height, inseam, waist, hip, foot, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # # Check if 'boys' or 'girls' is present in the first element
        # first_element = topsize[0][0]
        # key_to_sort = 'boys' if 'boys' in first_element else 'girls'

        # # Sort the size list based on the determined key
        # sorted_size = sorted(topsize, key=lambda x: int(
        #     x[0].get(key_to_sort, [0, 0])[1]), reverse=True)

        # print("percentsize")
        # print(percentsize)
        print("top size:")
        print(topsize)

        print("bottom size:")
        print(bottomsize)

        # print("sorted size:")
        # print(sorted_size)
        return render(request, 'topbottom-output.html', {'top_size': topsize, 'bottom_size': bottomsize, 'weight': float(request.POST.get('weight', 0)), 'height': float(request.POST.get('height', 0)), 'inseam': float(request.POST.get('inseam', 0)), 'chest': float(request.POST.get('chest', 0)), 'waist': float(request.POST.get('waist', 0)), 'hip': float(request.POST.get('hip', 0)), 'foot': float(request.POST.get('foot', 0)), 'inch': inch, 'cent': cent, 'gender': gender})

    elif category == 2:

        # get measurements from form requests
        weight = np.asarray([float(request.POST.get('weight'))])
        height = np.asarray([float(request.POST.get('height'))])
        chest = np.asarray([float(request.POST.get('chest'))])
        waist = np.asarray([float(request.POST.get('waist'))])

        # calculate polo size chart
        with open('static/polokidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateTop(
            brandChart, weight, height, chest, waist, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate h&m size chart
        with open('static/hmkidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateTop(
            brandChart, weight, height, chest, waist, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate guess size chart
        with open('static/guess.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateTop(
            brandChart, weight, height, chest, waist, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # print("percentsize")
        # print(percentsize)
        print("top size:")
        print(topsize)

        # print("sorted size:")
        # print(sorted_size)

        return render(request, 'top-output.html', {'top_size': topsize, 'weight': float(request.POST.get('weight', 0)), 'chest': float(request.POST.get('chest', 0)), 'waist': float(request.POST.get('waist', 0)), 'inch': inch, 'cent': cent, 'gender': gender})

    elif category == 3:

        # get measurements from form requests
        weight = np.asarray([float(request.POST.get('weight'))])
        height = np.asarray([float(request.POST.get('height'))])
        inseam = np.asarray([float(request.POST.get('inseam'))])
        waist = np.asarray([float(request.POST.get('waist'))])
        hip = np.asarray([float(request.POST.get('hip'))])
        foot = np.asarray([float(request.POST.get('foot'))])

        # calculate polo size chart
        with open('static/polokidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateBottom(
            brandChart, weight, height, inseam, waist, hip, foot, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate h&m size chart
        with open('static/hmkidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateBottom(
            brandChart, weight, height, inseam, waist, hip, foot, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate guess size chart
        with open('static/guess.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateBottom(
            brandChart, weight, height, inseam, waist, hip, foot, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # print("percentsize")
        # print(percentsize)

        print("bottom size:")
        print(bottomsize)

        # print("sorted size:")
        # print(sorted_size)

        return render(request, 'bottom-output.html', {'bottom_size': bottomsize, 'weight': float(request.POST.get('weight', 0)), 'height': float(request.POST.get('height', 0)), 'inseam': float(request.POST.get('inseam', 0)), 'waist': float(request.POST.get('waist', 0)), 'hip': float(request.POST.get('hip', 0)), 'foot': float(request.POST.get('foot', 0)), 'inch': inch, 'cent': cent, 'gender': gender})


def evaluateTop(brandChart, weight, height, chest, waist, gender):

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
        evaluatechest = []  # chest
        evaluatewaist = []  # waist

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

        # find length of array baseline
        if len(evaluateheight) > 0:
            arrlength = len(evaluateheight)
        elif len(evaluatewaist) > 0:
            arrlength = len(evaluatewaist)
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
            if len(evaluatechest) == 0:
                o = 0
            else:
                o = evaluatechest[x]

            # compile parts evaluation per category
            partsEvaluation = [k, l, m, o]

            # find minimum value
            size = min((y for y in partsEvaluation if y > 0), default=0)
            listOfEvaluation.append(partsEvaluation)

            # assign the minimum value to the size category eg -  'xl': array([0.38578487]
            evalsize[loopCategory[0][1][x]] = size

        if evalsize:

            if max(evalsize.values()) != 0:
                # evalfinalfit[loopCategory[-1]] =  listOfEvaluation[list(evalsize).index(max(evalsize, key=evalsize.get, default=0))]
                # maximum value
                evalfinalpercent[loopCategory[-1]
                                 ] = round(float(max(evalsize.values()) * 100))
                evalfinalsize[loopCategory[-1]] = [max(
                    evalsize, key=evalsize.get, default=0), round(float(max(evalsize.values()) * 100))]

    # based on the chosen gender, remove the part for the opposite gender
    if gender == 'girl':
        invalid = {"boys", "big boys", "little boys", "boys fit",
                   "baby", "belts boys", "belts unisex", "unisex"}
    elif gender == 'boy':
        invalid = {"girls", "big girls", "little girls", "girls fit",
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


def evaluateBottom(brandChart, weight, height, inseam, waist, hip, foot, gender):

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

            if 'hip cm' in part[0]:
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
            if len(evaluatehip) == 0:
                p = 0
            else:
                p = evaluatehip[x]
            if len(evaluatefoot) == 0:
                r = 0
            else:
                r = evaluatefoot[x]

            # compile parts evaluation per category
            partsEvaluation = [k, l, m, n, p, r]

            # find minimum value
            size = min((y for y in partsEvaluation if y > 0), default=0)
            listOfEvaluation.append(partsEvaluation)

            # assign the minimum value to the size category eg -  'xl': array([0.38578487]
            evalsize[loopCategory[0][1][x]] = size

        if evalsize:

            if max(evalsize.values()) != 0:
                # evalfinalfit[loopCategory[-1]] =  listOfEvaluation[list(evalsize).index(max(evalsize, key=evalsize.get, default=0))]
                # maximum value
                evalfinalpercent[loopCategory[-1]
                                 ] = round(float(max(evalsize.values()) * 100))
                evalfinalsize[loopCategory[-1]] = [max(
                    evalsize, key=evalsize.get, default=0), round(float(max(evalsize.values()) * 100))]

    # based on the chosen gender, remove the part for the opposite gender
    if gender == 'girl':
        invalid = {"boys", "big boys", "little boys", "boys fit",
                   "baby", "belts boys", "belts unisex", "unisex"}
    elif gender == 'boy':
        invalid = {"girls", "big girls", "little girls", "girls fit",
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
