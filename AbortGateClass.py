
class AbortGate:
    # Basic 1 to 1 constructor
    def __init__(self, name, t1, t2, gate_max, gate_min, std_max, std_min):
        self.name = name            # Instrument name
        self.t1 = t1                # Time that gate opens (relative to countdown start)
        self.t2 = t2                # Time that gate closes (relative to countdown start)
        self.gate_max = gate_max    # Max value while within gate time range
        self.gate_min = gate_min    # Min value while within gate time range
        self.std_max = std_max      # Max value while outside gate time range
        self.std_min = std_min      # Min value while outside gate time range

    def __init__(self, line):
        pass    # Alternate constructor ... might not really be a thing in python

    # Passes in the recorded value and the timestamp
    # Returns True when we need to abort, False if value is within parameters
    def should_abort(self, val, time):
        if(time > self.t1 and time < self.t2):
            if (val > self.gate_min and val < self.gate_max):   # We are within gate time, check gate vals
                return False
        else:
            if(val > self.std_min and val < self.std_max):      # Outside gate time, check std vals
                return False

        return True                         # Executed if either of our conditionals aren't valid ABORT!!!!
