# -*- coding: utf-8 -*-

"""byte - model module."""
from __future__ import absolute_import, division, print_function

from byte.core.property import Property, PropertyError, RelationProperty

from six import add_metaclass
import inspect


class ModelError(Exception):
    """Generic model error."""


class ModelParseError(ModelError):
    """Model parse error."""


class ModelPropertyError(ModelError, PropertyError):
    """Model property violation."""


class ModelInternal(object):
    """Private structure for internal data model attributes."""

    def __init__(self):
        """Create internal data model structure."""
        self.primary_key = None

        # Private attributes
        self._properties_by_key = None
        self._properties_by_name = None

    @property
    def properties_by_key(self):
        """Retrieve model properties by key."""
        return self._properties_by_key

    @properties_by_key.setter
    def properties_by_key(self, value):
        """Update model properties by key."""
        self._properties_by_key = value
        self._properties_by_name = dict([(prop.name, prop) for prop in value.values()])

    @property
    def properties_by_name(self):
        """Retrieve model properties by name."""
        return self._properties_by_name


class ModelOptions(object):
    """Private structure for data model options."""

    def __init__(self, items=None):
        """
        Create data model options structure.

        :param items: Options dictionary
        :type items: dict
        """
        self.items = items or {}

    @property
    def slots(self):
        """Retrieve flag indicating model slots have been enabled."""
        return self.items.get('slots', False)

    @classmethod
    def parse(cls, value):
        """
        Parse model options from dictionary or object.

        :param value: Options
        :type value: dict or object
        """
        if not value:
            return cls()

        if type(value) is dict:
            return cls(value)

        options = {}

        for key in dir(value):
            if key.startswith('_'):
                continue

            options[key] = getattr(value, key)

        return cls(options)


class ModelProperties(object):
    """Private structure for data model properties."""

    def __init__(self, properties):
        """
        Create data model properties structure.

        :param properties: Properties dictionary
        :type properties: dict
        """
        self.__all__ = properties

        for key, value in properties.items():
            setattr(self, key, value)

    @classmethod
    def extract(cls, namespace):
        """
        Extract model properties from namespace.

        :param namespace: Class namespace
        :type namespace: dict
        """
        properties = {}

        for key, prop in cls.__extract(namespace):
            if key in properties:
                raise ModelPropertyError("Duplicate property '%s' defined on model" % (key,))

            properties[key] = prop

        return cls(properties)

    @classmethod
    def __extract(cls, namespace):
        for key, value in cls.__extract_properties(namespace.get('Properties')):
            yield key, value

        for key, value in cls.__extract_properties(namespace, remove=True):
            yield key, value

    @classmethod
    def __extract_properties(cls, namespace, remove=True):
        if not namespace:
            return

        # Iterate over items in `namespace`
        for key in cls.__get_namespace_keys(namespace):
            if key.startswith('_'):
                continue

            # Retrieve item value
            value = cls.__get_namespace_value(namespace, key)

            if not value or not isinstance(value, Property):
                continue

            # Yield property
            yield cls.__extract_property(
                key, value,
                namespace=namespace,
                remove=remove
            )

    @staticmethod
    def __extract_property(key, value, namespace=None, remove=False):
        if not remove:
            return key, value

        # Remove property from `namespace` (if enabled)
        if namespace is None:
            raise ValueError('Missing required "namespace" parameter (when "remove" has been enabled)')

        if type(namespace) is dict:
            del namespace[key]
        else:
            delattr(namespace, key)

        return key, value

    @staticmethod
    def __get_namespace_keys(namespace):
        if type(namespace) is dict:
            return list(namespace.keys())

        return dir(namespace)

    @staticmethod
    def __get_namespace_value(namespace, key):
        if type(namespace) is dict:
            return namespace[key]

        return getattr(namespace, key)


class ModelMeta(type):
    """Data model metaclass."""

    def __new__(mcs, name, bases=None, namespace=None):
        """
        Create data model class.

        :param name: Class name
        :type name: str

        :param bases: Class bases
        :type bases: tuple

        :param namespace: Class namespace
        :type namespace: dict
        """
        if not mcs.__is_model(name, bases, namespace):
            return super(ModelMeta, mcs).__new__(mcs, name, bases, namespace)

        internal = namespace['Internal'] = ModelInternal()
        options = namespace['Options'] = ModelOptions.parse(namespace.pop('Options', None))
        properties = namespace['Properties'] = ModelProperties.extract(namespace)

        # Define `__slots__` (if enabled)
        if options.slots:
            namespace['__slots__'] = mcs.__get_slots(namespace, properties)

        # Bind methods
        namespace['__init__'] = mcs.__create_init(bases, namespace, properties)

        # Construct model
        cls = type.__new__(mcs, name, bases, namespace)

        # Bind model
        mcs.__bind(cls, internal, properties)

        return cls

    def __getitem__(self, key):
        return self.Internal.properties_by_key.get(key)

    @staticmethod
    def __is_model(name, bases=None, namespace=None):
        # Ignore invalid classes
        if not bases or not namespace or bases[0] is object:
            return False

        # Ignore the `ModelMixin` class
        if name == 'ModelMixin' and namespace.get('__module__') == 'byte.model':
            return False

        # Ignore mixin classes
        if bases[0].__name__ == 'ModelMixin' and bases[0].__module__ == 'byte.model':
            return False

        # Model class matched
        return True

    @staticmethod
    def __get_slots(namespace, properties):
        slots = set(namespace.get('slots', []) + [
            '__collection__'
        ])

        for key, prop in properties.__all__.items():
            if prop.relation:
                slots.add(key + '_id')  # Identifier property
                slots.add('_RelationProperty_' + key)  # Resolution cache
            else:
                slots.add(key)

        return tuple(slots)

    @staticmethod
    def __create_init(bases, namespace, properties):
        original = namespace.get('__init__')

        def __init__(self, *args, **kwargs):
            self.__collection__ = kwargs.pop('_collection', None)

            # Set initial property values
            for key, prop in properties.__all__.items():
                # Resolve default value
                if inspect.isfunction(prop.default):
                    value = prop.default()
                else:
                    value = prop.default

                # Set default value for property
                setattr(self, key, kwargs.get(key, value))

            # Call original or super `__init__` method
            if original:
                original(self, *args, **kwargs)
            elif bases[0] is not object:
                bases[0].__init__(self, *args, **kwargs)

        return __init__

    @classmethod
    def __bind(mcs, cls, internal, properties):
        # Register model
        # Registry.register_model(cls)

        # Bind properties to model
        mcs.__bind_properties(cls, internal, properties)

    @classmethod
    def __bind_properties(mcs, cls, internal, properties):
        for key in list(properties.__all__.keys()):
            prop = properties.__all__[key]

            # Bind property
            if prop.relation:
                mcs.__bind_property_relation(cls, properties, key, prop)
            else:
                mcs.__bind_property(cls, internal, key, prop)

        # Define properties dictionary on `Internal` class
        internal.properties_by_key = properties.__all__

    @staticmethod
    def __bind_property(cls, internal, key, prop):
        # Bind property to model
        prop.bind(cls, key)

        # Define primary key on `Internal` class
        if prop.primary_key:
            if internal.primary_key:
                raise ModelPropertyError('Multiple primary key properties are not permitted')

            internal.primary_key = prop

    @staticmethod
    def __bind_property_relation(cls, properties, key, prop):
        # Bind `prop` (to ensure metadata is available)
        prop.bind(cls, key + '_id')

        # Create identifier property
        p_id = Property(prop.relation.value_type)
        p_id.bind(cls, key + '_id')

        # Create resolve property
        p_resolve = RelationProperty(p_id, prop.value_type)
        p_resolve.bind(cls, key)

        # Store resolve property on model
        setattr(cls, key, p_resolve)

        # Store resolve property on model `Properties`
        setattr(properties, key, p_resolve)
        properties.__all__[key] = p_resolve

        # Store identifier property on model `Properties`
        setattr(properties, key + '_id', p_id)
        properties.__all__[key + '_id'] = p_id


@add_metaclass(ModelMeta)
class Model(object):
    """Base data model class."""

    __slots__ = [
        'byte_engine'
    ]

    def __init__(self, **kwargs):
        """Create data model item."""
        self.byte_engine = None

        # Set properties on object (without validation)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, **kwargs):
        """Create model item, validate provided properties and save it to the engine (if defined)."""
        item = cls(**kwargs)

        # TODO Validate values against property types

        # Save item to engine (if defined)
        if item.byte_engine:
            item.save(mode='insert')

        return item

    @classmethod
    def from_plain(cls, data, engine=None, strict=True, translate=False):
        """
        Parse model item from plain dictionary.

        :param data: Item data
        :type data: dict

        :param strict: Enable strict model parsing (errors will raise exceptions)
        :type strict: bool

        :param translate: Enable data type translation (parse simple types into python data types)
        :type translate: bool

        :return: Model item
        :rtype: byte.model.Model
        """
        # Retrieve property descriptors
        properties_by_name = cls.Internal.properties_by_name

        if properties_by_name is None:
            raise ModelParseError('No properties defined')

        # Construct item instance
        obj = cls(
            byte_engine=engine
        )

        # Parse properties from dictionary
        for name, value in data.items():
            # Find matching property (by name)
            prop = properties_by_name.get(name)

            if not prop:
                if strict:
                    raise ModelParseError('Unknown property: %s' % (name,))

                continue

            # Decode property value
            valid, value = cls.__decode_property(
                prop, value,
                strict=strict,
                translate=translate
            )

            if not valid:
                continue

            # Set property value
            prop.set(obj, value)

        return obj

    def save(self, engine=None, mode=None, execute=True):
        """Save item to engine."""
        engine = engine or self.byte_engine

        if not engine:
            raise ModelError('Item hasn\'t been bound to any engine')

        # Save item to collection
        if mode == 'insert':
            return engine.insert().items(self.to_plain()).execute()

        raise NotImplementedError

    def to_plain(self, translate=False):
        """Dump model item to plain dictionary.

        :param translate: Enable data type translation (convert python data types into simple types)
        :type translate: bool

        :return: Plain dictionary
        :rtype: dict
        """
        result = {}

        for name, prop in self.__class__.Internal.properties_by_name.items():
            value = prop.get(self)

            if prop.primary_key and value is None:
                continue

            result[name] = prop.encode(value, translate=translate)

        return result

    @staticmethod
    def __decode_property(prop, value, strict=True, translate=False):
        # Try decode property value
        try:
            value = prop.decode(
                value,
                translate=translate
            )
        except Exception as ex:
            if strict:
                raise ModelParseError('Unable to decode value provided for property: %s - %s' % (prop.key, ex))

            return False, None

        # Validate decoded value against property
        if not prop.validate(value):
            if strict:
                raise ModelParseError('Invalid value provided for property: %s' % (prop.key,))

            return False, None

        # Decoded valid property value
        return True, value

    def __repr__(self):
        """Retrieve string representation of model item."""
        class_name = self.__class__.__name__
        primary_key = self.__class__.Internal.primary_key

        if primary_key:
            return '<%s %s: %r>' % (
                class_name,
                primary_key.key,
                primary_key.get(self)
            )

        return '<%s>' % class_name


class ModelMixin(Model):
    """Base class for model mixins."""