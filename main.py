import csv
import math
import matplotlib.pyplot as plt
from wind import wind
from forces import CalculateSlope, PotenciaGravidade, PowerResistenceAir, PowerRollingRestiance
import pandas as pd


class BikeConstants:
    def __init__(self, G=9.81, weight=90, CdA=0.32, density=1.240088, Crr=0.005):
        self.G = G
        self.weight = weight
        self.CdA = CdA
        self.density = density
        self.Crr = Crr


class DataPoint:
    def __init__(self, time, lat, long, heart, cadence, distance, temperature, speed, altitude, slope=0, powerGravity=0, powerAir=0, powerRR=0):
        self.time = time
        self.lat = float(lat)
        self.long = float(long)
        self.heart = heart
        self.cadence = cadence
        self.distance = float(distance)
        self.temperature = int(temperature)
        self.speed = float(speed)
        self.altitude = float(altitude)
        self.slope = float(slope)  # radianos
        self.powerGravity = float(powerGravity)
        self.powerAir = float(powerAir)
        self.powerRR = float(powerRR)

    def __repr__(self):

        return (f"DataPoint(time={self.time}, lat={self.lat}, long={self.long}, "
                f"heart={self.heart}, cadence={self.cadence}, distance={self.distance}, "
                f"temperature={self.temperature}, speed={self.speed}, altitude={self.altitude})")


bikeConstants = BikeConstants()
dataPoint = []
with open('/home/joaosimoes/Desktop/calculadora potencia/data copy.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Skip the header row
    for row in csv_reader:
        point = DataPoint(time=row[0], lat=row[1], long=row[2], heart=row[3], cadence=row[4],
                          distance=row[5], temperature=row[6], speed=row[7], altitude=row[8])
        dataPoint.append(point)

nPoints = len(dataPoint)  # I=10982
CalculateSlope(dataPoint, nPoints)
maxGA = PotenciaGravidade(dataPoint, nPoints, bikeConstants)
maxRE = PowerResistenceAir(dataPoint, nPoints, bikeConstants)
PowerRollingRestiance(dataPoint, nPoints, bikeConstants)

Power = []
PositivePower = []
Tempo = []
soma = 0
nPositive = 0
for i in range(0, nPoints-1):
    tem = i
    power = (dataPoint[i].powerGravity +
             dataPoint[i].powerAir + dataPoint[i].powerRR) * 1.05
    Power.append(power)

    if power > 0 and dataPoint[i].cadence.isdigit() and dataPoint[i].cadence != "0":
        soma = soma + power
        nPositive = nPositive + 1
        Tempo.append(tem)
        PositivePower.append(power)

media = soma/nPositive

plt.plot(Tempo, PositivePower, label='Potência',
         color='blue', marker='o', markersize=2)
plt.show()


timestamp = pd.Timestamp(dataPoint[0].time)
rounded_timestamp = timestamp.floor("H")
(windSpeed, windDir) = wind(
    rounded_timestamp, dataPoint[0].lat, dataPoint[0].long)


print(media)
