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
Trace Generator Model
"""
__version__ = "0.1"
__author__ = "Albert De La Fuente"


import collections


class BaseTraceGenerator(object):
    def __init__(self):
        self.counter = 0

    def __iter__(self):
        return self

    # Python 3 compatibility
    def __next__(self):
        self.counter += 1
        return self.next()

    def count(self):
        return self.counter


class FileTraceGenerator(BaseTraceGenerator):
    def __init__(self, trace_file):
        super(FileTraceGenerator, self).__init__()
        self.trace_file = trace_file
#        with open(self.trace_file) as f:
#            self.lines = f.readlines()
#            self.cpu = map(int, self.lines)
        self.file_handler = open(self.trace_file)
        self.values = map(int, self.file_handler.readlines())
        self.file_handler.close()
        self.counter = 0
        self.index = 0
        self.reverse = False
        self.cycle = False

    def next(self):
        try:
            result = self.values[self.index]
            self.index += 1
            if self.cycle:
                self.index = self.cycle % len(self.values)
            return result
        except:
            raise StopIteration()

    def set_reverse(self):
        self.reverse = True
        self.values += reversed(self.values)

    def set_cycle(self):
        self.cycle = True


class FunctionTraceGenerator(BaseTraceGenerator):
    def __init__(self, function, *args, **kwargs):
        super(FunctionTraceGenerator, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.counter = 0

    def next(self):
        return self.function(*self.args, **self.kwargs)

if __name__ == "__main__":
    t = FileTraceGenerator('../planetlab-workload-traces/20110303/vn5_cse_wustl_edu_uw_onesarm')
    print('{}:{}'.format(t.count(), t.next()))
    print('{}:{}'.format(t.count(), t.next()))
    print('{}:{}'.format(t.count(), t.next()))
    print('{}:{}'.format(t.count(), t.next()))
    print('{}:{}'.format(t.count(), t.next()))

    import math
    t = FunctionTraceGenerator(math.exp, [2, 3, 4, 5, 6])
    print('{}:{}'.format(t.count(), t.next()))
    print('{}:{}'.format(t.count(), t.next()))
    print('{}:{}'.format(t.count(), t.next()))
    print('{}:{}'.format(t.count(), t.next()))
    print('{}:{}'.format(t.count(), t.next()))
