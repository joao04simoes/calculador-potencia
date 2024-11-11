import math


def CalculateSlope(dataPoint, nPoints,):
    for i in range(0, nPoints-1):
        if (dataPoint[i+1].altitude - dataPoint[i].altitude) != 0 and dataPoint[i+1].distance - dataPoint[i].distance != 0:
            slope = ((dataPoint[i+1].altitude - dataPoint[i].altitude) /
                     (dataPoint[i+1].distance - dataPoint[i].distance))
            dataPoint[i].slope = math.atan(slope)

        else:
            dataPoint[i].slope = 0


def PotenciaGravidade(dataPoint, nPoints, bikeConstants):
    max = 0
    for i in range(0, nPoints-1):
        force = bikeConstants.weight * \
            bikeConstants.G * math.sin(dataPoint[i].slope)
        dataPoint[i].powerGravity = force * dataPoint[i].speed
        if dataPoint[i].powerGravity > max:
            max = dataPoint[i].powerGravity
    return max


def PowerResistenceAir(dataPoint, nPoints, bikeConstants):
    max = 0
    soma = 0
    for i in range(0, nPoints-1):
        force = 0.5 * bikeConstants.CdA * \
            bikeConstants.density * (dataPoint[i].speed ** 2)
        dataPoint[i].powerAir = force * dataPoint[i].speed
        if dataPoint[i].powerAir > max:
            max = dataPoint[i].powerAir
        soma = soma + dataPoint[i].powerAir
    print(soma)
    soma = soma / (nPoints-1)
    return max


def PowerRollingRestiance(dataPoint, nPoints, bikeConstants):
    for i in range(0, nPoints-1):
        force = bikeConstants.weight * bikeConstants.G * \
            math.cos(dataPoint[i].slope)*bikeConstants.Crr
        dataPoint[i].powerRR = force*dataPoint[i].speed
