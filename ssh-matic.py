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

environments = [
    {
        'name': 'Server1',
        'host': '123.123.123.123', # some IP or domain here
        'username': 'user' # username on the server no. 1
    },
    {
        'name': 'Server2',
        'host': '234.234.234.234', # some IP or domain here
        'username': 'master' # username on the server no. 2
    }
]

options = {
    'indent': '    ', # indent from remote messages
    'private_key': '/home/myself/.ssh/id_rsa', # location of private key
    'command': 'git --git-dir=public_html/.git pull'
}

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
    print '[Updating ' + bold(environment['name']) + ']'
    print
    server = ssh.Connection(host=environment['host'], username=environment['username'], private_key=options['private_key'])
    result = server.execute(options['command'])

    # Cleanup lines
    result = [line.strip(' \n\t') for line in result]

    # Display results
    if result.count('Already up-to-date.') > 0 and len(result) == 1:
        print options['indent'] + success('(up-to-date)')
        print
    else:
        for line in result:
            print options['indent'] + warning(line)
        print

    server.close()

# ended updating environments
