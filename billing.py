#!/usr/bin/env python

import string

class BillingReportData:
    """Contains metadata and functions related to the printer billing report"""
    def __init__(self):
        # a list of people I don't want to include in my final report.
		# Names have been changed for example purposes
        self.excluded_names = ['Jon Bon Jovi',
                               'Richie Sambora',
                               'Tico Torres',
                               'David Bryan',
                               'Alec John Such',
                               ]
        self.fname_amount = 2
        self.name_field = 'Name'
        self.case = 'uppercase'
        self.color_device = 'RICOH Aficio SP C811DN'
        self.color_countfield = 'Total Printouts'
        self.color_charge = 0.43
        self.bw_device = 'RICOH Aficio MP 5500'
        self.bw_countfield = 'Total Printouts: Black & White(Copier/Document Server)'
        self.bw_charge = 0.06
        self.output_name = 'report.csv'
        self.delim = ","
        self.term = '\n'
        self.maxcharge = 5.00

class StatRecord:
    """the individual records in a statlist"""
    def __init__(self, record_dict, namefield):
        self.namefield = namefield
        self.record = record_dict
    def getname(self, case=None, strip_initials=None):
        """Return a formatted version of the name without braces,
        optionally stripping initials or titles or changing it's case"""
        name = string.strip(self.record[self.namefield], '[]')
        if strip_initials:
            # get rid of titles or initials
            temp = []
            for index in range(len(name)):
                if len(name[index]) > 2: temp.append(name[index])
            name = string.join(temp)
        if not case: return name
        elif case is 'uppercase': return name.upper()
        elif case is 'lowercase': return s.lower()
        elif case is 'titlecase': return string.capwords(name)
        else: return name
    def firstname(self, case=None, strip_initials=None, words=1):
        name = self.getname(case, strip_initials)
        name = name.split()
        # return the first name taking into account that
        # some people have 2 or more words in their first name
        if len(name) > words:
            return string.join(name[:words])
        else:
            return name[0]
    def lastname(self, case=None, strip_initials=None, words=1):
        name = self.getname(case, strip_initials)
        name = name.split()
        # return the last name taking into account that
        # some people have 2 or more words in their last name
        return name[-words]
    def count(self, countfield):
        return int(self.record[countfield])
    def charge(self, amount, countfield):
        return int(self.record[countfield]) * amount
    def getfields(self):
        return self.record.keys()
    
class StatList:
    """A class that parses a csv User Statistics List
    file from a copy machine and contains instances of StatRecords"""
    def __init__(self, data, namefield):
        # get file metadata
        self.file_type = data[0][0].lstrip('#')
        self.format_version = data[1][0].split(':')[-1]
        self.date_obtained = data[2][0].split(':')[-3:] # it gets split into several different items
        self.device_name = data[3][0].split(':')[-1]
        self.address = data[4][0].split(':')[-1]
        # Get the headers
        self.headers = data[6]
        self.headers[0] = self.headers[0].lstrip('#') # get rid of pesky hash symbol on first header
        # delete all the header info and metadata from the original list
        del(data[0:7])
        # pass along each record as a dict with the header as a key to a StatRecord object
        self.records = []
        for record in data:
            dictionary = {}
            for index in range(len(record)):
                dictionary[self.headers[index]] = record[index] # match up headers with data fields
            self.records.append(StatRecord(dictionary, namefield))
