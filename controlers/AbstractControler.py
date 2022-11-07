from abc import ABC, abstractmethod


class AbstractControler( ABC ):
	def __init__( self, controler_type : str ):
		self.controler_type = controler_type
		self.Logined = False


	@abstractmethod
	def run_session( self ):
		pass
