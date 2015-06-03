from config.header import Header
from config.write_output import print_debug, print_output
from config.moduleInfo import ModuleInfo
import re
import os

class wpa_supplicant(ModuleInfo):

	filestr = '/etc/wpa_supplicant/wpa_supplicant.conf'


	def __init__(self):
		options = {'command': '-wp', 'action': 'store_true', 'dest': 'wpa_supplicant', 'help': 'WPA Supplicant - Need root Privileges'}
		ModuleInfo.__init__(self, 'wpa_supplicant', 'wifi', options)

	def parse_file_network(self, fd):
		password=None
		ssid=None

		for line in fd:
			if re.match('^[ \t]*ssid=', line):
				ssid=(line.split("\"")[1])
			if re.match('^[ \t]*psk=', line):
				password=line.split("\"")[1]
			if re.match('^[ \t]*password=', line):
				password=line.split("\"")[1]
			if re.match('^[ \t]*}', line):
				return (ssid, password)



	def parse_file(self):
		pwdFound = []
		fd = open(self.filestr)

		for line in fd:
			if "network=" in line:
				values = {}
				(ssid,password) = self.parse_file_network(fd)
				if ssid and password:
					values['PASSWORD'] = password
					values['SSID'] = ssid
					pwdFound.append(values)
		return pwdFound;


	def check_file_access(self):
		if not os.path.exists(self.filestr):
			print_debug('WARNING', 'the path "%s" does not exist' %(self.filestr))
			return -1
		return 0

	def run(self):
		Header().title_info('Wifi (from WPA Supplicant)')
		if self.check_file_access():
			return
		pwdFound = self.parse_file()

		print_output("wpa_supplicant", pwdFound)
