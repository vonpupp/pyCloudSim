#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:
#
# Copyright 2013 Albert De La Fuente
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
CSV Loader
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


import csv
import os

def dict_float_cast(l):
    result = {}
    for item in l:
        try:
            result[item] = float(l[item])
        except:
            result[item] = str(l[item])
    return result

class CSVLoader():
    def __init__(self, fname):
        self.fname = fname
        self.data = []
        self.summary_list = {}
        self.load_file()

    def load_file(self):
        self.file_in = open(self.fname, mode='r')
        self.reader = csv.DictReader(self.file_in, delimiter='\t', quoting=csv.QUOTE_NONE)
        self.data.append([])
        simulation_counter = len(self.data)-1
        self.data[simulation_counter] = []
        for row in self.reader:
            float_row = dict_float_cast(row)
            self.data[simulation_counter] += float_row
#        fields = self.reader.fieldnames
#        data = {}
#        for line in self.reader:
#            for field in fields:
#                d = data.get(field)
#                if not d:
#                    try:
#                        data[field] = [float(line[field])]
#                    except:
#                        data[field] = [str(line[field])]
#                else:
#                    try:
#                        data[field].append(float(line[field]))
#                    except:
#                        data[field].append(str(line[field]))
        #self.data += [buffer]
        #self.simulation_counter += 1
        #print buffer
        self.file_in.close()