import numpy as np
import skfuzzy as fuzz
from django.shortcuts import render
import requests
import json


def output(request):

    category = int(request.POST.get('category', 1))
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
        weight = np.asarray([float(request.POST.get('weight', 0.0))])
        height = np.asarray([float(request.POST.get('height', 0.0))])
        inseam = np.asarray([float(request.POST.get('inseam', 0.0))])
        chest = np.asarray([float(request.POST.get('chest', 0.0))])
        waist = np.asarray([float(request.POST.get('waist', 0.0))])
        hip = np.asarray([float(request.POST.get('hip', 0.0))])
        foot = np.asarray([float(request.POST.get('foot', 0.0))])

        # calculate polo size chart
        with open('static/polokidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluatePolo(
            brandChart, weight, height, waist, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        finalsize, finalpercentsize = evaluatePolo(
            brandChart, weight, height, waist, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        with open('static/zaratraining.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateTopZara(
            brandChart, height, chest, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        finalsize, finalpercentsize = evaluateBottomZara(
            brandChart, height, inseam, waist, hip, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate h&m size chart
        with open('static/hmkidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateTopHM(
            brandChart, height, chest, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        finalsize, finalpercentsize = evaluateBottomHM(
            brandChart, height, inseam, waist, hip, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate guess size chart
        with open('static/guess.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateGuess(
            brandChart, weight, height, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        finalsize, finalpercentsize = evaluateGuess(
            brandChart, weight, height, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        def sorting_key(item):
            brand_percentages = []

            for values in item[0].values():
                if isinstance(values, list) and len(values) == 2:
                    percentage = values[1]
                    brand_percentages.append(percentage)

            max_percentage = max(brand_percentages, default=0)
            return max_percentage

        def get_highest_percentage_across_brands(sizes):
            highest_per_brand = {}
            for size in sizes:
                brand = size[1]
                for category, details in size[0].items():
                    # Assuming details is a list where the first item is size and the second item is percentage
                    size_label, percentage = details
                    if brand not in highest_per_brand or highest_per_brand[brand][1][1] < percentage:
                        highest_per_brand[brand] = [
                            category, [size_label, percentage]]

            # Convert the dictionary back to the original format
            result = []
            for brand, (category, details) in highest_per_brand.items():
                result.append([{category: details}, brand])
            return result

        topsizes = get_highest_percentage_across_brands(topsize)
        bottomsizes = get_highest_percentage_across_brands(bottomsize)
        print('topsizes', topsizes)
        # Now you can sort them using sorting_key
        topsize = sorted(topsizes, key=sorting_key, reverse=True)
        bottomsize = sorted(bottomsizes, key=sorting_key, reverse=True)

        print("top size:")
        print(topsize)

        print("bottom size:")
        print(bottomsize)

        # print("sorted size:")
        # print(sorted_size)
        return render(request, 'topbottom-output.html', {'top_size': topsize, 'bottom_size': bottomsize, 'weight': float(request.POST.get('weight', 0)), 'height': float(request.POST.get('height', 0)), 'inseam': float(request.POST.get('inseam', 0)), 'chest': float(request.POST.get('chest', 0)), 'waist': float(request.POST.get('waist', 0)), 'hip': float(request.POST.get('hip', 0)), 'foot': float(request.POST.get('foot', 0)), 'measurement': request.POST.get('measurement', ''), 'inch': inch, 'cent': cent, 'gender': gender})

    elif category == 2:

        # get measurements from form requests
        weight = np.asarray([float(request.POST.get('weight'))])
        height = np.asarray([float(request.POST.get('height'))])
        chest = np.asarray([float(request.POST.get('chest'))])
        waist = np.asarray([float(request.POST.get('waist'))])

        # calculate polo size chart
        with open('static/polokidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluatePolo(
            brandChart, weight, height, waist, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate h&m size chart
        with open('static/hmkidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateTopHM(
            brandChart, height, chest, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate guess size chart
        with open('static/guess.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateGuess(
            brandChart, weight, height, gender)
        topsize.append(finalsize)
        percentsize.append(finalpercentsize)

        def sorting_key(item):
            brand_percentages = []

            for values in item[0].values():
                if isinstance(values, list) and len(values) == 2:
                    percentage = values[1]
                    brand_percentages.append(percentage)

            max_percentage = max(brand_percentages, default=0)
            return max_percentage

        def get_highest_percentage_across_brands(sizes):
            highest_per_brand = {}
            for size in sizes:
                brand = size[1]
                for category, details in size[0].items():
                    # Assuming details is a list where the first item is size and the second item is percentage
                    size_label, percentage = details
                    if brand not in highest_per_brand or highest_per_brand[brand][1][1] < percentage:
                        highest_per_brand[brand] = [
                            category, [size_label, percentage]]

            # Convert the dictionary back to the original format
            result = []
            for brand, (category, details) in highest_per_brand.items():
                result.append([{category: details}, brand])
            return result

        topsizes = get_highest_percentage_across_brands(topsize)

        # Now you can sort them using sorting_key
        topsize = sorted(topsizes, key=sorting_key, reverse=True)
        for item in topsize:
            print('item', item)

        print("top size:")
        print(topsize)

        # print("sorted size:")
        # print(sorted_size)

        return render(request, 'top-output.html', {'top_size': topsize, 'weight': float(request.POST.get('weight', 0)), 'height': float(request.POST.get('height', 0)), 'chest': float(request.POST.get('chest', 0)), 'waist': float(request.POST.get('waist', 0)), 'inch': inch, 'cent': cent, 'gender': gender})

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

        finalsize, finalpercentsize = evaluatePolo(
            brandChart, weight, height, waist, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate h&m size chart
        with open('static/hmkidsv2.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateBottomHM(
            brandChart, height, inseam, waist, hip, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # calculate guess size chart
        with open('static/guess.json', 'r') as x:
            brandChart = json.load(x)

        finalsize, finalpercentsize = evaluateGuess(
            brandChart, weight, height, gender)
        bottomsize.append(finalsize)
        percentsize.append(finalpercentsize)

        # print("percentsize")
        # print(percentsize)
        def sorting_key(item):
            brand_percentages = []

            for values in item[0].values():
                if isinstance(values, list) and len(values) == 2:
                    percentage = values[1]
                    brand_percentages.append(percentage)

            max_percentage = max(brand_percentages, default=0)
            return max_percentage

        def get_highest_percentage_across_brands(sizes):
            highest_per_brand = {}
            for size in sizes:
                brand = size[1]
                for category, details in size[0].items():
                    # Assuming details is a list where the first item is size and the second item is percentage
                    size_label, percentage = details
                    if brand not in highest_per_brand or highest_per_brand[brand][1][1] < percentage:
                        highest_per_brand[brand] = [
                            category, [size_label, percentage]]

            # Convert the dictionary back to the original format
            result = []
            for brand, (category, details) in highest_per_brand.items():
                result.append([{category: details}, brand])
            return result

        bottomsizes = get_highest_percentage_across_brands(bottomsize)

        # Now you can sort them using sorting_key
        bottomsize = sorted(bottomsizes, key=sorting_key, reverse=True)
        for item in bottomsize:
            print('item', item)

        print("Category 3-bottom size:")
        print(bottomsize)

        # print("sorted size:")
        # print(sorted_size)

        return render(request, 'bottom-output.html', {'bottom_size': bottomsize, 'weight': float(request.POST.get('weight', 0)), 'height': float(request.POST.get('height', 0)), 'inseam': float(request.POST.get('inseam', 0)), 'waist': float(request.POST.get('waist', 0)), 'hip': float(request.POST.get('hip', 0)), 'foot': float(request.POST.get('foot', 0)), 'inch': inch, 'cent': cent, 'gender': gender})


def evaluateTopZara(brandChart, height, chest, gender):

    # initialization
    evalfinalsize = {}
    evalfinalpercent = {}
    evalfinalfit = {}
    finalsize = []
    finalpercentsize = []

    for loopCategory in brandChart:
        evalsize = {}

        evaluateheight = []  # height
        evaluatechest = []  # chest

        # loop through rows in table
        for part in loopCategory:

            if 'chest (cm)' in part[0]:
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
                            chest, [round(lower, 2), round(middle, 2), j])
                        evaluatechest.append(fuzzy)
                    else:
                        if len(j) == 2:
                            middle = 0.965*j[1]
                            fuzzy = fuzz.trimf(
                                chest, [round(lower, 2), round(middle, 2), j[1]])
                            evaluatechest.append(fuzzy)

            if 'height (cm)' in part[0]:
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

        # find length of array baseline
        if len(evaluateheight) > 0:
            arrlength = len(evaluateheight)
        else:
            arrlength = 0

        # list of evaluation for all parts (weight, height, etc) per category
        listOfEvaluation = []

        for x in range(arrlength):
            if len(evaluateheight) == 0:
                k = 0
            else:
                k = evaluateheight[x]
            if len(evaluatechest) == 0:
                l = 0
            else:
                l = evaluatechest[x]

            # compile parts evaluation per category
            partsEvaluation = [k, l]

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
    invalid = set()
    # based on the chosen gender, remove the part for the opposite gender
    if gender == 'girl':
        invalid = {"boy", "boys", "big boys", "little boys", "boys fit",
                   "baby", "belts boys", "belts unisex", "unisex"}
    elif gender == 'boy':
        invalid = {"girl", "girls", "big girls", "little girls", "girls fit",
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


def evaluateBottomZara(brandChart, height, inseam, waist, hip, gender):

    # initialization
    evalfinalsize = {}
    evalfinalpercent = {}
    evalfinalfit = {}
    finalsize = []
    finalpercentsize = []

    for loopCategory in brandChart:
        evalsize = {}

        evaluateheight = []  # height
        evaluateinseam = []  # inseam
        evaluatewaist = []  # waist
        evaluatehip = []  # hip

        # loop through rows in table
        for part in loopCategory:

            if 'height (cm)' in part[0]:
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

            if 'leg length (cm)' in part[0]:
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

            if 'waist (cm)' in part[0]:
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

            if 'hips (cm)' in part[0]:
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

            # compile parts evaluation per category
            partsEvaluation = [k, m, n, p]

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
    invalid = set()
    # based on the chosen gender, remove the part for the opposite gender
    if gender == 'girl':
        invalid = {"boy", "boys", "big boys", "little boys", "boys fit",
                   "baby", "belts boys", "belts unisex", "unisex"}
    elif gender == 'boy':
        invalid = {"girl", "girls", "big girls", "little girls", "girls fit",
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


def evaluateGuess(brandChart, weight, height, gender):

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

        # find length of array baseline
        if len(evaluateheight) > 0:
            arrlength = len(evaluateheight)
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

            # compile parts evaluation per category
            partsEvaluation = [k, l]

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
    invalid = set()
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


def evaluatePolo(brandChart, weight, height, waist, gender):

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

            # compile parts evaluation per category
            partsEvaluation = [k, l, m]

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

    invalid = set()

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


def evaluateBottomHM(brandChart, height, inseam, waist, hip, gender):

    # initialization
    evalfinalsize = {}
    evalfinalpercent = {}
    evalfinalfit = {}
    finalsize = []
    finalpercentsize = []

    for loopCategory in brandChart:
        evalsize = {}

        evaluateheight = []  # height
        evaluateinseam = []  # inseam
        evaluatewaist = []  # waist
        evaluatehip = []  # hip

        # loop through rows in table
        for part in loopCategory:

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

            # compile parts evaluation per category
            partsEvaluation = [k, m, n, p]

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
    invalid = set()
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


def evaluateTopHM(brandChart, height, chest, gender):

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

        # find length of array baseline
        if len(evaluateheight) > 0:
            arrlength = len(evaluateheight)
        else:
            arrlength = 0

        # list of evaluation for all parts (weight, height, etc) per category
        listOfEvaluation = []

        for x in range(arrlength):
            if len(evaluateweight) == 0:
                l = 0
            else:
                l = evaluateweight[x]
            if len(evaluatechest) == 0:
                o = 0
            else:
                o = evaluatechest[x]

            # compile parts evaluation per category
            partsEvaluation = [l, o]

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
    invalid = set()
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
