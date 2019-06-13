"""
Summary:
    Python Script to run webform via a webservice to run as the GUI of the Ivan Application
    
Author:
    grimmvenom <grimmvenom@gmail.com>
    

Helpful CSS Tool:
https://github.com/uncss/uncss

"""

import os, sys, json
from bottle import Bottle, route, post, get, run, request, static_file
from multiprocessing import Process, Queue
import subprocess, webbrowser
from enum import Enum


class MyApp(Bottle):
    def __init__(self, name):
        super(MyApp, self).__init__()
        self.name = name
        self.route('/', callback=self.index)

    def index(self):
        return "Hello, my name is " + self.name


# app = MyApp('OOBottle')
# app.run(host='localhost', port=8080)


class BottleGUI(Bottle):
    def __init__(self, name):
        super(BottleGUI, self).__init__()
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.root_dir = os.path.abspath('apps' + os.sep + 'resources' + os.sep + 'web_template')
        self.images_root = os.path.abspath(self.root_dir + os.sep + 'img')
        self.fonts_root = os.path.abspath(self.root_dir + os.sep + 'fonts')
        self.css_root = os.path.abspath(self.root_dir + os.sep + 'css')
        print('root dir: ', self.root_dir)
        self.route('/', callback=self.root)
        self.post('/', callback=self.accept_post)
        self.route
        
        # @route('/<filename>')
        # def server_static(self, filename):
        #     return static_file(filename, root=self.root_dir)
        #
        # @route('/css/<filename>')
        # def server_static(self, filename):
        #     return static_file(filename, root=self.css_root)
        #
        # @route('/img/<filename>')
        # def server_static(self, filename):
        #     return static_file(filename, root=self.images_root)
        #
        # @route('/fonts/<filename>')
        # def server_static(self, filename):
        
    def get_form_values(self):
        # args = dict()
        args = request.forms.dict
        if 'file_upload' in request.files.dict.keys():
            print("FILE UPLOAD FOUND!")
            filename = str(request.files.dict['file_upload'][0]['filename'])
            data = request.files.file_upload
            if data and data.file:
                raw = data.file.read()  # This is dangerous for big files
                filename = data.filename
                
        print(args)
        print("\n\n")
        for key, value in args.copy().items():
            if len(value[0]) <= 1:
                print(key, " empty: ", value[0])
                del args[key]
        # print(args)
        print("Arguments: ")
        print(json.dumps(args, indent=4, sort_keys=True))
        return args
    
    def determine_cmdline(self, args):
        command = str()
        arg_mapping = {
            "url_input": ' -u ',
            "file_upload": "-f",
            "type": {
                'status': '-status',
                'scrape': '-scrape',
                'verify': '-verify'
                },
            "excel_enable": "--excel",
            # "advanced_enable": {"toggle": True, "dependents": ["base_url_enable", "base_url"]},
            # "base_url_enable": "",
            "base_url": " -base ",
            # "limit_domain_enable": "",
            "limit_domain": "--limit",
            # "exclude_domain_enable": "",
            "exclude_domain": "--exclude",
            "auth_enable": "",
            "username": "--user",
            "password": "--password",
            "database": "-db"}
        
        url_list = list()
        if 'url_input' in args.keys():
            items = args['url_input'][0].split("\r\n")
            for item in items:
                url_list.append(item)
        
        if 'file_upload' in args.keys():
            data = request.files.file_upload
            if data and data.file:
                raw = data.file.read()  # This is dangerous for big files
                filename = data.filename
                print(filename)
            # command += arg_mapping['url_input'] + str()
        print(command)
        
    def execute(self, args, command):
        if args["Script"] and args["Browser"]:
            print("Running: ", str(command))
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            print(process.returncode)
    
    @get('/')
    def root(self):
        print("Running Canary GUI")
        print("Launch http://localhost:8080 in a webbrowser")
        return static_file('index.html', root=self.root_dir)

    @route('/<filename>')
    def server_static(self, filename):
        return static_file(filename, root=self.root_dir)
    
    @route('/css/<filename>')
    def server_static(self, filename):
        return static_file(filename, root=self.css_root)
    
    @route('/img/<filename>')
    def server_static(self, filename):
        return static_file(filename, root=self.images_root)
    
    @route('/fonts/<filename>')
    def server_static(self, filename):
        return static_file(filename, root=self.fonts_root)
    
    @post('/')
    def accept_post(self):
        args = self.get_form_values()
        self.determine_cmdline(args)
        # execute(args, command)
        # print(json.dumps(args, indent=4, sort_keys=True))
        return static_file('index.html', root=self.root_dir)


if __name__ == '__main__':
    # GUI = BottleGUI()
    queue = Queue()
    try:
        webbrowser.open_new('http://localhost:8080')
    except:
        pass
    try:
        # if 'start' not in sys.argv:
        # 	sys.argv.append('start')
        # daemon_run(host='localhost', port='8080', logfile='weblog.log')
        # run(host='localhost', port=8080, quiet=True)
        GUI = BottleGUI('Canary')
        GUI.run(host='localhost', port=8080, quiet=True)
    except Exception as e:
        print(e)
        print("Open http://localhost:8080 in a browser to view GUI")
        pass
    
   



