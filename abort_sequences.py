# This file contains all of the custom exceptions that
# execute the abort sequences when called

recovery_state = {
    "NC_IP": 0,
    "NI_IF": 0,
    "NC_IO": 0,
    "NP_IO": 0,
    "NC3_OP": 0

    # Incomplete list and names will change
}


# Base abort class, pure virtual
class Abort(Exception):
    # Basic abort
    pass

# Example of how we could make a different exception
# for each abort scenario and handle it automatically using OOP


class PressureAbort(Abort):
    # Pressure abort
    pass


class TempAbort(Abort):
    # Temperature abort
    pass


class FlowAbort(Abort):
    # Flow Abort
    pass
