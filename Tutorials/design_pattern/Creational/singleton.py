class Singleton:
	instance = None
	@classmethod
	def Instance(cls):
		if cls.instance == None:
			cls.instance=Singleton()
		return 	cls.instance

	def __init__(self):
		if self.instance!=None:
			raise ValueError("An other instanc is already running!")



	def setData(self,value):
		self.value=value


	def getData(self):
		return self.value




obj1=Singleton.Instance().setData(10)
obj2=Singleton.Instance().getData()
