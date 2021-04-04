"""
создайте класс `Car`, наследник `Vehicle`
"""

# from base import Vehicle
from homework_02.base import Vehicle


class Car(Vehicle):

    def __init__(self, weight, fuel, fuel_consumption):
        super().__init__(weight, fuel, fuel_consumption)
        self.engine = None

    def set_engine(self, engine):
        if engine.__class__.__name__ == 'Engine':
            self.engine = engine

