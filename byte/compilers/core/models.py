class Operation(object):
    pass


class DeleteOperation(Operation):
    pass


class InsertOperation(Operation):
    def __init__(self, items):
        self.items = items


class SelectOperation(Operation):
    def __init__(self, where):
        self.where = where


class UpdateOperation(Operation):
    pass
