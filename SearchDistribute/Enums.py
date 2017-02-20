
class Enum(set):	## Source: http://stackoverflow.com/a/2182437/4900327
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
				# print("name: %s %s; value: %s %s"%(name, type(name), value, type(value)))
				raise AttributeError
			
	def __delattr__(self, name):			## used as:	 del(Enum.VAL)
		vals = [i for i in self]
		if name not in vals:
			raise AttributeError
		vals.remove(name)
		vals = set(vals)
		self = self.__init__(vals)





class SearchEngine(Enum):
    Google = "Google"

class ProxyBrowser(Enum):
	PhantomJS = "PhantomJS"