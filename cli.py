import os
import sys
import json
import time
import socket
import readline


#CONFIG = 'cli_connection_config.json'


class CLI:
	def __init__(self):
		self.load_settings()
		self.objects = []
		self.vars = ['LABEL', 'URLS', 'CHATS', 'time', 'UC_USER', 'UC_PASSWORD', 'GRAFANA_LOGIN', 
						'GRAFANA_PASSWORD', 'USER_API_REQUEST_ADDR', 'IP_UC_ACCESS_LAYER_WEB', 'PORT_UC_ACCESS_LAYER_WEB']

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#self.sock.setblocking(0)
		self.sock.settimeout(0.3)
		self.sock.connect(self.server_address)

		readline.parse_and_bind("tab: complete")
		readline.set_completer(self.string_completer)

	def load_settings(self):
			self.encoding = 'utf-8'
			if len(sys.argv) == 3:
				self.server_address = (sys.argv[1], int(sys.argv[2]))
			else:
				self.server_address = ('127.0.0.1', 45673)


	def main(self):
		main_menu = {'show_stat_of_certain_object':self.show_stat, 'show_config_of_certain_object':self.show_config, 'show_all_stats':self.show_all_stats, 
						"show_all_configs":self.show_all_configs, "change_config":self.change_config, "add_object":self.add_object, 
						"delete_object":self.delete_object, "show_crashes":self.show_crashes, "show_crash_info":self.show_crash_info,
						"clear_crash_logs":self.clear_crash_logs, 'quit':self.quit}

		secret_commands = {} #{'debug_log':self.debug_log}

		self.commands_with_labels = ['show_config_of_certain_object', 'show_stat_of_certain_object', 'change_config', 'delete_object']
		self.commands_with_args = self.commands_with_labels + ['show_all_stats']

		while self.update_objects() == 0:
			pass


		while True:

			self.current_commands = [key for key in main_menu]
			self.state = 'main_menu'

			if self.update_objects() == 0:
				continue

			self.labels = [obj['LABEL'] for obj in self.objects]

			command = self.get_commnand().split(' ')

			if command[0] in secret_commands:
				secret_commands[command[0]]()
				continue

			if command[0] not in main_menu:
				continue

			if self.update_objects() == 0:
				continue

			if command[0] in self.commands_with_args:
				main_menu[command[0]](command)
			else:
				main_menu[command[0]]()

			self.labels = [obj['LABEL'] for obj in self.objects]


	def update_objects(self):
		info = {'reason':'show_all_configs'}
		self.sock.send(self.prepare_object_to_sending(info))
		self.objects = self.get_information()
		self.labels = [obj['LABEL'] for obj in self.objects]

		if self.objects == None:
			self.objects = []
		elif type(self.objects) == str:
			print('Sudden network error occured, try again')
			return 0


	def show_stat(self, cmd):
		index = self.get_index_from_command(cmd)
		if index == None:
			return

		info = {'reason':'show_stat', 'index':index}
		self.sock.send(self.prepare_object_to_sending(info))

		print('\n STATS:')
		stat = self.get_information()

		print(f'Total: {len(stat["errors"]) + len(stat["successes"])}')
		print(f'Successes: {len(stat["successes"])}')
		print(f'Errors: {len(stat["errors"])}')

		if 'errors' in cmd:
			print('\n'.join(stat['errors']), end = '\n')
		elif 'successes' in cmd:
			print('\n'.join(stat['successes']), end = '\n')
		else:
			print('\n'.join(stat['stats']), end = '\n')


	def show_config(self, cmd=None, index=None):
		if type(index) != int:
			index = self.get_index_from_command(cmd)
			if index == None:
				return
		elif index == None and cmd == None:
			return

		print('\n')
		data = self.objects[index] # We already updated objects list with all configs

		for key in data:
			print(f'{key}:', data[key])

		print('\n\n')


	def debug_log(self):
		info = {'reason':'debug_log'}
		self.sock.send(self.prepare_object_to_sending(info))

		log = self.get_information()

		if log:
			for string in log:
				print(string, end='\n\n')


	def show_all_stats(self, cmd):
		info = {'reason':'show_all_stats'}
		self.sock.send(self.prepare_object_to_sending(info))

		stats = self.get_information()

		if not stats:
			print('Stats error')
			return

		for i in range(len(stats)):
			obj = stats[i]

			if obj:
				print('\n')
				print(f"{i} {self.objects[i]['LABEL']}:")
				print(f'Total: {len(obj["errors"]) + len(obj["successes"])}')
				print(f'Successes: {len(obj["successes"])}')
				print(f'Errors: {len(obj["errors"])}')
				if 'errors' in cmd:
					print('\n'.join(obj['errors']), end = '\n')
				elif 'successes' in cmd:
					print('\n'.join(obj['successes']), end = '\n')
				elif obj['stats']:
					print('\n'.join(obj['stats']), end = '\n')


	def show_all_configs(self):
		configs = self.objects # We already updated objects list with all configs

		for i in range(len(configs)):
			data = configs[i]

			print('\n')

			for key in data:
				print(f'{key}:', data[key])

			print('\n\n')


	def change_config(self, cmd):
		index = self.get_index_from_command(cmd)
		if index == None:
			return

		self.show_config(index=index)
		self.changing_config = dict(self.objects[index])

		self.state = 'change_config'
		self.current_commands = ['set', 'rm', 'add_url', 'rm_url', 'add_chat', 'rm_chat']
		self.unsettable_vars = ['URLS', 'CHATS']
		self.undeletable_vars = self.vars

		string = '(q - quit) (a - apply) \n'
		cmd = self.get_commnand(string=string)

		changes = [cmd]

		while True:
			if cmd in ['q', 'quit']:
				return

			cmd = self.get_commnand(string=string)

			if cmd in ['a', 'apply']:
				break

			changes.append(cmd)

		cfg = {}

		for change in changes:
			elements = change.split(' ')
			cmd = elements[0]

			if cmd == 'set':
				if elements[1] not in self.unsettable_vars:
					cfg[elements[1]] = ' '.join(elements[2::])
				else:
					print(f'skipping "{elements[1]}", due to unavaliability of setting')

			elif cmd == 'rm':
				if elements[1] not in self.undeletable_vars:
					cfg['remove'] = elements[1]
				else:
					print(f'skipping "{elements[1]}", due to unavaliability of deletion')

			elif cmd == 'add_url':
				url_config = elements[1::]
				if not url_config:
					self.bad_enterpretation(string=change)
					continue

				if 'timeout' in url_config:
					if len(url_config) < 3:
						self.bad_enterpretation(string=change)
						continue
					timeout = int(url_config[url_config.index('timeout') + 1])
				else:
					timeout = 5

				self.changing_config['URLS'].append({"url":url_config[0], "timeout":timeout})

				cfg['URLS'] = self.changing_config['URLS']

			elif cmd == 'rm_url' or cmd == 'rm_chat':
				if cmd == 'rm_url':
					key = 'URLS'
				else:
					key = 'CHATS'

				elements[1] = int(elements[1])
				if elements[1] >= 0 and elements[1] < len(self.changing_config[key]):
					del self.changing_config[key][elements[1]]
					cfg[key] = self.changing_config[key]

			elif cmd == 'add_chat':
				if "ID" not in elements or "type" not in elements:
					self.bad_enterpretation(string=change)

				plain_text = ""
				if 'plain_text' in elements:
					if elements.index('plain_text') < elements.index('type'):
						plain_text = ' '.join(elements[elements.index('plain_text')+1:elements.index('type')])
					else:
						plain_text = ' '.join(elements[elements.index('plain_text')+1:])

				self.changing_config['CHATS'].append({'ID':elements[elements.index('ID') + 1], 'plain_text':plain_text, 'type':elements[elements.index('type') + 1]})
				cfg['CHATS'] = self.changing_config['CHATS']


		if cfg:
			info = {'reason':'change_config', 'index':index, 'payload':cfg}
			self.sock.send(self.prepare_object_to_sending(info))

			print(self.get_information())

		self.changing_config = None


	def add_object(self):
		self.current_commands = ['quit']
		self.state = 'add_object'
		ipt = input('Enter LABEL (q - quit) -> \n')

		config = {'LABEL':ipt.replace(' ', "_"), "URLS":[], "CHATS":[], 'time':"00:00 * * *"}

		if ipt in ['q', 'quit']:
			return
		'''
		elif 'file:' in ipt:
			filename = ipt.split(':')[1]
			f = open(filename, 'r')
			config = json.load(f)
			f.close()
		'''

		for var in self.vars:
			if var not in config:
				config[var] = ""

		info = {'reason':'add_object', 'payload':config}
		self.sock.send(self.prepare_object_to_sending(info))

		print(self.get_information())


	def delete_object(self, cmd):
		index = self.get_index_from_command(cmd)
		if index == None:
			return

		info = {'reason':'delete_object', 'index':index}
		self.sock.send(self.prepare_object_to_sending(info))

		print(self.get_information())


	def get_crashes(self):
		info = {'reason':'show_crashes'}
		self.sock.send(self.prepare_object_to_sending(info))

		return self.get_information()


	def show_crashes(self):
		for crash in self.get_crashes():
			print(crash)

		print('\n')

	def show_crash_info(self):
		self.state = 'show_crash_info'
		self.current_commands = list(filter(('').__ne__, self.get_crashes())) + ['quit', 'q']
		filename = input('Enter filename of crashlog without any extensions (q - quit) -> ')
		if filename == 'q' or filename == 'quit':
			return

		if filename not in self.get_crashes():
			print('There is not such crashlog')
			return

		info = {'reason':'show_crash_info', 'payload':filename}
		self.sock.send(self.prepare_object_to_sending(info))

		print('\n')
		print(self.get_information(parse=False), end='\n\n')


	def clear_crash_logs(self):
		info = {'reason':'clear_crash_logs'}
		self.sock.send(self.prepare_object_to_sending(info))

		print(self.get_information(), end='\n\n')


	def quit(self):
		if self.sock.fileno() != -1:
			self.sock.shutdown(socket.SHUT_RDWR)
			self.sock.close()

		sys.exit()


	def objects_are_empty(self):
		return len(self.objects) == 0


	def recieve_data(self, size=2**15):
		return self.sock.recv(size).decode(self.encoding)


	def get_information(self, parse=True):
		info = self.recieve_data()
		try:
			info += self.recieve_data()
			info += self.recieve_data()
		except:
			pass

		if parse and ('[' in info or '{' in info):
			try:
				info = info.replace('True', '1')
				info = info.replace('False', '0')
				info = info.replace('None', 'null')
				return json.loads(info)
			except json.decoder.JSONDecodeError:
				print(info)
				return None #self.get_information()
		return info


	def get_index_from_user(self):
		if len(self.objects) == 0:
			print('Objects list is empty')
			return None

		labels = [obj['LABEL'] for obj in self.objects]
		self.current_commands = list(labels)

		string = f'Enter index from 0 to {len(self.objects) - 1} or label'
		res = self.get_commnand(string=string)

		if res.isnumeric():
			return int(res)
		elif res in labels:
			return labels.index(res)
		return None


	def get_index_from_command(self, cmd):
		if len(cmd) < 2:
			print('Label or index not specified')
			return
		if cmd[1] not in self.labels:
			if not cmd[1].isnumeric() or len(self.objects) <= int(cmd[1]) < 0:
				print('Label or index not specified appropriatly')
				return

			return int(cmd[1])
		else:
			return self.labels.index(cmd[1])


	def get_choice(self, lst, ask_string='Enter your choice', attempts=True, show_all_variants=True):
		if len(lst) == 0:
			return None

		if type(lst) == list:
			lst = list(lst)
			print('v - show all variants')
			if show_all_variants:
				for i in range(len(lst)):
					print(f'{i} - {lst[i]}')

		for i in range(15, 0, -1):
			try:
				if attempts:
					ch = input(f'{ask_string} ({i}) (q - quit) -> ')
				else:
					ch = input(f'{ask_string} (q - quit) -> ')

				if ch == 'q':
					return 'quit'
				elif ch == 'v':
					return self.get_choice(lst=lst, ask_string=ask_string, attempts=attempts, show_all_variants=True)

				ch = int(ch)

				if type(lst) == list:
					return ch, lst[ch]
				elif type(lst) == tuple:
					if ch < lst[0] or ch > lst[1]:
						continue

				return ch

			except:
				continue


	def get_commnand(self, string=''):
		res = None
		while not res:
			res = input(f"{string}{' ' * int(bool(string))}-> ")

		return res


	def prepare_object_to_sending(self, obj, split_data=False):
		if split_data:
			string = str(obj) + '\n'
		else:
			string = str(obj)
		return string.replace("'", '"').encode(self.encoding)


	def string_completer(self, text, state):
		commands = list(self.current_commands)
		buffer = readline.get_line_buffer().split(' ')

		if self.state == 'main_menu':
			if len(buffer) == 2:
				if buffer[0] in self.commands_with_labels:
					commands = self.labels
				elif buffer[0] == 'show_all_stats':
					commands = ['errors', 'successes']
			elif len(buffer) == 3:
				if buffer[0] == 'show_stat_of_certain_object':
					commands = ['errors', 'successes']

		if self.state == 'change_config':
			#buffer = list(filter(('').__ne__, buffer))

			if len(buffer) == 2:
				#print(buffer)
				if buffer[0] == 'set':
					commands = [key for key in self.changing_config if key not in self.unsettable_vars]
				elif buffer[0] == 'rm':
					commands = [key for key in self.changing_config  if key not in self.undeletable_vars]
				elif buffer[0] == 'add_url':
					commands = ['http://', 'https://']
				elif buffer[0] == 'rm_url':
					commands = list(map(str, list(range(0, len(self.changing_config['URLS'])))))
				elif buffer[0] == 'rm_chat':
					commands = list(map(str, list(range(0, len(self.changing_config['CHATS'])))))
				elif buffer[0] == 'add_chat':
					commands = ['ID']

			elif len(buffer) == 3:
				commands = []
				if buffer[0] == 'add_url':
					commands = ['timeout']

			elif len(buffer) >= 4:
				commands = []
				if buffer[0] == 'add_chat':
					if buffer[-2] == 'type':
						commands = ['P2P', 'GROUP']
					else:
						if 'plain_text' not in buffer:
							commands.append('plain_text')
						if 'type' not in buffer:
							commands.append('type')



		options = [cmd for cmd in commands if cmd.startswith(text)]

		if state < len(options):
			return options[state]
		else:
			return None


	def bad_enterpretation(self, string):
		print(f'Bad interpretation {string}')


def handle_help():
	string = \
			f'\t{sys.argv[0]} [MonitoringBot IP] [MonitoringBot PORT] Usage:\n\n' + \
			'If IP or PORT is not specified, 127.0.0.1:45673 is used by default\n\n' + \
			'--help, h   | show this message\n'
	print(string)

if '--help' in sys.argv or '-h' in sys.argv:
	handle_help()
else:
	CLI().main()
