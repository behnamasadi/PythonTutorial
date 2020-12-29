#https://www.youtube.com/watch?v=bPaVoXyTBX4&list=PLplJltxWVIbIjWVcNStHBkPsaRLpYnDBU&index=10
class Component:
	def Operation(self):
		raise NotImplenetedError("Operation() must be defined in the sub class")

class ConcretComponent(Component):
	def operation(self):
		print("ConcretComponent:Operation")

class Decorator(Component):
	def __init__(self,obj):
		self.comp=obj

	def Operation(self):
		print("Decorator::Operation")
		self.comp.Operation()
