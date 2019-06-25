# Contains the data structure responsible for maintaining
# the state of the solenoids in the system

import prometheus_consts as const


class SolenoidManager:

    def __init__(self):
        # Note that the 0/1 doesn't refer to open/closed
        # it refers to energized or not energized
        self.curr_state = {}

        for name in const.SOL_NAMES:    # Initialize dict
            self.curr_state[name] = 0   # All sols in default state

    # Changes a state of a single solenoid
    # called by state_change and by user on GUI
    def toggle(self, name):
        # self.toggle_from_address(dict[name])
        self.write_to_log()

    # Makes large change to entire system state
    def state_change(self, new_state):
        # Loops thru both dicts (easy because keys are the same)
        for name in const.SOL_NAMES:

            if new_state[name] != self.curr_state[name]:
                # self.toggle_from_address(dict[name])
                pass

        self.write_to_log()

    # Function actually responsible for sending electric signal
    # called by toggle and state change, not user facing
    def toggle_from_address(self, address):
        pass

    # Writes current state to logfile, called every time state changes
    def write_to_log(self):
        pass
