def vin_validator(vin: str) -> str:
    if len(vin) != 5:
        raise ValueError('The VIN length should be 5')
    if not 1000 <= int(vin[:4]) <= 9999:
        raise ValueError('The VIN number should be between 1000 and 9999')
    if not 'A' <= vin[-1] <= 'Z':
        raise ValueError('The letter must be a capital English letter')
    return vin
