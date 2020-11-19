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
cwd = os.getcwd()
path = cwd + '/roles'
for dirpath, dirname, filename in os.walk(path):
    for fname in filename:
        path = os.path.join(dirpath, fname)
        updated_path = path.replace("\\", "/")
        if fname == 'oneview_config.json':
            config_file = open(path, "r")
            json_object = json.load(config_file)
            config_file.close()
            json_object["ip"] = "<oneview_ip>"
            json_object["credentials"]["userName"] = "<username>"
            json_object["credentials"]["password"] = "<password>"
            json_object["credentials"]["image_streamer_ip"] = "<image_streamer_ip>"
            config_file = open(path, "w")
            json.dump(json_object, config_file, indent=2)
        if updated_path.split("/")[-2] == 'defaults' and fname == 'main.yml':
            with open(path, 'r') as stream:
                content = yaml.load(stream)
            for k, v in content.items():
                if (str(v).count('.')) >= 3 or str(k).find("username") != -1 or str(k).find("password") != -1:
                    content[k] = "<" + k + "_ip>"
            with open(path, "w") as f:
                yaml.dump(content, f)
