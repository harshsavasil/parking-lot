import argparse
from collections import defaultdict
import logging
import os
import sys

from ParkingLotCommand import *
import Vehicle

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)


class ParkingLot:
    EMPTY_SLOT = -1

    def __init__(self):
        self._capacity = 0
        self.slotId = 0
        self.numOfOccupiedSlots = 0

    def createParkingLot(self, capacity):
        """
        This method creates a parking lot for a specific capacity.
        Args:
            capacity ([Integer]): Capacity defines the maximum numbers of parking spaces

        Returns:
            [Integer]: returns the maximum numbers of parking spaces
        """
        if capacity <= 0:
            logging.error('Number of Parking Spots must be greater than zero')
            return None
        else:
            self.slots = [ParkingLot.EMPTY_SLOT] * capacity
            self._capacity = capacity
            self.ageSlotMap = defaultdict(list)
            return self._capacity

    def _getEmptySlot(self):
        """
        This method returns the id of the first empty parking space.

        Returns:
            [Integer]: Parking Slot Id
        """
        for index in range(len(self.slots)):
            if self.slots[index] == ParkingLot.EMPTY_SLOT:
                return index

    def _isFraudulent(self, registration_number):
        """
        This method can be used to add fraudulent checks on the vehicle's registration number.
        For now, if a vehicle with the same registration number exists in the parking space, then
        we will consider the new vehicle as a fraud.

        Args:
            registration_number ([String]): Registration Number of the vehicle
        """
        vehicle_found = [
            slot for slot in self.slots
            if slot != ParkingLot.EMPTY_SLOT
            and slot.registration_number == registration_number
        ]
        isFraudulent = True if len(vehicle_found) > 0 else False
        if isFraudulent:
            logging.info(
                f'Vehicle with registration number "{registration_number}" already exists in our parking lot. This could be a fraud.'
            )
        return isFraudulent

    def park(self, registration_number, driver_age):
        """
        This method parks the vehicle passed into the first empty parking space found.

        Args:
            registration_number ([String]): Registration Number of the vehicle
            driver_age ([Integer]): Driver's age

        Returns:
            [Intger]: Returns -1 in case of no parking space else the number allocated parking space
        """
        if self.numOfOccupiedSlots < self._capacity and not self._isFraudulent(registration_number):
            slotId = self._getEmptySlot()
            self.slots[slotId] = Vehicle.Car(registration_number, driver_age)
            self.ageSlotMap[driver_age].append(slotId)
            self.slotId = self.slotId + 1
            self.numOfOccupiedSlots = self.numOfOccupiedSlots + 1
            return slotId + 1
        else:
            return -1

    def leave(self, slotId):
        """
        This method takes care of the clearing of a parking space. It could
        be useful in cases of calculation of parking fee as well.

        Args:
            slotId ([Integer]): Parking Space number to be emptied

        Returns:
            [Vehicle]: Returns None if the parking space is already empty else vehicle
        """
        if self.numOfOccupiedSlots > 0 and self.slots[slotId - 1] != -1:
            vehicle = self.slots[slotId - 1]
            self.ageSlotMap[vehicle.driver_age].remove(slotId - 1)
            self.slots[slotId - 1] = -1
            self.numOfOccupiedSlots = self.numOfOccupiedSlots - 1
            return vehicle
        return None

    def getSlotFromRegistrationNumber(self, registration_number):
        """
        this method returns the slot number if the vehicle with the registration number exists
        in the parking lot else -1.

        Args:
            registration_number ([String]): Registration Number of the vehicle

        Returns:
            [Integer]: Slot Id if Vehicle is found else -1
        """

        for index in range(len(self.slots)):
            slot = self.slots[index]
            if slot.registration_number == registration_number:
                return index + 1
        return -1

    def getSlotsFromDriversAge(self, driver_age):
        """
        This method returns the slot numbers with the driver's age same as driver_age.

        Args:
            driver_age ([Integer]): Driver's age

        Returns:
            [Integer]: Number of slots
        """
        return [str(slot + 1) for slot in self.ageSlotMap[driver_age]]

    def runParkingLot(self, commandLine):
        """
        This method is respnsible for running the parking lot. It
        identifies the commands and acts accordingly like an event listener.
        Args:
            commandLine ([String]): Parknng Lot Command
        """
        command = commandLine.split(' ')[0]
        if command not in PARKING_LOT_COMMANDS:
            logging.error('[ParkingLot] Unknown Command Error')

        elif PARKING_LOT_COMMANDS[command] == ParkingLotCommand.CREATE_PARKING_LOT:
            numOfSlots = int(commandLine.split(' ')[1])
            capacity = self.createParkingLot(numOfSlots)
            if capacity:
                logging.info('Created parking of ' + str(capacity) + ' slots')
            else:
                logging.info('Unable to create a parking lot')
                sys.exit(-1)

        elif PARKING_LOT_COMMANDS[command] == ParkingLotCommand.PARK:
            registration_number = commandLine.split(' ')[1]
            driver_age = int(commandLine.split(' ')[3])
            allocated_parking_spot = self.park(registration_number, driver_age)
            if allocated_parking_spot == ParkingLot.EMPTY_SLOT:
                logging.info("Parking lot is full!")
            else:
                logging.info('Car with vehicle registration number "{0}" has been parked at slot number {1}'.format(
                    registration_number, allocated_parking_spot
                ))

        elif PARKING_LOT_COMMANDS[command] == ParkingLotCommand.LEAVE:
            vacated_slot_id = int(commandLine.split(' ')[1])
            vehicle = self.leave(vacated_slot_id)
            if vehicle:
                logging.info('Slot number {0} vacated, the car with vehicle registration number "${1}" has left the space, the driver of the car was of age {2}'.format(
                    vacated_slot_id, vehicle.registration_number, vehicle.driver_age))

        elif PARKING_LOT_COMMANDS[command] == ParkingLotCommand.SLOT_NUMBERS_FOR_DRIVER_OF_AGE:
            driver_age = int(commandLine.split(' ')[1])
            slotIds = self.getSlotsFromDriversAge(driver_age)
            logging.info(', '.join(slotIds))

        elif PARKING_LOT_COMMANDS[command] == ParkingLotCommand.SLOT_NUMBER_FOR_CAR_WITH_NUMBER:
            registration_number = commandLine.split(' ')[1]
            slotId = self.getSlotFromRegistrationNumber(registration_number)
            logging.info(slotId)

        elif PARKING_LOT_COMMANDS[command] == ParkingLotCommand.VEHICLE_REGISTRATION_NUMBER_FOR_DRIVE_OF_AGE:
            driver_age = int(commandLine.split(' ')[1])
            slotIds = [
                int(index) - 1 for index in self.getSlotsFromDriversAge(driver_age)]
            slots = [self.slots[index]
                     for index in range(len(self.slots)) if index in slotIds]
            vehicle_numbers = [vehicle.registration_number for vehicle in slots]
            logging.info(', '.join(vehicle_numbers))
        else:
            exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', required=True,
                        dest='input_file', help="Input File")
    args = parser.parse_args()

    if args.input_file:
        parkinglot = ParkingLot()
        logging.debug('[ParkingLot] Reading Input File.')
        with open(args.input_file) as f:
            # TODO: add validations in file to ensure the correctness of the commands
            for line in f:
                line = line.rstrip('\n')
                parkinglot.runParkingLot(line)
    else:
        logging.error('[ParkingLot] Please pass an input file.')


if __name__ == '__main__':
    main()
