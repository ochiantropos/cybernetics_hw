from pprint import pprint
from .AbstractControler import AbstractControler


class VievCommandsControler( AbstractControler ):
    def __init__( self, controler_type : str, elements : dict ):
        super().__init__( controler_type )
        self.elements = elements


    def run_session( self ):
        print("\n------------Available commands------------\n")
        self.view_commands()


    def view_commands( self ):
        for key,value in self.elements.items():
            print( "Command key:: {0:3s} or {1:15s}".format( str(key), str( value ) ) )