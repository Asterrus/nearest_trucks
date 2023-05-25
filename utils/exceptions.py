class InvalidZip(Exception):
    def __init__(self, zip: str):
        self.text = f'location with zip {zip} was not found'
