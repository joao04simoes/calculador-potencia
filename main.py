import csv
import math

G = 9.81
wheight = 90
Cd = 0.6
A = 0.5
density = 1.240088


class DataPoint:
    def __init__(self, time, lat, long, heart, cadence, distance, temperature, speed, altitude, slope, powerGravity, powerAir):
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
    for i in range(0, nPoints-1):
        force = wheight * G * math.sin(dataPoint[i].slope)
        dataPoint[i].powerGravity = force * dataPoint[i].speed


def PowerResistenceAir():
    max = 0
    soma = 0
    for i in range(0, nPoints-1):
        force = 0.5 * Cd * A * density * (dataPoint[i].speed ** 2)
        dataPoint[i].powerAir = force * dataPoint[i].speed
        if dataPoint[i].powerAir > max:
            max = dataPoint[i].powerAir
        soma = soma + dataPoint[i].powerAir
    print(soma)
    soma = soma / (nPoints-1)
    return max


dataPoint = []
with open('/home/joaosimoes/Desktop/calculadora potencia/data copy.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Skip the header row
    for row in csv_reader:
        point = DataPoint(time=row[0], lat=row[1], long=row[2], heart=row[3], cadence=row[4],
                          distance=row[5], temperature=row[6], speed=row[7], altitude=row[8], slope=0, powerGravity=0, powerAir=0)
        dataPoint.append(point)

nPoints = len(dataPoint)  # I=10982
CalculateSlope()
PotenciaGravidade()
max = PowerResistenceAir()

print(max)
