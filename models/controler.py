from controlers.AbstractControler import AbstractControler

class Controler:
	"""docstring for Controler"""
	def __init__( self, TypedControler : AbstractControler.__class__ ):
		self.ControlerTypeClass = TypedControler

		self.ControlerTypeClass.run_session()


	def get_login_form_locals_controlers( self ):
		return self.ControlerTypeClass.Logined


	def redirect_to_local_session(self):
		pass