from models.controler import Controler
from models.controler import VievCommandsControler, LoginControler, RegisterControler, ReplenishTheBalanceControler, ViewListOfAllRoomsControler, BookRoomForDateArrivalControler, BookRoomForDateDepartureControler



class MainSession:
	def __init__(self):

		self.events = {
			# name of command , modificator, self controler
			0 : [ "view_commands", True,None],
			1 : [ "register", True, RegisterControler('1') ],
			2 : [ "login", True, LoginControler('2') ],
			3 : [ "replenish_the_balance", False, ReplenishTheBalanceControler('3') ],
			4 : [ "view_list_of_all_rooms", False, ViewListOfAllRoomsControler('4') ],
			5 : [ "book_room_for_date_arrival", False, BookRoomForDateArrivalControler('5') ],
			6 : [ "book_room_for_date_departure", False, BookRoomForDateDepartureControler('6') ],
		}
		self.events[0][2] =  VievCommandsControler('0',{ key : [value[0], value[1]] for key,value in self.events.items() })
		self.answer = [None,None]	
		self.__END_EVENT = False
		self.controler = None
		

	def run( self ):
		while not self.__END_EVENT:
			self.command_entry_process( False )
   
   
	def command_entry_process( self, logined : bool = False ):	
		self.answer = self.session_filter( int( input() ), logined )
  
		if self.answer[ 0 ]:
			self.controler = Controler( self.events[ self.answer[ 1 ] ] )
   
		else:
			self.command_doesnt_found()


	def command_doesnt_found( self ):
		print("Command dosnt fount!!!")


	def session_filter( self, event : int, logined_type : bool = False ):
		if event in self.events.keys():
			if not self.events[ event ][ 1 ] == logined_type:
				return True,event
			else:
				return False,event

		else:
			return False,None



if __name__ == '__main__':

	MainSession().run()