from abc import ABC
from homework_02.exceptions import LowFuelError, NotEnoughFuel
# from exceptions import LowFuelError, NotEnoughFuel


class Vehicle(ABC):

    def __init__(self, weight, fuel, fuel_consumption):
        self.started = False
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if self.started is False:
            if self.fuel == 0:
                raise LowFuelError
            else:
                self.started = True

    def move(self, distance):
        if distance * self.fuel_consumption > self.fuel:  # проверяем, что топлива достаточно
            raise NotEnoughFuel()
        else:
            self.fuel = self.fuel - distance * self.fuel_consumption  # остаток топлива



