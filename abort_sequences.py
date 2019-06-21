# This file contains all of the custom exceptions that
# execute the abort sequences when called


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
