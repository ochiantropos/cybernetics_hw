from abc import ABC, abstractmethod
from pprint import pprint

class AbstractControler( ABC ):
	def __init__( self, controler_type : str ):
		self.controler_type = controler_type


	@abstractmethod
	def run_session( self ):
		pass



class VievCommandsControler( AbstractControler ):
	def __init__( self, controler_type : str, elements : dict ):
		super().__init__(controler_type)
		print(elements)


	def run_session( self ):
		print("ahah sosi")



class LoginControler( AbstractControler ):
	def __init__( self, controler_type : str ):
		super().__init__(controler_type)


	def run_session( self ):
		print("ahah sosi")


class RegisterControler( AbstractControler ):

	def __init__( self, controler_type : str ):
		super().__init__(controler_type)

	def run_session( self ):
		pass


class ReplenishTheBalanceControler( AbstractControler ):

	def __init__( self, controler_type : str ):
		super().__init__(controler_type)

	def run_session( self ):
		pass


class ViewListOfAllRoomsControler( AbstractControler ):

	def __init__( self, controler_type : str ):
		super().__init__(controler_type)

	def run_session( self ):
		pass


class BookRoomForDateArrivalControler( AbstractControler ):

	def __init__( self, controler_type : str ):
		super().__init__(controler_type)

	def run_session( self ):
		pass



class BookRoomForDateDepartureControler( AbstractControler ):

	def __init__( self, controler_type : str ):
		super().__init__(controler_type)

	def run_session( self ):
		pass





class Controler:
	"""docstring for Controler"""
	def __init__( self, TypedControler : AbstractControler.__class__ ):
		self.ControlerTypeClass = TypedControler



	def redirect_to_local_session(self):
		self.ControlerTypeClass.run_session()