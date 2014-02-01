#!/usr/bin/env python

import csv, sys, os
from billing import BillingReportData, StatList

def main(files):
    report = BillingReportData()
    for export_file in files:
        database = csv.reader(open(file), delimiter=report.delim)
        records = []
        for record in database:
            records.append(record)
        stats = StatList(records, report.name_field)
        if stats.device_name == report.color_device:
            output_file_name = 'color ' + report.output_name
            charge_amount = report.color_charge
            countfield = report.color_countfield
        elif stats.device_name == report.bw_device:
            output_file_name = 'bw ' + report.output_name
            charge_amount = report.bw_charge
            countfield = report.bw_countfield
        else:
            sys.exit('Unknown device. Cannot process file.')
        output_file = open(output_file_name, 'w')
        output = csv.writer(output_file, delimiter=report.delim, lineterminator=report.term)
        for stat in stats.records:
            if not stat.getname():
                next
            elif stat.getname() in report.excluded_names:
                next
            elif stat.charge(charge_amount, countfield) <= report.maxcharge:
                next
            elif stat.count(countfield) == 0:
                next
            else:
                row = [stat.lastname(case=report.case),
                       stat.firstname(case=report.case, words=report.fname_amount),
                       stat.count(countfield),
                       stat.charge(charge_amount, countfield)
                       ]
                output.writerow(row)
        output_file.close()
    
if __name__ == '__main__':
	files = sys.argv[1:]
	if len(files) >= 1:
		main(files)
	else:
		sys.exit('You must specify at least one file to process.')
