#   Print where the pulses are found without including piggybacks
#   print the area under the pulse(use the un-smoothed data)

import sys
import matplotlib.pyplot as plt
import numpy as np
import array
import os
   
def main():
    #get file
    iniFile = sys.argv[1]
    datFile = []
    for root, dirs, files in os.walk("."):
        #print(files)
        for filename in files:
            if((filename[-4 :]) == ".dat"):
                datFile.append(str(filename))
    
    for each in datFile:
        print(each)

    for i in range(0, len(datFile)):
        print(i)
        pr = pulseReader(iniFile, datFile[i])
        print(datFile[i])
        pr.smoothData()
        pr.processPulses()
        pr.findArea()

        plt.plot(pr.data)
        plt.show()

        plt.plot(pr.data2)
        plt.show()
        del(pr)

    # read in the ini file & get pulse parameter

    '''
    pr = pulseReader(iniFile, datFile[0])
    pr.smoothData()
    pr.processPulses()
    pr.findArea()
    plt.plot(pr.data)
    #plt.show()

    plt.plot(pulseReader.data2)
    #plt.show()
    '''

class pulseReader:
    pulseBeg = []
    pulseEnd = []
    data2 = array.array('d')
    data = np.empty
    
    def __init__(self,iniFile, datFile):
        # I get all the pulse parameters from the inifile
        with open (iniFile) as params:
            self.vt = float(params.readline().split("=")[1])
            self.width = float(params.readline().split('=')[1])
            self.pulse_delta = float(params.readline().split('=')[1])
            self.drop_ratio = float(params.readline().split('=')[1])
            self.below_drop_ratio = float(params.readline().split('=')[1])
        # negate all values and save into an array. 
        self.data = (-1 * (np.loadtxt(datFile)))
        self.data = array.array('d', self.data)

    #datFile = sys.argv[2]

    #create an array for the smoothed data
    def smoothData(self):
        #data2 = array.array('d')
        # start with the fourth from the start and "smooth"
        for y in range(4, len(self.data)-4):
            self.data2.append( int ((( (self.data[y-3]) + (2 * self.data[y-2]) + (3 * self.data[y-1]) + (3 * self.data[y]) 
                        + (3 * self.data[y+1]) + (2 * self.data[y+2]) + (self.data[y+3]) ) //15)))

    # Find the pulses, and then weed out the piggy back pulses
    def processPulses(self):
        z = 0
        while (z+2 < len(self.data2) ):
            if ( (self.data2[z+2]) > self.data2[z+1] and self.data2[z+1] > self.data2[z] ):
                if((self.data2[z+2] - self.data2[z]) > self.vt ):
                    self.pulseBeg.append(z+4)
                    while(self.data2[z+1] > self.data2[z]):z += 1
                    self.pulseEnd.append(z+4)
                    if( len(self.pulseBeg) > 1):
                        if( (self.pulseBeg[-1] - self.pulseBeg[-2]) - 2 < self.pulse_delta ):
                            peak = max( self.data[ (self.pulseBeg[-2]) : ( (self.pulseEnd[-1]) ) ] )
                            peakPos = self.data.index(peak)
                            piggyList = self.data[self.pulseBeg[-2] : (self.pulseEnd[-1])+1 ]
                            magic = self.drop_ratio * peak
                            count = 0
                            for i in self.data[peakPos:self.pulseBeg[-1]+1]:
                                if (i < magic):  count += 1
                            if (count >= self.below_drop_ratio):
                                print("Found piggy back at "+ str(self.pulseBeg[-2]))
                                del self.pulseBeg[-2] 
                                del self.pulseEnd[-2]    
                else:
                    z += 1
            else:
                z += 1
    #finding and printing the area from beginning of pulse for width positions away
    def findArea(self):
        for each in range(0,len(self.pulseBeg)):
            if(each <(len(self.pulseBeg))-1):
                if ( (self.pulseBeg[each] + self.width) > (self.pulseBeg[each+1])):pulseEndian = int(self.pulseBeg[each+1])
            else: 
                pulseEndian = int(self.pulseBeg[each]+ self.width)
            print (str(self.pulseBeg[each]) + (" (") + str(sum(self.data[self.pulseBeg[each]:pulseEndian])) + (")"))

if __name__ == "__main__":
    main()
 