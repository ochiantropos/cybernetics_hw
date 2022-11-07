from pprint import pprint
from .AbstractControler import AbstractControler


class BookRoomForDateArrivalControler( AbstractControler ):
    
	def __init__( self, controler_type : str ):
		super().__init__(controler_type)

	def run_session( self ):
		pass