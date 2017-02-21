class Enum():	## Source: http://stackoverflow.com/a/2182437/4900327
	'''	Note: only enums set with an identical paramter_name = parameter_value pair will be allowed.
		e.g. SearchEngines.Google = "Google" will work
			 SearchEngines.Bing = "Boing" won't work; it won't show up when we do SearchEngines.list()
	'''
	## Source: http://stackoverflow.com/a/1398059/4900327
	## and http://stackoverflow.com/a/35864720/4900327
	## and http://radek.io/2011/07/21/static-variables-and-methods-in-python/
	@classmethod
	def list(classname):		## Now, you can search as: `if user_input in SearchEngines.list()`
		static_vars = []
		for attribute in dir(classname):
			if not callable(getattr(classname, attribute)) and not attribute.startswith("__") and attribute == getattr(classname, attribute):
				static_vars.append(attribute)
		return static_vars

	def __getattr__(self, name):
		if name in self:
			return name
		return None

	def __setattr__(self, name, value):
		vals = [i for i in self]
		if value=="" or value==None:		## used as: Enum.VAL = "" or Enum.VAL = None i.e. we are trying to delete
			if name not in vals:			## used as: Enum.VAL_XYZ = "" i.e. we are trying to remove something that doesn't exist.
				return
			else:
				vals.remove(name)
				self = self.__init__(vals)
				return

		else:								## used as: Enum.VAL = "VAL" i.e. we are trying to set a new value.
			if name in vals:
				return
			elif str(name) == str(value):
				vals = set(vals + [name])
				self = self.__init__(vals)
				return
			else:
				raise AttributeError

	def __delattr__(self, name):			## used as:	 del(Enum.VAL)
		raise AttributeError
		vals = [i for i in self]
		if name not in vals:
			raise AttributeError
		vals.remove(name)
		vals = set(vals)
		self = self.__init__(vals)


class SearchEngines(Enum):
	Google = "Google"


SearchEngines.Soo = "gog"
del(SearchEngines.Google)
print(SearchEngines.list())

class ProxyTypes(Enum):
	Socks5 = "Socks5"

class ProxyBrowsers(Enum):
	PhantomJS = "PhantomJS"

