
from controlers.AbstractControler import AbstractControler
from controlers.LoginControler import LoginControler
from controlers.RegisterControler import RegisterControler
from controlers.BookRoomForDateArrivalControler import BookRoomForDateArrivalControler
from controlers.BookRoomForDateDepartureControler import BookRoomForDateDepartureControler
from controlers.ReplenishTheBalanceControler import ReplenishTheBalanceControler
from controlers.VievCommandsControler import VievCommandsControler
from controlers.ViewListOfAllRoomsControler import ViewListOfAllRoomsControler
from controlers.ExitControler import ExitControler
from controlers.BreakTheLoginedControler import BreakTheLoginedControler

from models.controler import Controler


class MainSession:
	def __init__(self):
		self.__Logined = [1,2]
		self.__END_EVENT = False

		self.events = {
			# name of command , modificator, self controler
			'0' : [ "view_commands", 2,None],
			'1' : [ "register", 1, RegisterControler('1') ],
			'2' : [ "login", 1, LoginControler('2') ],
			'3' : [ "replenish_the_balance", 0, ReplenishTheBalanceControler('3') ],
			'4' : [ "view_list_of_all_rooms", 0, ViewListOfAllRoomsControler('4') ],
			'5' : [ "book_room_for_date_arrival", 0, BookRoomForDateArrivalControler('5') ],
			'6' : [ "book_room_for_date_departure", 0, BookRoomForDateDepartureControler('6') ],
			'7' : [ "exit", 2, ExitControler('7') ],
			'8' : [ "break_the_logined",0,BreakTheLoginedControler('1') ]
  		}

		self.events[ '0' ][ 2 ] =  VievCommandsControler('0',{ key : value[ 0 ] for key,value in self.events.items() if value[ 1 ] in self.__Logined })
		self.answer = [None,None]	
		self.controler = None
		

	def run( self ):
		while not self.__END_EVENT:
			self.command_entry_process( self.__Logined )


	def command_entry_process( self, logined : list ):	
		self.answer = self.session_filter( input("Enter the comand: ") , logined )
		print(self.answer)

		if self.answer[ 0 ]:
			self.controler = Controler( self.events[ self.answer[ 1 ] ][2] )
			
			if self.controler.get_login_form_locals_controlers():
				if self.__Logined[ 0 ] == 0:
					self.__Logined[ 0 ] = 1
				else:
					self.__Logined[ 0 ] = 0

				self.events[ '0' ][ 2 ] =  VievCommandsControler('0',{ key : value[ 0 ] for key,value in self.events.items() if value[1] in self.__Logined })

			print(self.__Logined)

		else:
			self.command_doesnt_found()


	def command_doesnt_found( self ):
		print("Command has not founded!!!")


	def session_filter( self, event : int, logined_type : list ):
		string_keys = [self.events[item][0] for item in self.events.keys()]
		if event in self.events.keys():

			if event in string_keys:
				event = [ self.events[ item ][ 0 ] for item in self.events.keys() if self.events[ item ][ 0 ] == event ][ 0 ]

			if self.events[ event ][ 1 ] in logined_type:
				return True,event

			else:
				return False,event

		else:
			return False,None



if __name__ == '__main__':

	MainSession().run()