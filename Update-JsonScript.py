##############################################################################
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
#
# File Name: Update-JsonScript.py
# VERSION 1.0
# Usage: python Update-JsonScript.py
#
# This script can be used independently to remove any sensitive information
# provided in config files.
#
##############################################################################
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
##############################################################################
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import yaml
import json
import git
import shutil
cwd = os.getcwd()
path = cwd + '/roles'
#path = "C:/Users/chebrolb/Desktop/code/oneview-ansible-collections/oneview-ansible-collection/roles"
change_required = False
change_required_in_defaults = False
paths = []
paths_for_defaults = []
branchName = 'update'

path = os.getcwd()
clone_dir = 'collections'
# Deleting the clone directory if exists
if os.path.exists(clone_dir):
    shutil.rmtree(clone_dir, ignore_errors=True)

repo = git.Repo.clone_from('https://github.com/HewlettPackard/oneview-ansible-collections',
                           path + os.path.sep + clone_dir)
os.chdir(path + os.path.sep + clone_dir)

def IsChangeRequired(json_object):
    if (json_object["ip"] != "<oneview_ip>" or json_object["credentials"]["userName"] != "<username>" 
        or json_object["credentials"]["password"] != "<password>" or 
        json_object["image_streamer_ip"] != "<image_streamer_ip>"):
        return True
    else:
        return False

def UpdateJsonScript(path):
    for dirpath, dirname, filename in os.walk(path):
        for fname in filename:
            path = os.path.join(dirpath, fname)
            updated_path = path.replace("\\", "/")
            if fname == 'oneview_config.json':
                config_file = open(path, "r")
                json_object = json.load(config_file)
                config_file.close()
                change_required = IsChangeRequired(json_object)
                if (change_required == True):
                    json_object["ip"] == "<ip>"
                    json_object["credentials"]["userName"] == "<username>" 
                    json_object["credentials"]["password"] == "<password>"
                    json_object["image_streamer_ip"] == "<image_streamer_ip>"
                    config_file = open(path, "w")
                    json.dump(json_object, config_file, indent = 2)
                    paths.append(path)
                else:
                    print("No change required in {}".format(str(path)))
            if updated_path.split("/")[-2] == 'defaults' and fname == 'main.yml':
                with open(path, 'r') as stream:
                    content = yaml.load(stream)
                for k,v in content.items():
                    if (str(v).count('.')) >= 3 or str(k).find("username") != -1 or str(k).find("password") != -1:
                        content[k] = "<" + k + ">"
                        paths_for_defaults.append(updated_path)
                    f = open(path, "w")
                    yaml.dump(content, f)
    return paths, paths_for_defaults
                              
if __name__ == '__main__':
    paths, paths_for_defaults = UpdateJsonScript(path)
    print(paths)
    print(paths_for_defaults)
    repo.git.add(A=True)
    repo.git.commit('-m', 'PR for config changes #pr',
                    author='chebroluharika@gmail.com') # to commit changes
    repo.git.push('--set-upstream', 'origin', branchName)
    repo.close()
    os.chdir(path) # Navigate to parent directory
    # Delete ruby directory as cleanup
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir, ignore_errors=True)
