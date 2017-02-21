## Source: http://stackoverflow.com/a/42360496/4900327
class MetaEnum(type):
	def __new__(meta, name, bases, attrs):
		return super().__new__(meta, name, bases, attrs)

	def __setattr__(cls, attr, value):
		# print("Setting `%s` to %s"%(attr, value))
		if str(attr) != str(value):
			raise AttributeError
		return super().__setattr__(attr, value)


class Enum(metaclass=MetaEnum):
	'''	Enums are classes which subclass this class.

		Only enums parameters set with an identical paramter_name = parameter_value pair will be allowed.

		Example usage:
			class SearchEngines(Enum):
				Google = "Google"
			SearchEngines.Yandex = "Yandex"
			SearchEngines.Bing = "Boing" ## will raise an AttributeError
			SearchEngines.Google  ## will return 'Google'
			SearchEngines.Yandex  ## will return 'Yandex'
			SearchEngines.list()  ## will return ['Google', 'Yandex']
			obj = SearchEngines() ## will raise TypeError, as Enum should not be instantised
	'''
	def __init__(self):
		raise TypeError  ## Source: https://docs.python.org/2/library/exceptions.html#exceptions.TypeError

	@classmethod
	def list(classname):  ## Now, you can search as: `if user_input in SearchEngines.list()`
		static_vars = []
		for attribute in dir(classname):
			if not callable(getattr(classname, attribute)) and not attribute.startswith("__") and attribute == getattr(
					classname, attribute):
				static_vars.append(attribute)
		return sorted(static_vars)

class SearchEngines(Enum):
	Google = "Google"

class ProxyTypes(Enum):
	Socks5 = "Socks5"

class ProxyBrowsers(Enum):
	PhantomJS = "PhantomJS"