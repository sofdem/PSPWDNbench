#!/usr/bin/env python3
#coding: utf-8
"""
Created on Wed Aug 28 2019
@creation             : 2019-08-28
@author               : Hamza HASSOUNE
@email                : hamza.hassoune@grenoble-inp.org

Parser for the new file that regroup all the data of
the instances..
"""
from __future__ import print_function

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

    def head(self, instant, profiles_set):
        """
        Method that compute the head at the source.
        """
        return float(self.Z_COORDINATE)*profiles_set[self.TIMESERIE_ID][instant+5]

    def svgdraw(self):
        """
        Method that print the svg line for a source.
        """
        print('<circle cx="{}" cy="{}" r="20" stroke="black" stroke-width="2"\
              fill="blue" />'.format(self.X_COORDINATE, self.Y_COORDINATE))


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
        print('<circle cx="{}" cy="{}" r="{}" stroke="grey" stroke-width="{}"\
              fill="blue" />'.format(self.Surface*60/max(surfaces), self.X_COORDINATE,\
                                     self.Y_COORDINATE, 20*self.Vol_init/self.Vol_max))

class Junction(Node):
    """
    Junction subclass
    """
    def __init__(self,NODE_ID, X_COORDINATE, Y_COORDINATE, Z_COORDINATE,\
                 TIMESERIE_ID, Water_dem_base, Max_P):
        Node.__init__(self, NODE_ID, X_COORDINATE, Y_COORDINATE, Z_COORDINATE)
        self.TIMESERIE_ID = TIMESERIE_ID
        self.Water_dem_base = Water_dem_base
        self.Max_P = Max_P

    def svgdraw(self):
        """
        Method that print the svg line for a junction.
        """
        print('<circle cx="{}" cy="{}" r="20" stroke="black" stroke-width="2"\
              fill="grey" />'.format(self.X_COORDINATE, self.Y_COORDINATE))

    # def gamsline(self, NODE_ID):
    #     print("     j(n)       junctions     / j1, j2 /")

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

class Tariff(Timeserie):
    """
    Tariff_ELIX subclass
    """
    def __init__(self, TIMESERIE_ID, DURATION, START, SLICE, tariff_values):
        Timeserie.__init__(self, TIMESERIE_ID, DURATION, START, SLICE)
        self.tariff_values = tariff_values      # list of all tariff values.


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
    # print(tariff_values)
    # print(len(tariff_values))
    # print(isinstance(profiles["domestic"], Profile))
    # print(isinstance(tariffs["tariff_ELIX"], Tariff))
    # print(type(sources["Bache_O"].Max_wd))
    # print(sources["Bache_O"].Max_wd)
    # print(sources["Bache_O"].Max_wd > 10**15)
    # print(isinstance(nodes["Bache_O"], Node))
    # print(isinstance(arcs["v1"], Arc))
    # print(type(pipes_set["T30"].Diameter))
    # print(pipes_set["T30"].Diameter)
    # print(isinstance(pipes_set["T30"], Pipe))

    # return nodes, arcs, timeseries


def main():
    """
    Main function to test the parser.
    """
    create_objects("Vanzyl")
main()
