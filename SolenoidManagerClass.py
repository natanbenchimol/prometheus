import prometheus_shared as shared
import prometheus_consts as CONST
# from datetime import time
import time
import RPi.GPIO as GPIO


class SolenoidManager:
    """ Solenoid class:
    controls the state of solenoid valves. Valves come in two states 'Normally Open (NO)' or
    'Normally Closed (NC)' and their state can be changed by applying a voltage across the positive and negative leads.
     Mosfets in the DAQ PCB are used as a push button to apply a voltage across the solenoids valves and energize them.
     """

    def __init__(self):
        """ SolenoidManager initializer
        valve_current_state - dictionary used to log the current state of all valves
        raspberryPi_pin_mapping - gipio pin mapping on RaspberryPi
        """

        self.NON_ENERGIZED_STATE = 0  # corresponds to a no voltage being applied to solenoid valve
        self.ENERGIZED_STATE = 1  # corresponds to voltage being applied to solenoid valve
        self.All_valve_deEnergized = True

        self.valve_current_state = {}  # log of current valve states
        for name in CONST.SOL_NAMES:
            self.valve_current_state[name] = 0  # All solenoids in their default state

        # TODO: All ints need to be replaced with pin numbers"""
        #             "NC3O": int,
        #             "NCOP": int,
        #             "NC3N": int,
        #             "NCIF": int,
        #             "NOIP": int,
        #             "NCIP": int,
        #             "NCIO": int,
        #             "NCFP": int,
        #             "SPRK": int
        #             """
        # each valve name is mapped to a pin on the DAQ/raspberryPi
        self.raspberryPi_pin_mapping = {
            "NC3O": 3,
            "NCOP": 5,
            "NC3N": 7,
            "NCIF": 11,
            "NOIP": 19,
            "NCIP": 15,
            "NCIO": 13,

        }
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        # TODO: GPIO.setmode(....) start all valve pins in a deEnergized state
        # for name in CONST.SOL_NAMES:
        for name in self.raspberryPi_pin_mapping:
            GPIO.setup(self.raspberryPi_pin_mapping[name], GPIO.OUT, initial=GPIO.LOW)

    def __energize_state(self, name):
        """changes the valve state to an Energized state
            name - name of valve
        """

        GPIO.output(self.raspberryPi_pin_mapping[name], GPIO.HIGH)  # This code is taken from swapnils snippet
        self.valve_current_state[name] = self.ENERGIZED_STATE
        self.All_valve_deEnergized = False

    def __non_energized_state(self, name):
        """changes the valve state to an Non-Energized state
           name - name of valve
        """
        GPIO.output(self.raspberryPi_pin_mapping[name], GPIO.LOW)
        self.valve_current_state[name] = self.NON_ENERGIZED_STATE

    def change_valve_state(self, name):
        """ changes the current state of the solenoid valve. States are either open or close
            :param name - name of the valve to change its state
        """
        current_state = self.valve_current_state[name]

        if not self.isEnergized(name):
            # log state change
            shared.log_event("SOL", name + " transitioning from state " + str(current_state) + " to " + str(
                self.ENERGIZED_STATE))
            self.__energize_state(name)

        else:
            # log state change
            shared.log_event("SOL", name + " transitioning from state " + str(current_state) + " to " + str(
                self.NON_ENERGIZED_STATE))
            self.__non_energized_state(name)

    def reverse_all_state(self):
        """ Reverses all current vale states. If a valve is energized then this method changes it to a
        non-energized state. If a valve is non-energized then it state is changed to an energized state."""

        for name in self.raspberryPi_pin_mapping:
            self.change_valve_state(name)

    def __energize_all_valves(self):
        """ Changes all valve states to an energized state"""

        for name in self.raspberryPi_pin_mapping:
            current_state = self.valve_current_state[name]
            shared.log_event("SOL", name + " transitioning from state " + str(current_state) + " to " + str(
                self.ENERGIZED_STATE))
            self.__energize_state(name)

    def __deEnergize_all_valves(self):
        """ Changes all valve states to a Non-Energized state"""
        for name in self.raspberryPi_pin_mapping:
            current_state = self.valve_current_state[name]
            shared.log_event("SOL", name + " transitioning from state " + str(current_state) + " to " + str(
                self.NON_ENERGIZED_STATE))
            self.__non_energized_state(name)

    def change_all_valve_states(self):
        """ changes the valves state to either all energized or all deEnergized"""
        if self.All_valve_deEnergized:
            self.__energize_all_valves()
            self.All_valve_deEnergized = False
        else:
            self.__deEnergize_all_valves()
            self.All_valve_deEnergized = True

    def current_state(self, name):
        """ returns the current state of a valve"""

        current_state = self.valve_current_state[name]
        return current_state

    def __isEnergized(self, name):
        """returns true if valve isEnergized otherwise returns false"""
        return self.current_state(name) == self.ENERGIZED_STATE
