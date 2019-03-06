#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains some utility functions used by the
'What is happening' skill.
"""

from hermes_python.ontology.dialogue import InstantTimeValue, TimeIntervalValue


def get_calendar(intent_message, default_calendar):
    """
    Get the calendar from an intent.

    This returns the default calendar if the intent doesn't have a calendar.

    Parameter intent_message: the intent message
    Parameter default_calendar: the default calendar
    """

    # The user has specified a calendar file in his voice command
    if intent_message.slots.calendar_file:
        calendar = str(intent_message.slots.calendar_file.first().value)
    else:
        # The user has specified a default calendar file in the
        # default_calendar parameter
        if default_calendar:
            calendar = default_calendar
        else:
            calendar = ""

    return calendar


def get_date(intent_message):
    """
    Get the date from an intent.

    The resulting date has the format yyyymmdd. If the intent message doesn't
    contain a date, this method returns an empty string.

    Parameter intent_message: the intent message
    """

    # The user has specified a date in his voice command
    if intent_message.slots.calendar_date:
        date = intent_message.slots.calendar_date.first()
        if isinstance(date, InstantTimeValue):
            # If the user specifies a date, return it in the format yyyymmdd.
            date = str(date.value[:10].replace("-", ""))
        elif isinstance(date, TimeIntervalValue):
            # If the user specifies a time interval, return the start date
            # in the format yyyymmdd.
            date = str(date.from_date[:10].replace("-", ""))
    else:
        date = ""

    return date
