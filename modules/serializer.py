import csv
import sys
import os
import pandas


class CSVserializer:

	def __init__( self, csv_table_name : str ):
		''''''
		self.__CSVdatabase_dir_name = self.__get_file_dir_name(); 
		self.__CSVdatabase_name = self.__CSVdatabase_dir_name + "\\" + csv_table_name
		self.__CSVdatabase_keys = []
		self.__CSVdatabase_infor_type = 1;
		try:
			self.__CSVdatabase_lenght = len( pandas.read_csv( self.__CSVdatabase_name ).index ) if  os.path.isfile(self.__CSVdatabase_name) else 0		
			
		except pandas.errors.EmptyDataError:
			self.__CSVdatabase_lenght = 0


	def save( self ):
		self.__write_all()

 
	def dump( self, data ):
		''''''
		if type(data) == list:
			self.dumps_into_csv(data)
		elif type(data) == dict:
			self.dump_into_csv(data) 


	def dump_into_csv( self, parameters : dict, rewrite : bool = True ):
		''''''
		self.__CSVdatabase_infor_type == dict
		self.__CSVdatabase_dataframe = pandas.DataFrame( [ parameters ] )
		self.__init_single_values( parameters );


	def dumps_into_csv( self, parameters : list, rewrite : bool = True  ):
		''''''
		self.__CSVdatabase_dataframe = pandas.DataFrame( parameters )
		self.__CSVdatabase_infor_type == list
		self.__init_significant_values( parameters );


	def load( self ):
		''''''
		self.__CSVdatabase_dataframe = self.__load_all()
		self.__CSVdatabase_dataframe.reset_index( drop=True, inplace=True )
		self.__init_significant_values( self.__CSVdatabase_dataframe.to_dict( 'records' ) )
		return self.__CSVdatabase_dataframe.to_dict( 'records' )


	''' --------------- magics method Overriding -------------- '''


	def __iter__( self ):
		for variable_key in self.__CSVdatabase_keys:
			yield variable_key, getattr( self, variable_key )


	''' --------------- private methods ----------------------- '''

 
	def __load_all( self ):
		try:
			data = pandas.read_csv( self.__CSVdatabase_name,index_col=0 )

		except pandas.errors.EmptyDataError:
			return pandas.DataFrame( data=[] )
   
		return data


	def __write_all( self ):
		data = dict( self )
		index=[ i for i in range( self.__CSVdatabase_lenght, self.__CSVdatabase_lenght+ len( getattr( self, list( self.__CSVdatabase_keys )[0] ) ) ) ]		
		df = pandas.DataFrame( data, columns=list( self.__CSVdatabase_keys ), index=index)
		df.to_csv( self.__CSVdatabase_name, mode='a', header=False if self.__CSVdatabase_lenght != 0 else True )
		self.__CSVdatabase_lenght+=len( getattr( self, list( self.__CSVdatabase_keys )[0] ) )


	''' sys method '''
	def __get_file_dir_name( self ):
		path = os.path.abspath(__file__)
		return os.path.dirname( path )


	''' init methods'''
	def __init_single_values( self, parameters : dict ):
		self.__CSVdatabase_keys = parameters.keys();
		self.__CSVdatabase_dataframe = pandas.DataFrame(data=[parameters])
		if type( parameters ) == dict:
			for param_tail,param_value in parameters.items():
				setattr( self, param_tail, param_value )


	def __init_significant_values( self, parameters : list ):
		self.__CSVdatabase_dataframe = pandas.DataFrame(data=parameters)
		if (len(parameters) != 0):
			self.__CSVdatabase_keys = parameters[0].keys();
			if type( parameters ) == list:
				for key in self.__CSVdatabase_keys:
					setattr( self, key, [ parameter[ key ] for parameter in parameters ] );
     