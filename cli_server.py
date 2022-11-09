import os
import util
import time
import json
import socket
import select
import threading

from constants import *


class CLIThread(threading.Thread):
    def __init__(self, objects):
        threading.Thread.__init__(self, daemon=True)
        self.objects = objects

        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((CLI_IP, CLI_PORT))
        self.sock.listen(5)
        self.inputs = [self.sock]
        self.outputs = []

        self.requests = {}


    def accept_connection(self, s):
        conn, addr = s.accept()
        conn.setblocking(0)
        self.inputs.append(conn)
        print(f'{addr} is connected to cli')


    def run(self):
        while self.inputs:
            self.readable, self.writable, self.exceptional = select.select(self.inputs, self.outputs, self.inputs)

            for s in self.readable:
                if s == self.sock:
                    self.accept_connection(s)
                else:
                    try:
                        data = s.recv(512)
                    except:
                        self.disconnect(s)
                        continue

                    if data:
                        try:
                            data = json.loads(data.decode(ENCODING))
                        except Exception as e:
                            print(e)
                            continue

                        self.requests[s] = data
                        if s not in self.outputs:
                            self.outputs.append(s)

            #time.sleep(.1)

            for s in self.writable:
                self.outputs.remove(s)
                if s in self.requests:
                    data = self.requests[s]

                    if data['reason'] == 'show_stat':
                        self.show_stat(s, data['index'])
                    elif data['reason'] == 'show_all_stats':
                        self.show_all_stats(s)
                    elif data['reason'] == 'show_config':
                        self.show_config(s, data['index'])
                    elif data['reason'] == 'show_all_configs':
                        self.show_all_configs(s)
                    elif data['reason'] == 'change_config':
                        self.change_config(s, data['index'], data['payload'])
                    elif data['reason'] == 'add_object':
                        self.add_object(s, data['payload'])
                    elif data['reason'] == 'delete_object':
                        self.delete_object(s, data['index'])
                    elif data['reason'] == 'show_crashes':
                        self.show_crashes(s)
                    elif data['reason'] == 'show_crash_info':
                        self.show_crash_info(s, data['payload'])
                    elif data['reason'] == 'clear_crash_logs':
                        self.clear_crash_logs(s)

                    del self.requests[s]


    def get_stat(self, index):
        if 'STATS' in self.objects[index]:
            return self.objects[index]['STATS']
        else:
            return []


    def get_config(self, index):
        cfg = dict(self.objects[index])
        cfg['time'] = cfg['time_config']
        del cfg['time_config']

        if "STATS" in cfg:
            del cfg['STATS']

        return cfg


    def show_config(self, s, index):
        s.sendall(util.prepare_object_to_sending(ENCODING, self.get_config(index)))


    def show_all_configs(self, s):
        configs = [self.get_config(i) for i in range(len(self.objects))]
        data = util.prepare_object_to_sending(ENCODING, configs)
        s.sendall(data)


    def show_stat(self, s, index):
        s.sendall(util.prepare_object_to_sending(ENCODING, self.get_stat(int(index))))


    def show_all_stats(self, s):
        stats = [self.get_stat(i) for i in range(len(self.objects))]
        s.sendall(util.prepare_object_to_sending(ENCODING, stats))


    def show_crashes(self, s):
        crashes = [crash.split(CRASH_LOGS_FILE_FORMAT)[0] for crash in os.listdir(CRASH_LOGS_DIRECTORY)]
        s.sendall(util.prepare_object_to_sending(ENCODING, crashes))


    def show_crash_info(self, s, filename):
        with open(f"{CRASH_LOGS_DIRECTORY}/{filename}{CRASH_LOGS_FILE_FORMAT * (CRASH_LOGS_FILE_FORMAT not in filename)}", 'r') as f:
            crash_info = f.read()
            f.close()

        s.sendall(util.prepare_object_to_sending(ENCODING, crash_info))


    def clear_crash_logs(self, s):
        for file in os.listdir(CRASH_LOGS_DIRECTORY):
            if '.txt' in file:
                os.remove(f'{CRASH_LOGS_DIRECTORY}/{file}')

        s.sendall(util.prepare_object_to_sending(ENCODING, 'Successfully clened!'))



    def change_config(self, s, index, config):

        old_object_config = dict(self.objects[index])
        time = self.objects[index]['time']

        if 'time' in config:
            try:
                time = util.set_time_conditions(config['time'])
                tm = config['time']
            except:
                s.sendall(util.prepare_object_to_sending(ENCODING, 'Bad interpretation\n'))
                del config['time']

        for obj in config:
            if obj == 'remove':
                if config[obj] in self.objects[index]:
                    del self.objects[index][config[obj]]
                    continue
            
            if  type(config[obj]) == str:
                if config[obj].isnumeric():
                    config[obj] = int(config[obj])
                elif config[obj].lower() == "false":
                    config[obj] = 0
                elif config[obj].lower() == "true":
                    config[obj] = 1

            self.objects[index][obj] = config[obj]

        cfg, old_cfg = self.load_config()

        try:
            cfg['CHATS_OBJECTS'][index] = dict(self.objects[index])

            if 'time' in config:
                cfg['CHATS_OBJECTS'][index]['time'] = tm
            else:
                cfg['CHATS_OBJECTS'][index]['time'] = cfg['CHATS_OBJECTS'][index]['time_config']

            del cfg['CHATS_OBJECTS'][index]['time_config']
            if 'STATS' in cfg['CHATS_OBJECTS'][index]:
                del cfg['CHATS_OBJECTS'][index]['STATS']

            f = open(CONFIG_PATH, 'w')
            json.dump(cfg, f)
            f.close()

            if 'time' in config:
                self.objects[index]['time'] = time
                self.objects[index]['time_config'] = tm

            s.sendall(util.prepare_object_to_sending(ENCODING, 'Config has been successfully changed'))
        except:
            self.objects[index] = dict(old_object_config)
            s.sendall(util.prepare_object_to_sending(ENCODING, 'Bad interpretation'))


    def delete_object(self, s, index):
        del self.objects[index]

        cfg, old_cfg = self.load_config()

        try:
            del cfg['CHATS_OBJECTS'][index]

            self.dump_config(cfg)

            s.sendall(util.prepare_object_to_sending(ENCODING, 'Object has been deleted'))
        except:
            self.dump_config(old_cfg)


    def add_object(self, s, config):

        self.objects.append(config)

        cfg, old_cfg = self.load_config()

        try:
            cfg['CHATS_OBJECTS'].append(config)

            self.dump_config(cfg)

            self.objects[-1]['time_config'] = config['time']
            self.objects[-1]['time'] = util.set_time_conditions(config['time'])

            s.sendall(util.prepare_object_to_sending(ENCODING, 'Object has been created'))
        except:
            self.dump_config(old_cfg)
            self.objects.pop()
            s.sendall(util.prepare_object_to_sending(ENCODING, 'Bad interpretation, objects hasn\'t been added'))


    def load_config(self):
        f = open(CONFIG_PATH, 'r')
        cfg = json.load(f)
        old_cfg = dict(cfg)
        f.close()

        return cfg, old_cfg


    def dump_config(self, cfg):
        f = open(CONFIG_PATH, 'w')
        json.dump(cfg, f)
        f.close()


    def disconnect(self, s):
        if s in self.outputs:
            self.outputs.remove(s)
        self.inputs.remove(s)

        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            pass

    def quit(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        exit()

