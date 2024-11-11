import csv
import math
import matplotlib.pyplot as plt
from wind import wind as wind

G = 9.81
wheight = 90
CdA = 0.32
density = 1.240088
Crr = 0.005


class DataPoint:
    def __init__(self, time, lat, long, heart, cadence, distance, temperature, speed, altitude, slope, powerGravity, powerAir, powerRR):
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


def CalculateSlope():
    for i in range(0, nPoints-1):
        if (dataPoint[i+1].altitude - dataPoint[i].altitude) != 0 and dataPoint[i+1].distance - dataPoint[i].distance != 0:
            slope = ((dataPoint[i+1].altitude - dataPoint[i].altitude) /
                     (dataPoint[i+1].distance - dataPoint[i].distance))
            dataPoint[i].slope = math.atan(slope)

        else:
            dataPoint[i].slope = 0


def PotenciaGravidade():
    max = 0
    for i in range(0, nPoints-1):
        force = wheight * G * math.sin(dataPoint[i].slope)
        dataPoint[i].powerGravity = force * dataPoint[i].speed
        if dataPoint[i].powerGravity > max:
            max = dataPoint[i].powerGravity
    return max


def PowerResistenceAir():
    max = 0
    soma = 0
    for i in range(0, nPoints-1):
        force = 0.5 * CdA * density * (dataPoint[i].speed ** 2)
        dataPoint[i].powerAir = force * dataPoint[i].speed
        if dataPoint[i].powerAir > max:
            max = dataPoint[i].powerAir
        soma = soma + dataPoint[i].powerAir
    print(soma)
    soma = soma / (nPoints-1)
    return max


def PowerRollingRestiance():
    for i in range(0, nPoints-1):
        force = wheight * G * math.cos(dataPoint[i].slope)*Crr
        dataPoint[i].powerRR = force*dataPoint[i].speed


dataPoint = []
with open('/home/joaosimoes/Desktop/calculadora potencia/data_3_11.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Skip the header row
    for row in csv_reader:
        point = DataPoint(time=row[0], lat=row[1], long=row[2], heart=row[3], cadence=row[4],
                          distance=row[4], temperature=row[5], speed=row[6], altitude=row[7], slope=0, powerGravity=0, powerAir=0, powerRR=0)
        dataPoint.append(point)

nPoints = len(dataPoint)  # I=10982
CalculateSlope()
maxGA = PotenciaGravidade()
maxRE = PowerResistenceAir()
PowerRollingRestiance()

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

    if power > 0:
        soma = soma + power
        nPositive = nPositive + 1
        Tempo.append(tem)
        PositivePower.append(power)

media = soma/nPositive

# plt.plot(Tempo, PositivePower, label='Potência',
#         color='blue', marker='o', markersize=2)
# plt.show()
(windSpeed, windDir) = wind(
    "2024-10-01 12:00:00", dataPoint[0].lat, dataPoint[0].long)

print(windSpeed)
print(windDir)
print(media)
