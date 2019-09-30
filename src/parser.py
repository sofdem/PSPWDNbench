#!/usr/bin/env python3
#coding: utf-8
# pylint: disable=C0301
"""
Created on Wed Aug 28 2019
@creation             : 2019-08-28
@author               : Hamza HASSOUNE
@email                : hamza.hassoune@grenoble-inp.org

Parser for the new files that regroup all the data of
the instances.
"""
from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np

##########################################################################
#########################       NODES        #############################
##########################################################################

class Node:
    """
    Node of the network
    """
    def __init__(self, NODE_ID, X_COORDINATE, Y_COORDINATE, Z_COORDINATE):
        self.NODE_ID = NODE_ID
        self.X_COORDINATE = X_COORDINATE
        self.Y_COORDINATE = Y_COORDINATE
        self.Z_COORDINATE = Z_COORDINATE

class Source(Node):
    """
    Source subclass
    """
    def __init__(self, NODE_ID, X_COORDINATE, Y_COORDINATE, Z_COORDINATE,\
                 TIMESERIE_ID, Max_wd, Cost_wd):
        Node.__init__(self, NODE_ID, X_COORDINATE, Y_COORDINATE, Z_COORDINATE)
        self.TIMESERIE_ID = TIMESERIE_ID
        self.Max_wd = Max_wd
        self.Cost_wd = Cost_wd

    def svgdraw(self):
        """
        Method that print the svg line for a source.
        """
        print('<circle cx="{}" cy="{}" r="4" stroke="SeaGreen" stroke-width="0.2"\
              fill="Green" />'.format(self.X_COORDINATE, self.Y_COORDINATE))

    def head(self, instant, profiles_set):
        """
        Method that compute the head at the source.
        """
        return float(self.Z_COORDINATE)*profiles_set[self.TIMESERIE_ID].profile_values[instant+5]

    def plothead(self, profiles_set):
        """
        To plot the Head at source VS Time.
        """
        plt.plot(list(range(len(profiles_set[self.TIMESERIE_ID].profile_values))),\
                 [ratio*self.Z_COORDINATE for ratio in profiles_set[self.TIMESERIE_ID].profile_values], color="blue")
        plt.xlabel("Time (Slice = {}h)".format(profiles_set[self.TIMESERIE_ID].SLICE))
        plt.ylabel("Head at source [m]")
        plt.title("Head VS Time (Source ID : {})".format(self.NODE_ID))
        plt.show()


class Tank(Node):
    """
    Tank subclass
    """
    def __init__(self, NODE_ID, X_COORDINATE, Y_COORDINATE, Z_COORDINATE,\
                 Vol_min, Vol_max, Vol_init, Surface):
        Node.__init__(self, NODE_ID, X_COORDINATE, Y_COORDINATE, Z_COORDINATE)
        self.Vol_min = Vol_min
        self.Vol_max = Vol_max
        self.Vol_init = Vol_init
        self.Surface = Surface

    def svgdraw(self, surfaces):
        """
        Method that print the svg line for a tank.
        """
        print('<circle cx="{}" cy="{}" r="{}" stroke="Navy" stroke-width="{}"\
              fill="Blue" />'.format(self.X_COORDINATE, self.Y_COORDINATE, 10*self.Surface/max(surfaces), 0.2))

class Junction(Node):
    """
    Junction subclass
    """
    def __init__(self, NODE_ID, X_COORDINATE, Y_COORDINATE, Z_COORDINATE,\
                 TIMESERIE_ID, Water_dem_base, Max_P):
        Node.__init__(self, NODE_ID, X_COORDINATE, Y_COORDINATE, Z_COORDINATE)
        self.TIMESERIE_ID = TIMESERIE_ID
        self.Water_dem_base = Water_dem_base
        self.Max_P = Max_P

    def svgdraw(self):
        """
        Method that print the svg line for a junction.
        """
        print('<circle cx="{}" cy="{}" r="2.5" stroke="Grey" stroke-width="0.2"\
              fill="Black" />'.format(self.X_COORDINATE, self.Y_COORDINATE))

    def plotdemand(self, profiles_set):
        """
        To plot the Water demand VS Time for a given junction.
        """
        plt.plot(list(range(len(profiles_set[self.TIMESERIE_ID].profile_values))),\
                 [ratio*self.Water_dem_base for ratio in profiles_set[self.TIMESERIE_ID].profile_values])
        plt.xlabel("Time (Slice = {}h)".format(profiles_set[self.TIMESERIE_ID].SLICE))
        plt.ylabel("Flow rate at junction [m³/h]")
        plt.title("Water demand VS Time (Junction ID : {})".format(self.NODE_ID))
        plt.show()

##########################################################################
##########################       ARCS        #############################
##########################################################################

class Arc:
    """
    Arc of the network
    """
    def __init__(self, ARC_ID, STARTNODE, ENDNODE, MIN_FLOW, MAX_FLOW, MODEL):
        self.ARC_ID = ARC_ID
        self.STARTNODE = STARTNODE
        self.ENDNODE = ENDNODE
        self.MIN_FLOW = MIN_FLOW
        self.MAX_FLOW = MAX_FLOW
        self.MODEL = MODEL

class Pipe(Arc):
    """
    Pipe subclass
    """
    def __init__(self, ARC_ID, STARTNODE, ENDNODE, MIN_FLOW, MAX_FLOW, MODEL,\
                 Loss_deg2, Loss_deg1, Length, Diameter, Roughness):
        Arc.__init__(self, ARC_ID, STARTNODE, ENDNODE, MIN_FLOW, MAX_FLOW, MODEL)
        self.Loss_deg2 = Loss_deg2
        self.Loss_deg1 = Loss_deg1
        self.Length = Length
        self.Diameter = Diameter
        self.Roughness = Roughness

    def svgdraw(self, nodes_set, diameters):
        """
        Method that print the svg line for a pipe.
        """
        print('<line x1="{}" x2="{}" y1="{}" y2="{}" stroke="RoyalBlue" stroke-width="{}"/>'\
              .format(nodes_set[self.STARTNODE].X_COORDINATE, nodes_set[self.ENDNODE].X_COORDINATE,\
               nodes_set[self.STARTNODE].Y_COORDINATE, nodes_set[self.ENDNODE].Y_COORDINATE, \
               3*float(self.Diameter)/float(max(diameters))))

    def plotloss(self):
        """
        To plot Head_losses VS Flow_rate for a given pipe.
        """
        x = np.linspace(self.MIN_FLOW, self.MAX_FLOW, 100)
        y = self.Loss_deg2*x*abs(x) + self.Loss_deg1*x
        plt.plot(x, y, color="green")
        plt.xlabel("Flow rate [m³/h]")
        plt.ylabel("Head losses [m]")
        plt.title("Head losses VS Flow rate (Pipe ID : {})".format(self.ARC_ID))
        plt.show()


class Pump(Arc):
    """
    Pump subclass
    """
    def __init__(self, ARC_ID, STARTNODE, ENDNODE, MIN_FLOW, MAX_FLOW, MODEL,\
                 MIN_GAP, MAX_GAP, TYPE, Inc_deg2, Inc_deg1, Inc_deg0, Pow_deg1,\
                 Pow_deg0, Speed, Min_speed):
        Arc.__init__(self, ARC_ID, STARTNODE, ENDNODE, MIN_FLOW, MAX_FLOW, MODEL)
        self.MIN_GAP = MIN_GAP
        self.MAX_GAP = MAX_GAP
        self.TYPE = TYPE
        self.Inc_deg2 = Inc_deg2
        self.Inc_deg1 = Inc_deg1
        self.Inc_deg0 = Inc_deg0
        self.Pow_deg1 = Pow_deg1
        self.Pow_deg0 = Pow_deg0
        self.Speed = Speed
        self.Min_speed = Min_speed

    def svgdraw(self, nodes_set):
        """
        Method that print the svg line for a pump.
        """
        print('<line x1="{}" x2="{}" y1="{}" y2="{}" stroke="Purple" stroke-width="2"/>'\
              .format(nodes_set[self.STARTNODE].X_COORDINATE, nodes_set[self.ENDNODE].X_COORDINATE,\
               nodes_set[self.STARTNODE].Y_COORDINATE, nodes_set[self.ENDNODE].Y_COORDINATE))

    def plotinc(self):
        """
        To plot Head_Increase VS Flow_rate for a given pump.
        """
        x = np.linspace(self.MIN_FLOW, self.MAX_FLOW, 100)
        y = self.Inc_deg2*x**2 + self.Inc_deg1*x + self.Inc_deg0
        plt.plot(x, y, color="red")
        plt.xlabel("Flow rate [m³/h]")
        plt.ylabel("Head increase [m]")
        plt.title("Head Increase VS Flow rate (Pump ID : {})".format(self.ARC_ID))
        plt.show()

    def plotpow(self):
        """
        To plot Power VS Flow_rate for a given pump.
        """
        x = np.linspace(self.MIN_FLOW, self.MAX_FLOW, 100)
        y = self.Pow_deg1*x + self.Inc_deg0
        plt.plot(x, y, color="purple")
        plt.xlabel("Flow rate [m³/h]")
        plt.ylabel("Power [kW]")
        plt.title("Power VS Flow rate (Pump ID : {})".format(self.ARC_ID))
        plt.show()

class Valve(Arc):
    """
    Valve subclass
    """
    def __init__(self, ARC_ID, STARTNODE, ENDNODE, MIN_FLOW, MAX_FLOW, MODEL,\
                 MIN_GAP, MAX_GAP, TYPE):
        Arc.__init__(self, ARC_ID, STARTNODE, ENDNODE, MIN_FLOW, MAX_FLOW, MODEL)
        self.MIN_GAP = MIN_GAP
        self.MAX_GAP = MAX_GAP
        self.TYPE = TYPE

    def svgdraw(self, nodes_set):
        """
        Method that print the svg line for a valve.
        """
        print('<line x1="{}" x2="{}" y1="{}" y2="{}" stroke="Red" stroke-width="2"/>'\
              .format(nodes_set[self.STARTNODE].X_COORDINATE, nodes_set[self.ENDNODE].X_COORDINATE,\
               nodes_set[self.STARTNODE].Y_COORDINATE, nodes_set[self.ENDNODE].Y_COORDINATE))

##########################################################################
#######################       TIMESERIES        ##########################
##########################################################################

class Timeserie:
    """
    Time series (Profile or Tariff)
    """
    def __init__(self, TIMESERIE_ID, DURATION, START, SLICE):
        self.TIMESERIE_ID = TIMESERIE_ID
        self.DURATION = DURATION
        self.START = START
        self.SLICE = SLICE

class Profile(Timeserie):
    """
    Profile subclass
    """
    def __init__(self, TIMESERIE_ID, DURATION, START, SLICE, profile_values):
        Timeserie.__init__(self, TIMESERIE_ID, DURATION, START, SLICE)
        self.profile_values = profile_values     # list of all flow rate values.

    def plot(self, sources_set, junctions_set):
        """
        To represent profile variations.
        """
        timeseries_sources = [sources_set[source].TIMESERIE_ID for source in sources_set]
        timeseries_junctions = [junctions_set[junction].TIMESERIE_ID for junction in junctions_set]

        if self.TIMESERIE_ID in timeseries_sources:
            plt.plot(list(range(len(self.profile_values))), self.profile_values, color="grey")
        if self.TIMESERIE_ID in timeseries_junctions:
            plt.plot(list(range(len(self.profile_values))), self.profile_values, color="grey")

        plt.xlabel("Time (Slice = {}h)".format(self.SLICE))

        if self.TIMESERIE_ID in timeseries_sources:
            plt.ylabel("Head ratio")
        if self.TIMESERIE_ID in timeseries_junctions:
            plt.ylabel("Water demand ratio")

        if self.TIMESERIE_ID in timeseries_sources:
            plt.title("Head ratio VS Time ({} Pattern)".format(self.TIMESERIE_ID))
        if self.TIMESERIE_ID in timeseries_junctions:
            plt.title("Water demand ratio VS Time ({} Profile)".format(self.TIMESERIE_ID))
        plt.show()

class Tariff(Timeserie):
    """
    Tariff_ELIX subclass
    """
    def __init__(self, TIMESERIE_ID, DURATION, START, SLICE, tariff_values):
        Timeserie.__init__(self, TIMESERIE_ID, DURATION, START, SLICE)
        self.tariff_values = tariff_values      # list of all tariff values.

    def plot(self):
        """
        To represent tariff variations.
        """
        plt.plot(list(range(len(self.tariff_values))), self.tariff_values, color="green")
        plt.xlabel("Time (Slice = {}h)".format(self.SLICE))
        plt.ylabel("Tariff [€/Kwh]")
        plt.title("Electricity tariff VS Time")
        plt.show()

    def average(self):
        """
        Return the average tariff value over the entire duration.
        """
        return sum(self.tariff_values)/len(self.tariff_values)


def create_objects(instance_file):
    """
    Function that create all the objects in the input file.
    """
    instance_out = []
    with open(instance_file, 'r') as myinstance:
        instance_list = list(myinstance)
        # print(file_list)
        for _, rawline in enumerate(instance_list):
            line = rawline.replace("\n", "")
            line_list = line.split(";")
            # print(line_list)
            instance_out.append(line_list)
    # return(instance_out)
    nodes_set = {}
    sources_set = {}
    tanks_set = {}
    junctions_set = {}

    arcs_set = {}
    pipes_set = {}
    pumps_set = {}
    valves_set = {}

    timeseries_set = {}
    profiles_set = {}
    tariffs_set = {}

    for line in instance_out:
        if line[0] == "Source":
            nodes_set[line[1]] = Node(line[1], float(line[2]), float(line[3]), float(line[4]))
            sources_set[line[1]] = Source(line[1], float(line[2]), float(line[3]), float(line[4]),\
                                      line[5], float(line[6]), float(line[7]))
        if line[0] == "Tank":
            nodes_set[line[1]] = Node(line[1], float(line[2]), float(line[3]), float(line[4]))
            tanks_set[line[1]] = Tank(line[1], float(line[2]), float(line[3]), float(line[4]),\
                                  float(line[5]), float(line[6]), float(line[7]), float(line[8]))
        if line[0] == "Junction":
            nodes_set[line[1]] = Node(line[1], float(line[2]), float(line[3]), float(line[4]))
            junctions_set[line[1]] = Junction(line[1], float(line[2]), float(line[3]),\
                                              float(line[4]), line[5], float(line[6]),\
                                              float(line[7]))
        if line[0] == "Pipe":
            arcs_set[line[1]] = Arc(line[1], line[2], line[3], float(line[4]), float(line[5]),\
                                    line[6])
            try:
                pipes_set[line[1]] = Pipe(line[1], line[2], line[3], float(line[4]),\
                                          float(line[5]), line[6], float(line[7]),\
                                          float(line[8]), float(line[9]), float(line[10]),\
                                          float(line[11]))
            except ValueError:
                pipes_set[line[1]] = Pipe(line[1], line[2], line[3], float(line[4]),\
                                          float(line[5]), line[6], float(line[7]),\
                                          float(line[8]), line[9], line[10], line[11])
        if line[0] == "Pump":
            arcs_set[line[1]] = Arc(line[1], line[2], line[3], float(line[4]), float(line[5]),\
                                    line[6])
            try:
                pumps_set[line[1]] = Pump(line[1], line[2], line[3], float(line[4]),\
                                          float(line[5]), line[6], float(line[7]),\
                                          float(line[8]), line[9], float(line[10]),\
                                          float(line[11]), float(line[12]), float(line[13]),\
                                          float(line[14]), float(line[15]), float(line[16]))
            except ValueError:
                pumps_set[line[1]] = Pump(line[1], line[2], line[3], float(line[4]),\
                                          float(line[5]), line[6], float(line[7]),\
                                          float(line[8]), line[9], float(line[10]),\
                                          float(line[11]), float(line[12]), float(line[13]),\
                                          float(line[14]), line[15], line[16])
        if line[0] == "Valve":
            arcs_set[line[1]] = Arc(line[1], line[2], line[3], float(line[4]), float(line[5]),\
                                    line[6])
            valves_set[line[1]] = Valve(line[1], line[2], line[3], float(line[4]), float(line[5]),\
                                    line[6], float(line[7]), float(line[8]), line[9])

        if line[0] == "Profile":
            timeseries_set[line[1]] = Timeserie(line[1], float(line[2]), line[3], float(line[4]))
            profile_values = []
            for _, value in enumerate(line[5:]):
                profile_values.append(float(value))
            profiles_set[line[1]] = Profile(line[1], float(line[2]), line[3], float(line[4]),\
                                        profile_values)

        if line[0] == "Tariff":
            timeseries_set[line[1]] = Timeserie(line[1], float(line[2]), line[3], float(line[4]))
            tariff_values = []
            for _, value in enumerate(line[5:]):
                tariff_values.append(float(value))
            tariffs_set[line[1]] = Tariff(line[1], float(line[2]), line[3], float(line[4]),\
                                      tariff_values)
    # network = {**sources_set, **tanks_set, **junctions_set, **pipes_set, **pumps_set, **valves_set}
    return instance_file, nodes_set, sources_set, tanks_set, junctions_set, arcs_set,\
           pipes_set, pumps_set, valves_set, timeseries_set, profiles_set, tariffs_set


def fill_gams(file_name, nodes_set, sources_set, junctions_set, tanks_set, pipes_set, pumps_set, tariffs_set, output_name):
    """
    To fill the gams file.
    """
    with open(output_name, "w") as outputgams:
        with open(file_name, 'r') as modelefile:
            gams_list = list(modelefile)
            for index, line in enumerate(gams_list):
                if index in range(19):
                    # print(line)
                    outputgams.write(line)
            nline = "     n          nodes         /"
            nlist = [" "+key+"," for key in list(nodes_set.keys())]
            nlist[-1] = nlist[-1].replace(",", "")
            for key in nlist:
                nline += key
            nline += " /"
            outputgams.write(nline)
            outputgams.write("\n")

            jline = "     j(n)       junctions     /"
            jlist = [" "+key+"," for key in list(junctions_set.keys())]
            jlist[-1] = jlist[-1].replace(",", "")
            for key in jlist:
                jline += key
            jline += " /"
            outputgams.write(jline)
            outputgams.write("\n")

            rline = "     r(n)       reservoirs    /"
            rlist = [" " + key + "," for key in list(tanks_set.keys())]
            rlist[-1] = rlist[-1].replace(",", "")
            for key in rlist:
                rline += key
            rline += " /"
            outputgams.write(rline)
            outputgams.write("\n")

            pline = "     l(n,n)     pipes         /"
            plist = [" " + key + "," for key in list(pipes_set.keys())]
            plist[-1] = plist[-1].replace(",", "")
            for key in plist:
                pline += key
            pline += " /"
            outputgams.write(pline)
            outputgams.write("\n")

            tline = "     t          periods       / t1*t"
            tline += str(len(tariffs_set["tariff_ELIX"].tariff_values)-5) + " /"
            outputgams.write(tline)
            outputgams.write("\n")

            outputgams.write(gams_list[24])
            outputgams.write(gams_list[26])

            outputgams.write("     d          pump number   / p1*p" + str(len(pumps_set)) + " /")
            outputgams.write("\n")

    #Function to complete to generate the entire GAMS file, the lines above allow to generate only part of the file.
    pass


def svg_network(nodes_set, sources_set, tanks_set, junctions_set, pipes_set, \
                pumps_set, valves_set, surfaces, diameters, instance_file):
    """
    Function that generate an svg representation of the network.
    """
    width = max([nodes_set[node_ID].X_COORDINATE for node_ID in nodes_set])\
            - min([nodes_set[node_ID].X_COORDINATE for node_ID in nodes_set])
    height = max([nodes_set[node_ID].Y_COORDINATE for node_ID in nodes_set])\
            - min([nodes_set[node_ID].Y_COORDINATE for node_ID in nodes_set])

    print('<svg width="{}" height="{}" fill ="Red">'.format(width+100, height+100))

    print("<rect x=\"0\" y=\"0\" width=\"{}\" height=\"{}\" fill=\"white\"/>".format(width+100, height+100))

    for pipe_ID in pipes_set:
        pipes_set[pipe_ID].svgdraw(nodes_set, diameters)
    for pump_ID in pumps_set:
        pumps_set[pump_ID].svgdraw(nodes_set)
    for valve_ID in valves_set:
        valves_set[valve_ID].svgdraw(nodes_set)
    for source_ID in sources_set:
        sources_set[source_ID].svgdraw()
    for tank_ID in tanks_set:
        tanks_set[tank_ID].svgdraw(surfaces)
    for junction_ID in junctions_set:
        junctions_set[junction_ID].svgdraw()

    print('<rect x=\"{}\" y=\"{}\" rx=\"1\" ry=\"1\" width=\"55\" height=\"73\" \
          style=\"fill:Gainsboro;stroke:black;stroke-width:0.3;opacity:255\" />'.format(width+40, height+22))
    print("<text x=\"{}\" y=\"{}\" fill=\"black\" font-weight =\"bold\" \
          font-style= \"oblique\" font-size= \"7\" >{}</text>".format(width+55, height+30, "Legend"))

    print('<circle cx="{}" cy="{}" r="2.5" stroke="SeaGreen" stroke-width="0.2" \
          fill="Green" />'.format(width+47, height+39))
    print("<text x=\"{}\" y=\"{}\" fill=\"black\" font-style= \"oblique\" \
          font-size= \"6\" >{}</text>".format(width+55, height+42, "Source"))

    print('<circle cx="{}" cy="{}" r="2.5" stroke="Navy" stroke-width="0.2" \
          fill="Blue" />'.format(width+47, height+48))
    print("<text x=\"{}\" y=\"{}\" fill=\"black\" font-style= \"oblique\" \
          font-size= \"6\" >{}</text>".format(width+55, height+50, "Tank"))

    print('<circle cx="{}" cy="{}" r="2.5" stroke="Grey" stroke-width="0.2" \
          fill="Black" />'.format(width+47, height+57))
    print("<text x=\"{}\" y=\"{}\" fill=\"black\" font-style= \"oblique\" \
          font-size= \"6\" >{}</text>".format(width+55, height+59, "Junction"))

    print('<line x1="{}" x2="{}" y1="{}" y2="{}" stroke="RoyalBlue" \
          stroke-width="2"/>'.format(width+45, width+50, height+67, height+67))
    print("<text x=\"{}\" y=\"{}\" fill=\"black\" font-style= \"oblique\" \
          font-size= \"6\" >{}</text>".format(width+55, height+69, "Pipe"))

    print('<line x1="{}" x2="{}" y1="{}" y2="{}" stroke="Purple" \
          stroke-width="2"/>'.format(width+45, width+50, height+76, height+76))
    print("<text x=\"{}\" y=\"{}\" fill=\"black\" font-style= \"oblique\" \
          font-size= \"6\" >{}</text>".format(width+55, height+78, "Pump"))

    print('<line x1="{}" x2="{}" y1="{}" y2="{}" stroke="Red" \
          stroke-width="2"/>'.format(width+45, width+50, height+85, height+85))
    print("<text x=\"{}\" y=\"{}\" fill=\"black\" font-style= \"oblique\" \
          font-size= \"6\" >{}</text>".format(width+55, height+87, "Valve"))

    print('<rect x=\"{}\" y=\"{}\" rx=\"2\" ry=\"2\" width=\"90\" height=\"15\" \
          style=\"fill:Gainsboro;stroke:black;stroke-width:0.5;opacity:255\" />'.format(width/2-20, height+80))
    print("<text x=\"{}\" y=\"{}\" fill=\"black\" font-weight =\"bold\" \
          font-size= \"8\" >{}</text>".format(width/2-5, height+90, instance_file.replace(".txt", "")+" Network"))
    print('</svg>')

    return None


def main():
    """
    Main function to test the parser.
    """
    instance_file, nodes_set, sources_set, tanks_set, junctions_set, arcs_set, pipes_set, \
    pumps_set, valves_set, timeseries_set, profiles_set, tariffs_set = create_objects("Richmond.txt")

    surfaces = [tanks_set[tank_ID].Surface for tank_ID in tanks_set]
    diameters = [pipes_set[pipe_ID].Diameter for pipe_ID in pipes_set]

        # The tests below correspond to Richmond instance:

    # print(isinstance(profiles_set["domestic"], Profile))
    # print(isinstance(tariffs_set["tariff_ELIX"], Tariff))
    # print(type(sources_set["Bache_O"].Max_wd))
    # print(sources_set["Bache_O"].Max_wd)
    # print(isinstance(nodes_set["Bache_O"], Node))
    # print(isinstance(arcs_set["v1"], Arc))
    # print(isinstance(pipes_set["Tub1154"], Pipe))
    #
    # print(sources_set["Bache_O"].head(5, profiles_set))
    # sources_set["Bache_O"].plothead(profiles_set)
    # junctions_set["634"].plotdemand(profiles_set)
    # pipes_set["Tub794"].plotloss()
    # pumps_set["1A"].plotinc()
    # pumps_set["1A"].plotpow()
    # profiles_set["constant"].plot(sources_set, junctions_set)
    # profiles_set["domestic"].plot(sources_set, junctions_set)
    # profiles_set["Source"].plot(sources_set, junctions_set)
    # tariffs_set["tariff_ELIX"].plot()
    # print(tariffs_set["tariff_ELIX"].average())

        # And for Anytown(M) instance:

    # print(pipes_set["T30"].Diameter)

        #Finally "Test_svg.txt" instance was created to test the svgdraw methods:

    # svg_network(nodes_set, sources_set, tanks_set, junctions_set, pipes_set, \
    #             pumps_set, valves_set, surfaces, diameters, instance_file)

        # Lines below for testing "fill_gams" function:

    output_name = instance_file.replace(".txt", ".gms")
    fill_gams("GAMS_file_complet.gms", nodes_set, sources_set, junctions_set, tanks_set, pipes_set, pumps_set, tariffs_set, output_name)

main()
