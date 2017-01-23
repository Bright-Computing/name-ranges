#!/usr/bin/python3

import os
import re
from jinja2 import Template


class Report(object):
    def __init__(self, filename, path):
        self.name = filename
        self.path = path

class ReportBuilder(object):
    def __init__(self, template_filename, report_directory):
        self.reports = []
        self._build_reports(report_directory)

        template_file = open(template_filename)
        self.template = Template(template_file.read())


    def _build_reports(self, report_directory):
        for current_filename in os.listdir(report_directory):
            match = re.match("(.*)\.html$", current_filename)

            if match and current_filename != "index.html":
                self.reports.append(Report(match.group(1), "%s/%s" % (report_directory, current_filename)))

    def generate(self):
        print(self.template.render(reports=self.reports))
        pass


if __name__ == "__main__":
    report_builder = ReportBuilder("report.template", ".")

    report_builder.generate()
