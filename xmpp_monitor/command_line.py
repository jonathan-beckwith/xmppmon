from sys import argv

from xmpp_monitor import server
from xmpp_monitor import database
from xmpp_monitor import presence

def main():
	if len(argv) == 1:
		print('Usage:')
		print('\txmpp_monitor <command> [options]')
		print('\nCommands:')
		print('\tstart\tStarts the server')
		return

	command = argv[1]
	if command == 'start':
		server.start()
	if command == 'stop':
		server.stop()
	if command == 'init':
		database.init()
	if command == 'scan':
		presence.start()
	if command == 'summary':
		presence.create_summary()
	if command == 'start_all':
		server.start()
		presence.start()