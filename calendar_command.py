#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains a class to interface with the Unix calendar command"""

import subprocess
from os import listdir
from os.path import isfile, join

CALENDAR_COMMAND = ["calendar", "-A", "0"]


class CalendarCommand(object):
    """This class interfaces with the calendar command"""

    def __init__(self, calendar_directory):
        self.calendar_directory = calendar_directory

    def available_calendars(self):
        """
        Return a list of the available calendars.
        """

        calendars = [filename for filename in listdir(self.calendar_directory)
                     if isfile(join(self.calendar_directory, filename))]

        # Filter the calendar.judaic.2018 files and so on,
        # because we use the symbolic link calendar.judaic
        calendars = [calendar for calendar in calendars
                     if not calendar.startswith("calendar.judaic.")]
        return sorted([calendar[9:] for calendar in calendars])

    def is_valid_calendar(self, calendar):
        """
        Find out if a calendar is valid.

        An empty calendar is also valid.

        Parameter calendar: name of the calendar (without the prefix
        `calendar.` of the file).
        """

        return calendar in self.available_calendars() or calendar == ""

    def events(self, calendar="", date=""):
        """
        Get the list of events in a specific calendar and on a specific date.

        Parameter calendar: name of the calendar (without the prefix
        `calendar.` of the file).
        Parameter date: date in the format yyyymmdd.
        """
        command = list(CALENDAR_COMMAND)

        if calendar:
            command.extend(["-f",
                            join(self.calendar_directory,
                                 "calendar.{}".format(calendar))])

        if date:
            command.extend(["-t", "{}".format(date)])

        calendar_output = subprocess.check_output(command).decode("utf-8")
        # Split the lines and filter the empty lines.
        lines = [line for line in calendar_output.split("\n") if line]
        lines_copy = list(lines)
        index = 0
        for event in lines:
            if event.startswith("\t") or event.startswith(" "):
                # This line is a continuation of the previous one.
                lines_copy[index - 1] += event
            else:
                lines_copy[index] = event
                index += 1

        # Substitute multiple whitespaces by one space.
        events = [' '.join(event.split()) for event in lines_copy[:index]]

        # Replace '&' by 'and' because PicoTTS pronounces it as 'ampersand'.
        # See https://github.com/snipsco/snips-issues/issues/85
        events = [event.replace('&', 'and') for event in events]

        # Create a sentence with the date and a new sentence with the description.
        # Strip the asterisk (*) after a date. This means the date changes from year to year.
        return [event[:6] + '.' + event[6:].strip("*") for event in events]
