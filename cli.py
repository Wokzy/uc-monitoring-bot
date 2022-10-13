import os
import sys
import json
import socket



CONFIG = 'cli_connection_config.json'


class CLI:
	def __init__(self):
		self.load_settings()
		self.objects = []

		self.sock = socket.socket()
		self.sock.connect(self.server_address)

	def load_settings(self):
		if CONFIG in os.listdir():
			data = json.load(open(CONFIG))
			self.server_address = (data['IP'], data['PORT'])
			self.encoding = data['ENCODING']
		else:
			self.encoding = 'utf-8'
			ip, port = input('Enter CLI Server address (ip:port) -> ').split(':')
			port = int(port)
			self.server_address = (ip, port)


	def main(self):
		while True:
			main_menu = [('Show stat of certain object', self.show_stat), ('Show config of sertain object', self.show_config), ('Show all stats', self.show_all_stats), 
							("Show all configs", self.show_all_configs), ("Change config", self.change_config), ("Add object", self.add_object), 
							("Delete object", self.delete_object), ("Show crashes", self.show_crashes), ("Show crash info", self.show_crash_info),
							("Clear crash logs", self.clear_crash_logs)]

			choice = self.get_choice([i[0] for i in main_menu], attempts=False, show_all_variants=False)

			if choice == None:
				continue
			elif choice == 'quit':
				self.quit()

			if self.update_objects() == 0:
				continue

			main_menu[choice[0]][1]()


	def update_objects(self):
		info = {'reason':'show_all_configs'}
		self.sock.send(self.prepare_object_to_sending(info))
		self.objects = self.get_information()

		if self.objects == None:
			self.objects = []
		elif type(self.objects) == str:
			print('Sudden network error occured, try again')
			return 0


	def show_stat(self):
		index = self.get_index_from_user(lst=self.objects)
		if index == None:
			return

		info = {'reason':'show_stat', 'index':index}
		self.sock.send(self.prepare_object_to_sending(info))

		print('\n STATS:')
		stat = self.get_information()

		print('\n'.join(stat), end = '\n')


	def show_config(self):
		index = self.get_index_from_user(lst=self.objects)
		if index == None:
			return

		print('\n')
		data = self.objects[index] # We already updated objects list with all configs

		for key in data:
			print(f'{key}:', data[key])

		print('\n\n')


	def show_all_stats(self):
		info = {'reason':'show_all_stats'}
		self.sock.send(self.prepare_object_to_sending(info))

		stats = self.get_information()

		if not stats:
			print('Stats error')
			return

		for i in range(len(stats)):
			obj = stats[i]
			ch = input(f'Press enter to show {i} (q - quit): ')
			if ch == 'q':
				break

			print('\n')
			print('\n'.join(obj), end = '\n\n')


	def show_all_configs(self):
		configs = self.objects # We already updated objects list with all configs

		for i in range(len(configs)):
			data = configs[i]
			ch = input(f'Press enter to show {i} (q - quit): ')
			if ch == 'q':
				break

			print('\n')

			for key in data:
				print(f'{key}:', data[key])

			print('\n\n')


	def change_config(self):
		index = self.get_index_from_user(lst=self.objects)
		if index == None:
			return

		cfg = input('Enter json object with parametres to be changed (example: {"time":"12:00 * * *"}) (q - quit) \n: ')
		if cfg == 'q':
			return

		cfg = json.loads(cfg.replace("'", '"'))

		info = {'reason':'change_config', 'index':index, 'payload':cfg}
		self.sock.send(self.prepare_object_to_sending(info))

		print(self.get_information())


	def add_object(self):
		ipt = input('Enter object config as json or file:FILENAME.json (q - quit) \n')
		if ipt == 'q':
			return
		elif 'file:' in ipt:
			filename = ipt.split(':')[1]
			f = open(filename, 'r')
			config = json.load(f)
			f.close()
		else:
			config = json.loads(ipt.replace("'", '"'))

		info = {'reason':'add_object', 'payload':config}
		self.sock.send(self.prepare_object_to_sending(info))

		print(self.get_information())


	def delete_object(self):
		index = self.get_index_from_user(lst=self.objects)
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
		filename = input('Enter filename of crashlog without any extensions (q - quit) -> ')
		if filename == 'q':
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


	def get_information(self, parse=True):
		info = self.sock.recv(2048).decode(self.encoding)
		if parse and ('[' in info or '{' in info):
			try:
				return json.loads(info)
			except json.decoder.JSONDecodeError:
				print(info)
				return None
		return info


	def get_index_from_user(self, lst):
		if len(lst) == 0:
			print('Objects list is empty')
			return None

		string = f'Enter index from 0 to {len(lst) - 1}'
		return self.get_choice(lst=(0, len(lst) - 1), ask_string=string)


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

	def prepare_object_to_sending(self, obj, split_data=False):
		if split_data:
			string = str(obj) + '\n'
		else:
			string = str(obj)
		return string.replace("'", '"').encode(self.encoding)


CLI().main()
