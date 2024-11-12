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


def PowerResistenceAir(dataPoint, nPoints, bikeConstants, windDir, windSpeed,):
    max = 0
    soma = 0
    wFavor = 0
    for i in range(0, nPoints-1):
        wFavor = windFavor(dataPoint, windDir, windSpeed, i)
        # wFavor = 0
        # print(wFavor)
        force = 0.5 * bikeConstants.CdA * \
            bikeConstants.density * ((dataPoint[i].speed + wFavor) ** 2)
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


def windFavor(dataPoint, windDir, windSpeed, i):
    lat1, lon1, lat2, lon2 = map(math.radians, [
                                 dataPoint[i].lat, dataPoint[i].long, dataPoint[i+1].lat, dataPoint[i+1].long])
    # Difference in longitudes
    delta_lon = lon2 - lon1
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(delta_lon))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    # print("windspeed", windSpeed)
    windSpeed = windSpeed * math.cos(math.radians(compass_bearing - windDir))

    # print("bearing", compass_bearing)
    # print("windDir", windDir)
    # print("diference", compass_bearing - windDir)
    # print("real wind ", windSpeed)
    return windSpeed
