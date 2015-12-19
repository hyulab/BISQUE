from os import system, path

root_directory = path.abspath(__file__ + "/../")

print '		#######################################'
print "		#WELCOME TO BISQUE (LITE) INSTALLATION#"
print "		#######################################"
raw_input('Press ENTER to continue. Or, press Ctrl+C to cancel installation.')

###################################################
#MOVING BISQUE.PY INTO $PATH AND MAKING EXECUTABLE#
###################################################
system('rm /usr/local/bin/bisque')
system('sudo chmod +x bisque.py')
system('sudo ln -s %s/bisque.py /usr/local/bin/bisque' %(root_directory))

print "Installation complete!"