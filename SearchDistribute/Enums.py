
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
			elif name==value:
				vals = set(vals + [name])
				self = self.__init__(vals)
				return
			else:
				raise AttributeError 
			
	def __delattr__(self, name):			## used as:	 del(Enum.VAL)
		vals = [i for i in self]
		if name not in vals:
			raise AttributeError
		vals.remove(name)
		vals = set(vals)
		self = self.__init__(vals)


###-----------------------------TESTS-----------------------------###
# p = Enum()
# print([x for x in p])
# p.DOG = "DOG"
# p.CAT = "CAT"
# print("p is: %s"%p)
# print("p is: %s"%[x for x in p])
# if p.RAT is None:
# 	print("p.RAT is None")
# if "CAT" in p:
# 	print("CAT is in p")
# if p.CAT in p:
# 	print("p.CAT is in p")
# print(["CAT","DOG"] in [x for x in p])
# print(type(p.CAT))
# print(type(p.CAT)==type(""))
# print(type(p))
# print(type(p)==type(Enum([])))


# x=[None, '2', None, 'aa']
# for y in [z for z in x if z is not None]:
# 	print y