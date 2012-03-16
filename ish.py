#! /usr/bin/env python
#-*- coding: utf-8 -*-

import paramiko
import pickle
import cmd
import sys
import os.path
import os

'''
File: ish.py
Author: miizasa
Description: iizasa shell
'''

class RunCommand(cmd.Cmd):
    prompt = 'ish >'
    def __init__(self):
        cmd.Cmd.__init__(self)
        hd = os.environ["HOME"]
        hd = os.path.expanduser("~")
        if os.path.exists(hd + '/remotehosts.p'):
            self.hosts = pickle.load(open(hd  + '/remotehosts.p'))
        else:
            self.hosts = []
        self.connections = []
    def do_add_host(self, args):
        if args:
            self.hosts.append(args.split(','))
        else:
            print "usage: host <hostip,user,password,port>"
    def do_remove_host(self, args):
        if args:
            for host in self.hosts:
                if args == host[0]:
                    self.hosts.remove(host[0])
        else:
            print "usage: hostip"
    def do_list(self, args):
        for host in self.hosts:
            print host[0]
    def do_connect(self, args):
        for host in self.hosts:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host[0],port=int(host[3]), username=host[1], password=host[2])
            self.connections.append(client)
    def do_run(self, command):
        if command:
            for host, conn in zip(self.hosts, self.connections):
                stdin, stdout, stderr = conn.exec_command(command)
                stdin.close()
                for line in stdout.read().splitlines():
                    print 'host: %s: %s'%(host[0],line)
        else:
            print "usage: run <command>"
    def do_close(self, args):
        for conn in self.connections:
            conn.close()
    def do_exit(self, args):
        hd = os.environ["HOME"]
        hd = os.path.expanduser("~")
        pickle.dump(self.hosts, open(hd + '/remotehosts.p','w'))
        self.do_close(self)
        sys.exit()

if __name__ == '__main__':
    RunCommand().cmdloop()
