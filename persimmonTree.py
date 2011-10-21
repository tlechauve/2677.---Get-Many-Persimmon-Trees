#!/usr/bin/env python

import os, sys, re
import numpy as np
import argparse

def dataToArray(filename):
    """ Read data from input file and return values as numpy array
    
    warning: numpy reads array column per column and not row per row
    """
    reLine = '(\d+) ?(\d+)?'
    input = []
    f = open(filename, 'r')
    m = re.match(reLine, f.readline())
    while m.groups()[0] != '0':
        # extract trees number
        nbTree = int(m.groups()[0])
        # then the field shape
        fieldShape = [int(x) for x in re.match(reLine, f.readline()).groups()]
        # create a numpy array initialized with zeros with fieldShape
        array = np.zeros((fieldShape[1],fieldShape[0]))
        # put each tree in the array according to coordinates in text file
        for i in xrange(0,nbTree):
            tree = [int(x)-1 for x in re.match(reLine, f.readline()).groups()]
            array[tree[1]][tree[0]] = 1
        # lastly, extract the shape size that the lord gave
        estateShape = [int(x) for x in re.match(reLine, f.readline()).groups()]
        input.append({'array':array,'estateShape':estateShape})
        m = re.match(reLine, f.readline())
    f.close()
    return input

def course(array):
    """ count trees in all rectangular shapes with width and height defined,
    and return maximum number of tree in one.
    """
    estate = array['array']
    shape = array['estateShape']
    maxTree = 0
    for x in xrange(0,estate.shape[1]-shape[0]+1):
        for y in xrange(0,estate.shape[0]-shape[1]+1):
            miniShape = estate[y:y+shape[1],x:x+shape[0]]
            # how many 1 there is in the mini array
            nbTree = len(miniShape[miniShape==1])
            if nbTree > maxTree:
                maxTree = nbTree
    return maxTree
    

if __name__ == '__main__':
    """ For each data set, print one line containing the maximum possible number
    of persimmon trees that can be included in an estate of the given size.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename')
    filename = parser.parse_args().filename
    arrays = dataToArray(filename)
    for array in arrays:
        print course(array)
