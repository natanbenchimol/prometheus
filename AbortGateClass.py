
class AbortGate:
    # Basic 1 to 1 constructor
    # def __init__(self, name, t1, t2, gate_max, gate_min, std_max, std_min):
    #     self.name = name            # Instrument name
    #     self.t1 = t1                # Time that gate opens (relative to countdown start)
    #     self.t2 = t2                # Time that gate closes (relative to countdown start)
    #     self.gate_max = gate_max    # Max value while within gate time range
    #     self.gate_min = gate_min    # Min value while within gate time range
    #     self.std_max = std_max      # Max value while outside gate time range
    #     self.std_min = std_min      # Min value while outside gate time range

    # Constructor that takes a line from the config file
    def __init__(self, line):
        self.name = line[0]
        self.t1 = line[1]
        self.t2 = line[2]
        self.gate_max = line[3]
        self.gate_min = line[4]
        self.std_max = line[5]
        self.std_min = line[6]

    # Pretty print method
    def __str__(self):
        return self.name + " Abort Gate:\n" \
            + "\tTimeRange = " + str(self.t1) + " - " + str(self.t2) + "\n"\
            + "\tGateRange = " + str(self.gate_min) + " - " + str(self.gate_max) + "\n" \
            + "\tStdRange = " + str(self.std_min) + " - " + str(self.std_max)

    # Passes in the recorded value and the timestamp
    # Returns True when we need to abort, False if value is within parameters
    def should_abort(self, val, time):
        if self.t1 <= time <= self.t2:
            if self.gate_min <= val <= self.gate_max:   # We are within gate time, check gate vals
                return False
        else:
            if self.std_min <= val <= self.std_max:      # Outside gate time, check std vals
                return False

        return True                         # Executed if either of our conditionals aren't valid ABORT!!!!

    # Checks that we have a valid abort gate for just before the countdown is initiated
    def is_valid_gate(self):
        # All attributes must have a value
        for attr, value in self.__dict__.items():
            if value is None:
                print("Gate: " + self.name + " has no value for attribute: " + attr)
                return False

        # Times and max/mins are in the correct order
        if self.t1 > self.t2:
            print("Gate: " + self.name + " has inverted time attributes")
            return False
        if self.std_max < self.std_min:
            print("Gate: " + self.name + " has inverted std_max/std_min attributes")
            return False
        if self.gate_max < self.gate_min:
            print("Gate: " + self.name + " has inverted gate_max/gate_min attributes")
            return False

        # All good, proceed with fire
        return True
