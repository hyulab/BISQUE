import os 

root_directory = os.path.abspath(os.path.dirname(__file__))


def get_password():
	file_handle = open('%s/user_info/sql_info.txt' %(root_directory), 'r')
	for l in file_handle:
		if l.split(':')[0].strip() == 'Password': return l.split(':')[1].strip()
	file_handle.close()

def get_username():
	file_handle = open('%s/user_info/sql_info.txt' %(root_directory), 'r')
	for l in file_handle:
		if l.split(':')[0].strip() == 'Username': return l.split(':')[1].strip()
	file_handle.close()

def get_address():
	file_handle = open('%s/user_info/sql_info.txt' %(root_directory), 'r')
	for l in file_handle:
		if l.split(':')[0].strip() == 'Address': return l.split(':')[1].strip()
	file_handle.close()

def set_password(p):
	file_handle = open('%s/user_info/sql_info.txt' %(root_directory), 'r')
	lines = file_handle.readlines()
	file_handle.close()
	output_file = open('%s/user_info/sql_info.txt' %(root_directory), 'w')
	for l in lines:
		if l.split(':')[0].strip() == 'Password': output_file.write('Password:%s\n' %(p))
		else: output_file.write(l)
	output_file.close()
 

def set_username(u):
	file_handle = open('%s/user_info/sql_info.txt' %(root_directory), 'r')
	lines = file_handle.readlines()
	file_handle.close()
	output_file = open('%s/user_info/sql_info.txt' %(root_directory), 'w')
	for l in lines:
		if l.split(':')[0].strip() == 'Username': output_file.write('Username:%s\n' %(u))
		else: output_file.write(l)
	output_file.close()

def set_address(a):
	file_handle = open('%s/user_info/sql_info.txt' %(root_directory), 'r')
	lines = file_handle.readlines()
	file_handle.close()
	output_file = open('%s/user_info/sql_info.txt' %(root_directory), 'w')
	for l in lines:
		if l.split(':')[0].strip() == 'Address': output_file.write('Address:%s\n' %(a))
		else: output_file.write(l)
	output_file.close()