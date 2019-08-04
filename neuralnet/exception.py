
class LocationException(Exception):
    pass

class LocationOccupied(LocationException):
    def __init__(self, **kw):
        if 'node' in kw:
            super(LocationOccupied, self).__init__('A node already exists at: {loc}'.format(loc=kw['node'].loc))