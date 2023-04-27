import pickle
import scipy
import numpy

#takes data from file
with open('data.txt', 'rb') as handle:
    data = pickle.loads(handle.read())

#gets power from each packet
values = []
for i in range(len(data["DI1"])):
    power = (data["V1"][i]) * (data["I1"][i])
    inverse = 1 - (data["DI1"][i])
    temp = power * inverse
    values.append(temp)

#find transitions between data blocks of 0
count = 0
times = []
start = -1
for j in range(len(values)-3):
    if start == -1:
        if values[j+1] != 0 and values[j+2] != 0 and values[j+3] != 0:
            start = j+1
    if values[j+1] == 0 and values[j+2] == 0 and values[j+3] == 0 and start != -1: 
        final = j
        pair = (start, final)
        times.append(pair)
        start = -1
        count += 1
    if count > 50:
        break

#find the energy
energy = []
for m in range(len(times)):
    packet_energy = scipy.integrate.trapezoid(values[times[m][0]:times[m][1]], data["time"][times[m][0]:times[m][1]])
    energy.append(packet_energy)

#find the average of energy
toReturn = numpy.mean(energy)
print("average energy = " + str(toReturn))

#find the capacitance
capacitance = (2*toReturn)/((2.4**2) - (2.1**2))
print("capacitance = " + str(capacitance))
