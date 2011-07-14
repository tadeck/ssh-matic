#!/usr/bin/env python

'''
SSH-Matic 0.1.1 alpha

Simple update script aimed connecting with SSH to each server on the list and
invoking 'git pull' in public_html subdirectory, then displaying results.
Needs some polishing.
Author: https://github.com/tadeck/

HOW TO USE IT
To use it, replace given server with your owns and update the path to private key.
Feel free to fork it on https://github.com/tadeck/ssh-matic and make pull request

READ MORE
More details, updated version, howto and bug tracker accessible on:
https://github.com/tadeck/ssh-matic
'''

# location of this script
import sys
current_dir = sys.path[0]

data = eval(open(current_dir+'/settings.dat', 'r').read())

environments = data.get('environments')
defaults = data.get('defaults')

# some helpers used only for displaing colored output in Linux console
def success(text):
    return '\033[0;32m' + text + '\033[0m'
def failure(text):
    return '\033[0;31m' + text + '\033[0m'
def warning(text):
    return '\033[0;33m' + text + '\033[0m'
def bold(text):
    return '\033[1;37m' + text + '\033[0m'

import ssh
for environment in environments:
    # Determining variables for current environment:
    curr = {}
    for option_name in ['name','host','username','private_key','command','indent']:
        curr[option_name] = environment.get(option_name, defaults.get(option_name))
    
    print '[Connecting to ' + bold(curr['name']) + ']'
    print
    
    server = ssh.Connection(host=curr['host'], username=curr['username'], private_key=curr['private_key'])
    result = server.execute(curr['command'])

    # Cleanup lines
    result = [line.strip(' \n\t') for line in result]

    # Display results
    if result.count('Already up-to-date.') > 0 and len(result) == 1:
        print curr['indent'] + success('(up-to-date)')
        print
    else:
        for line in result:
            print curr['indent'] + warning(line)
        print

    server.close()

# ended updating environments
