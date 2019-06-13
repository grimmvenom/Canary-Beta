"""
Summary:
    Python Script to run webform via a webservice to run as the GUI of the Ivan Application
    
Author:
    grimmvenom <grimmvenom@gmail.com>
    

Helpful CSS Tool:
https://github.com/uncss/uncss

"""

import os, sys, json
from bottle import route, post, get, run, request, static_file
from multiprocessing import Process, Queue
import subprocess, webbrowser
from enum import Enum

current_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_dir)
root_dir = os.path.abspath('resources' + os.sep + 'web_template')
images_root = os.path.abspath(root_dir + os.sep + 'img')
fonts_root = os.path.abspath(root_dir + os.sep + 'fonts')
css_root = os.path.abspath(root_dir + os.sep + 'css')
print('root dir: ', root_dir)


def get_form_values():
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


def determine_cmdline(args):
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
    
    
def execute(args, command):
    if args["Script"] and args["Browser"]:
        print("Running: ", str(command))
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print(process.returncode)


@get('/')
def root():
    print("Running Canary GUI")
    print("Launch http://localhost:8080 in a webbrowser")
    return static_file('index.html', root=root_dir)


@route('/<filename>')
def server_static(filename):
    return static_file(filename, root=root_dir)


@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root=css_root)


@route('/img/<filename>')
def server_static(filename):
    return static_file(filename, root=images_root)


@route('/fonts/<filename>')
def server_static(filename):
    return static_file(filename, root=fonts_root)


@post('/')
def accept_post():
    args = get_form_values()
    determine_cmdline(args)
    # execute(args, command)
    # print(json.dumps(args, indent=4, sort_keys=True))
    return static_file('index.html', root=root_dir)


if __name__ == '__main__':
    queue = Queue()
    try:
        webbrowser.open_new('http://localhost:8080')
    except:
        pass
    try:
        # if 'start' not in sys.argv:
        # 	sys.argv.append('start')
        # daemon_run(host='localhost', port='8080', logfile='weblog.log')
        run(host='localhost', port=8080, quiet=True)
    except Exception as e:
        print(e)
        print("Open http://localhost:8080 in a browser to view GUI")
        pass

