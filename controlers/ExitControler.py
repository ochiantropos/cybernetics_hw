from pprint import pprint
from .AbstractControler import AbstractControler
import sys


class ExitControler( AbstractControler ):
    def __init__( self, controler_type : str):
        super().__init__(controler_type)


    def run_session( self ):
        sys.exit(0);
