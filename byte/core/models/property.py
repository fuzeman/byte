class BaseProperty(object):
    """Base class for properties."""

    def get(self, obj):
        """Get property value from object.

        :param obj: Item
        :type obj: byte.model.Model
        """
        raise NotImplementedError

    def set(self, obj, value):
        """Set property value on object.

        :param obj: Item
        :type obj: byte.model.Model

        :param value: Value
        :type value: any
        """
        raise NotImplementedError
