from .product_inc import (
    CheckSleep,
    CheckUpdateAtomicity,
    CheckRepeatableRead,
    CheckUpdateWithoutSelectForUpdate,
    CheckSelectForUpdate,
    CheckUpdateWithSelectForShare,
    CheckSelectForUpdateOtherRead
)

def get_cases():
    return [
        #CheckSleep
        #CheckUpdateAtomicity,
        #CheckRepeatableRead,
        #CheckUpdateWithoutSelectForUpdate,
        #CheckSelectForUpdate,
        #CheckUpdateWithSelectForShare,
        CheckSelectForUpdateOtherRead,
    ]