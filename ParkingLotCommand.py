from enum import Enum


class ParkingLotCommand(Enum):
    CREATE_PARKING_LOT = 1
    EXIT = 2
    LEAVE = 3
    PARK = 4
    SLOT_NUMBER_FOR_CAR_WITH_NUMBER = 5
    SLOT_NUMBERS_FOR_DRIVER_OF_AGE = 6
    VEHICLE_REGISTRATION_NUMBER_FOR_DRIVE_OF_AGE = 7


PARKING_LOT_COMMANDS = {
    'create_parking_lot': ParkingLotCommand.CREATE_PARKING_LOT,
    'exit': ParkingLotCommand.EXIT,
    'leave': ParkingLotCommand.LEAVE,
    'park': ParkingLotCommand.PARK,
    'slot_numbers_for_driver_of_age': ParkingLotCommand.SLOT_NUMBERS_FOR_DRIVER_OF_AGE,
    'slot_number_for_car_with_number': ParkingLotCommand.SLOT_NUMBER_FOR_CAR_WITH_NUMBER,
    'vehicle_registration_number_for_drive_of_age': ParkingLotCommand.VEHICLE_REGISTRATION_NUMBER_FOR_DRIVE_OF_AGE,
}
