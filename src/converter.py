#!/usr/bin/env python3
#coding: utf-8
"""
Created on Fri Aug 16 2019
@creation             : 2019-08-16
@author               : Hamza HASSOUNE
@email                : hamza.hassoune@grenoble-inp.org

Module that regroup all tools and functions used to
modify and merge different csv files in one instance.
"""

from __future__ import print_function
import csv
import glob
import os

def withoutspaces(file_name):
    """
    Remove all the spaces in the file.
    Return another csv file without spaces.
    """
    fichier = open(file_name, 'r')
    holeyfile = csv.reader(fichier, delimiter=";")
    filews = "ws_"+file_name
    outfile = open(filews, 'w')
    outwriter = csv.writer(outfile, delimiter=";")
    wslist = []
    for line in holeyfile:
        for index, _ in enumerate(line):
            line[index] = line[index].replace(" ", "")
        # print(line)
        wslist.append(line)
    outwriter.writerows(wslist)  #save after modification
    outfile.close()
    fichier.close()
    return filews    #used in the functions below

def convert_to_float(file_name):
    """
    To convert all the data to float format if necessary
    """
    fichier = open(file_name, 'r')
    rawfile = csv.reader(fichier, delimiter=";")
    floatfile = "fl_"+file_name
    outfile = open(floatfile, 'w')
    outwriter = csv.writer(outfile, delimiter=";")
    fllist = []
    fllist.append(next(rawfile)) #we copy and skip the header.

    if file_name in ["ws_Source.csv", "ws_Junction.csv"]:
        for line in rawfile:
            for index in [2, 3, 4, 6, 7]:
                try:
                    line[index] = str(float(line[index]))
                except:
                    continue
            fllist.append(line)

    if file_name == "ws_Tank.csv":
        for line in rawfile:
            for index in [2, 3, 4, 5, 6, 7, 8]:
                try:
                    line[index] = str(float(line[index]))
                except:
                    continue
            fllist.append(line)

    if file_name in ["ws_Pipe.csv", "ws_Pump.csv", "ws_Valve.csv"]:
        for line in rawfile:
            for index in [4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16]:
                try:
                    line[index] = str(float(line[index]))
                except:
                    continue
            fllist.append(line)

    if file_name in ["ws_Profile.csv", "ws_Tariff_ELIX.csv"]:
        for line in rawfile:
            for index, _ in enumerate(line):
                if index not in [0, 1, 3]:
                    try:
                        line[index] = str(float(line[index]))
                    except:
                        continue
            fllist.append(line)

    outwriter.writerows(fllist)  #save after modification
    outfile.close()
    fichier.close()
    return floatfile  #used in other functions.

def new_lines_list(file_name, columns, new_data_list):
    """
    columns = a list of indexes corresponding to the columns to modify
    Return a list with the new csv lines after conversion.
    """
    outlist = []
    filecsv = open(file_name)
    rawfile = csv.reader(filecsv, delimiter=";")
    for index, old_line in enumerate(rawfile):
        for i, j in enumerate(columns):
            old_line[j] = new_data_list[i][index]
        # print(old_line)
        outlist.append(old_line)
    return outlist

def fill_csv(file_name, mylist):
    """
    To create and fill our new csv file with the new lines.
    """
    newfile = "modified_"+file_name
    outfile = open(newfile, 'w')
    outwriter = csv.writer(outfile, delimiter=";")
    outwriter.writerows(mylist)  #save after modification
    outfile.close()

def mod_source(file_name, averages=None):
    """
    Modification of files : Valve.csv
    """
    # we remove the spaces from the file if there are any
    file_name = withoutspaces(file_name)   #ws_file_name
    # we typecast the data to float form
    file_name = convert_to_float(file_name)
    outlist = []
    filecsv = open(file_name)
    rawfile = csv.reader(filecsv, delimiter=";")
    for _, old_line in enumerate(rawfile):
        if averages and old_line[5] in list(averages.keys()):
            old_line[4] = str(averages[old_line[5]])
            # print(old_line)
            outlist.append(old_line)
        else:
            outlist.append(old_line)

    newfile = "modified_"+file_name
    outfile = open(newfile, 'w')
    outwriter = csv.writer(outfile, delimiter=";")
    outwriter.writerows(outlist)  #save after modification
    outfile.close()

def mod_tank(file_name):
    """
    Modification of files : Tank.csv
    """
    # we remove the spaces from the file if there are any
    file_name = withoutspaces(file_name)   #ws_file_name
    # we typecast the data to float form
    file_name = convert_to_float(file_name)

def convert_junction_data(file_name, averages=None):
    """
    To get and convert 'water_dem_base' from L/s to m³/h.
    Return two lists, the old data list and the new data one.
    """
    new_data_lists = [[]]
    filecsv = open(file_name, 'r')
    myfile = csv.reader(filecsv, delimiter=";")
    new_data_lists[0].append(next(myfile)[6])  #we copy the title of the column
    for line in myfile:
        water_dem_base = line[6]
        if line[5] in list(averages.keys()):
            new_data = round(averages[line[5]]*3.6, 6)
            new_data_lists[0].append(str(new_data))   #converted values list
        else:
            new_data = round(float(water_dem_base)*3.6, 6)
            new_data_lists[0].append(str(new_data))   #converted values list
    # print(new_data_lists)
    return new_data_lists

def mod_junction(file_name, averages=None):
    """
    Modification of files : Junction.csv
    """
    # we remove the spaces from the file if there are any
    file_name = withoutspaces(file_name)   #ws_file_name
    # we typecast the data to float form
    file_name = convert_to_float(file_name)
    # we convert the data
    new_data_list = convert_junction_data(file_name, averages)
    # we create a new lines list with these new data
    mylist = new_lines_list(file_name, [6], new_data_list)
    # finally we generate a new csv file containing the converted data
    fill_csv(file_name, mylist)

def convert_pipe_data(file_name):
    """
    To get and convert: 'MIN_FLOW','MAX_FLOW' from [L/s] to [m³/h]
                        'Loss_deg2' from [m.s²/L²] to [h².m⁻⁵]
                        'Loss_deg1' from [m.s/L]   to [h.m⁻²]
    Return the new data lists.
    """
    new_data_lists = [[], [], [], []]
    # [minflow_list, maxflow_list, lossdeg2_list, lossdeg1_list]
    filecsv = open(file_name, 'r')
    myfile = csv.reader(filecsv, delimiter=";")
    # we define a list with some constants used below
    coeff = [3.6, 3.6, 1/12.96, 1/3.6]    # (1/3.6)² = 1/12.96
    for line in myfile:
        for index, column in enumerate([4, 5, 7, 8]):
            try:
                new_data_lists[index].append(str(round(float(line[column])*coeff[index], 9)))
            except:
                # we copy the title of the columns
                new_data_lists[index].append(line[column])
    # print(new_data_list)
    return new_data_lists

def mod_pipe(file_name):
    """
    Modification of files : Pipe.csv
    """
    # we remove the spaces from the file if there are any
    file_name = withoutspaces(file_name)   #ws_file_name
    # we typecast the data to float form
    file_name = convert_to_float(file_name)
    # we convert the data
    new_data_lists = convert_pipe_data(file_name)
    # we create a new lines list with these new data
    mylist = new_lines_list(file_name, [4, 5, 7, 8], new_data_lists)
    # finally we generate a new csv file containing the converted data
    fill_csv(file_name, mylist)

def convert_pump_data(file_name):
    """
    To get and convert: 'MIN_FLOW','MAX_FLOW' from [L/s] to [m³/h]
                        'Inc_deg2' from [m.s²/L²] to [h².m⁻⁵]
                        'Inc_deg1' from [m.s/L]   to [h.m⁻²]
                        'Pow_deg1' from [kW.s/L]   to [kWh/m³]
    Return the new data lists.
    """
    new_data_lists = [[], [], [], [], []]
    # [minflow_list, maxflow_list, incdeg2_list, incdeg1_list, powdeg1_list]
    filecsv = open(file_name, 'r')
    myfile = csv.reader(filecsv, delimiter=";")
    # we define a list with some constants used below
    coeff = [3.6, 3.6, 1/12.96, 1/3.6, 1/3.6]    # (1/3.6)² = 1/12.96
    for line in myfile:
        for index, column in enumerate([4, 5, 10, 11, 13]):
            try:
                new_data_lists[index].append(str(round(float(line[column])*coeff[index], 9)))
            except:
                # we copy the title of the columns
                new_data_lists[index].append(line[column])
    # print(new_data_list)
    return new_data_lists

def mod_pump(file_name):
    """
    Modification of files : Pump.csv
    """
    # we remove the spaces from the file if there are any
    file_name = withoutspaces(file_name)   #ws_file_name
    # we typecast the data to float form
    file_name = convert_to_float(file_name)
    # we convert the data
    new_data_lists = convert_pump_data(file_name)
    # we create a new lines list with these new data
    my_csv_list = new_lines_list(file_name, [4, 5, 10, 11, 13], new_data_lists)
    # finally we generate a new csv file containing the converted data
    fill_csv(file_name, my_csv_list)

def convert_valve_data(file_name):
    """
    To get and convert: 'MIN_FLOW','MAX_FLOW' from [L/s] to [m³/h]
    Return the new data lists.
    """
    new_data_lists = [[], []]
    # [minflow_list, maxflow_list]
    filecsv = open(file_name, 'r')
    myfile = csv.reader(filecsv, delimiter=";")
    for line in myfile:
        for index, column in enumerate([4, 5]):
            try:
                new_data_lists[index].append(str(round(float(line[column])*3.6, 9)))
            except:
                # we copy the title of the columns
                new_data_lists[index].append(line[column])
    # print(new_data_list)
    return new_data_lists

def mod_valve(file_name):
    """
    Modification of files : Valve.csv
    """
    # we remove the spaces from the file if there are any
    file_name = withoutspaces(file_name)   #ws_file_name
    # we typecast the data to float form
    file_name = convert_to_float(file_name)
    # we convert the data
    new_data_lists = convert_valve_data(file_name)
    # we create a new lines list with these new data
    mylist = new_lines_list(file_name, [4, 5], new_data_lists)
    # finally we generate a new csv file containing the converted data
    fill_csv(file_name, mylist)

def convert_profile_data(file_name, convert):
    """
    Modification of files: Profile.csv
    convert = list containing indexes of lines to convert (first line index = 0)
    """
    fichier = open(file_name, 'r')
    profile = list(csv.reader(fichier, delimiter=";"))
    head = profile[0]
    for index, _ in enumerate(head):
        if index > 4:
            head[index] = "Value_{}".format(index-4)
    outlist = [[] for _, _ in enumerate(profile)]
    outlist[0] = head
    averages = {}
    if convert:
        convert = sorted(convert)
        for _, conv in enumerate(convert):
            linetoconvert = profile[conv]   # line which elements are not ratio
            for index, element in enumerate(linetoconvert[5:]):
                linetoconvert[index+5] = float(element)
            average = round(sum(linetoconvert[5:])/len(linetoconvert[5:]), 2)
            averages[linetoconvert[1]] = average
            # print(" Line: {},TIMESERIE_ID: {}, average value: {}"\
            #      .format(conv, linetoconvert[1], average))
            for index, element in enumerate(linetoconvert[5:]):
                linetoconvert[index+5] = str(round(element/average, 6))
            outlist[conv] = linetoconvert
        for i, _ in enumerate(profile):
            if i not in convert and i != 0:
                outlist[i] = profile[i]
    else:
        for index, line in enumerate(profile[1:]): #we skip the header
            i = index+1
            outlist[i] = line
    return outlist, averages

def mod_profile(file_name, convert=None):
    """
    Modification of files : Pump.csv
    """
    # we remove the spaces from the file if there are any
    file_name = withoutspaces(file_name)   # ws_file_name
    # we typecast the data to float form
    file_name = convert_to_float(file_name)
    # we convert the data and create a new lines list
    my_csv_list = convert_profile_data(file_name, convert)[0]
    # finally we generate a new csv file containing the converted data
    fill_csv(file_name, my_csv_list)

def mod_tariff(file_name):
    """
    Modification of files : Tariff_Elix.csv
    To name all columns of the csv file, whose number can be large,
    and convert the values from [€/MWh] to [€/kWh].
    """
    # we remove the spaces from the file if there are any
    file_name = withoutspaces(file_name)
    # we convert to float
    file_name = convert_to_float(file_name)
    # then we modify the file without spaces
    fichier = open(file_name, 'r')
    tariff_elix = csv.reader(fichier, delimiter=";")
    modifiedfile = "modified_"+file_name
    outfile = open(modifiedfile, 'w')
    outwriter = csv.writer(outfile, delimiter=";")
    outlist = []
    head = next(tariff_elix)
    for index, _ in enumerate(head):
        if index > 4:
            head[index] = "Value_{}".format(index-4)
    # print(head)
    outlist.append(head)
    line2 = next(tariff_elix)
    for index, tariff in enumerate(line2):
        if index > 4:
            line2[index] = str(round(float(tariff)/1000, 5))
    # print(line2)
    outlist.append(line2)
    outwriter.writerows(outlist)   #save after modification.
    outfile.close()
    fichier.close()

def merge(file_names, instance_name):
    """
    Function that takes as input list of name files
    and an instance name.
    Return all the csv files merged in text file named instance_name.
    """
    with open(instance_name, "w") as myfile:
        for _, name in enumerate(file_names):
            with open(name, 'r') as file_csv:
                file_list = list(file_csv)
                # print(file_list)
                for _, line in enumerate(file_list):
                    # print(line)
                    myfile.write(line)
                myfile.write("\n")

def remove(file_names):
    """
    Used to remove all intermediate files generated.
    """
    for interfile in file_names:
        os.remove(interfile)


def main():
    """
    Main function to run the program.
    """
    #Richmond test:

    mod_tank("Tank.csv")
    mod_pipe("Pipe.csv")
    mod_pump("Pump.csv")
    mod_valve("Valve.csv")

    # convert = [3] pour Richmond.
    # convert = [2, 3, 4] pour Shi-Small.
    convert = [3]
    mod_profile("Profile.csv", convert)

    averages = convert_profile_data("Profile.csv", convert)[1]
    print(averages)
    mod_source("Source.csv", averages)
    mod_junction("Junction.csv", averages)
    mod_tariff("Tariff_ELIX.csv")

    file_names = ["modified_fl_ws_Source.csv", "fl_ws_Tank.csv",\
                  "modified_fl_ws_Junction.csv", "modified_fl_ws_Pipe.csv",\
                  "modified_fl_ws_Pump.csv", "modified_fl_ws_Valve.csv",\
                  "modified_fl_ws_Profile.csv", "modified_fl_ws_Tariff_ELIX.csv"]

    merge(file_names, "Richmond.txt")

    # we remove all the csv files in the directory except the result file.
    # for interfile in glob.glob("*.csv"):
    #     os.remove(interfile)

    # Or we keep also the input csv files by uncommenting the lines below.
    file_names.extend(["fl_ws_Junction.csv", "fl_ws_Pump.csv", "fl_ws_Pipe.csv",\
                      "fl_ws_Valve.csv", "fl_ws_Profile.csv", "fl_ws_Tariff_ELIX.csv",\
                      "ws_Tank.csv", "ws_Junction.csv", "ws_Pump.csv", "ws_Valve.csv",\
                      "ws_Profile.csv", "ws_Tariff_ELIX.csv", "fl_ws_Source.csv",\
                      "ws_Source.csv", "ws_Pipe.csv"])
    remove(file_names)

main()
