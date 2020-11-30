class Vehicle:
    def __init__(self, registration_number, driver_age):
        self.driver_age = driver_age
        self.registration_number = registration_number


class Car(Vehicle):

    def __init__(self, registration_number, driver_age):
        Vehicle.__init__(self, registration_number, driver_age)

    def getType(self):
        return "Car"
