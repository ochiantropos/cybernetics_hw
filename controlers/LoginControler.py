from .AbstractControler import AbstractControler
import stdiomask


class LoginControler( AbstractControler ):
	def __init__( self, controler_type : str ):
		super().__init__(controler_type)
  

	def run_session( self ):
		self.get_information()

		
	def get_information( self ):
		print("\n-----------------Logining-----------------\n")
		login = self.get_login()
		password = self.get_password()

		# launching methods to check the entered information


		# change the globall status

		self.Logined = True

		print("\n\n")


	def get_password( self ):
		return stdiomask.getpass( prompt="{0:15s}".format( "Password:" ), mask='*' ) # will add validator class


	def get_login( self ):
		return input( "{0:15s}".format( "Login:" ) )












