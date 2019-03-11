#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the result sentences and intents for the English version
of the What is happening skill.
"""

# Result sentences and their parts:
DEFAULT = "default"
EMPTY = "empty"
AND = "and"
RESULT_EVENT_NOTHING = "There's nothing in the {} calendar."
RESULT_INVALID_CALENDAR = "{} is an invalid calendar. Please use another one."
RESULT_DEFAULT_CALENDAR = "My default calendar is {}."
RESULT_LIST = "This is the list of calendars you can choose: "
RESULT_RESET = "I have reset your default calendar."
RESULT_DEFAULT_CHANGED = "I have changed your default calendar to {}."

# Intents
INTENT_EVENT = 'koan:Event'
INTENT_WHAT_IS_DEFAULT_CALENDAR = 'koan:WhatIsDefaultCalendar'
INTENT_CHANGE_DEFAULT_CALENDAR = 'koan:ChangeDefaultCalendar'
INTENT_RESET_DEFAULT_CALENDAR = 'koan:ResetDefaultCalendar'
INTENT_LIST_CALENDARS = 'koan:ListOfCalendars'
