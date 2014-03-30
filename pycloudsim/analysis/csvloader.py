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
