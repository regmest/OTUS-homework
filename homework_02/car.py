"""
создайте класс `Car`, наследник `Vehicle`
"""

# from base import Vehicle
# from engine import Engine
from homework_02.base import Vehicle
from homework_02.engine import Engine


class Car(Vehicle):

    def __init__(self, weight, fuel, fuel_consumption):
        super().__init__(weight, fuel, fuel_consumption)
        self.engine = None

    def set_engine(self, engine):
        if isinstance(engine, Engine):
            self.engine = engine


