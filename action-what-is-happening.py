#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This module contains a Snips skill to tell you what is happening
this or another day.
"""

import random
from hermes_python.hermes import Hermes
from snips_tools import SnipsConfigParser
import tools_what_is_happening as tools
import calendar_command as cal

CONFIG_INI = "config.ini"

# Result sentences and their parts:
DEFAULT = "default"
EMPTY = "empty"
AND = " and "
RESULT_EVENT_NOTHING = "There's nothing in the {} calendar."
RESULT_INVALID_CALENDAR = "{} is an invalid calendar. Please use another one."
RESULT_DEFAULT_CALENDAR = "My default calendar is {}."
RESULT_LIST = "This is the list of calendars you can choose: "
RESULT_RESET = "I have reset your default calendar."
RESULT_DEFAULT_CHANGED = "I have changed your default calendar to {}."

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


class WhatIsHappening(object):
    """This skill tells you what is happening this or another day."""

    def __init__(self):
        """Initialize the skill."""
        # Try to read the configuration.
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
            calendar_directory = self.config["secret"]["calendar_location"]
        except (IOError, KeyError):
            self.config = None

        self.calendar_command = cal.CalendarCommand(calendar_directory)

        # start listening to MQTT
        self.start_blocking()

    def event_callback(self, hermes, intent_message):
        """Callback for intent Event"""

        calendar = tools.get_calendar(intent_message,
                                      self.config["secret"]["default_calendar"])

        if self.calendar_command.is_valid_calendar(calendar):
            date = tools.get_date(intent_message)
            events = self.calendar_command.events(calendar, date)
            if events:
                result_sentence = random.choice(events)
            else:
                if not calendar:
                    calendar = DEFAULT
                result_sentence = RESULT_EVENT_NOTHING.format(calendar)

        else:
            result_sentence = RESULT_INVALID_CALENDAR.format(calendar)

        hermes.publish_end_session(intent_message.session_id, result_sentence)

    def what_is_default_calendar_callback(self, hermes, intent_message):
        """Callback for intent WhatIsDefaultCalendar"""

        calendar = self.config["secret"]["default_calendar"]

        if not calendar:
            calendar = EMPTY

        hermes.publish_end_session(intent_message.session_id,
                                   RESULT_DEFAULT_CALENDAR.format(calendar))

    def list_of_calendars_callback(self, hermes, intent_message):
        """Callback for intent ListOfCalendars"""
        calendars = self.calendar_command.available_calendars()

        last = calendars.pop()
        result_sentence = RESULT_LIST + ", ".join(calendars) + AND + last
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    def change_default_calendar_callback(self, hermes, intent_message):
        """Callback for intent ChangeDefaultCalendar"""

        calendar = str(intent_message.slots.calendar_file.first().value)
        if self.calendar_command.is_valid_calendar(calendar):
            self.config["secret"]["default_calendar"] = calendar

            SnipsConfigParser.write_configuration_file(CONFIG_INI, self.config)
            result_sentence = RESULT_DEFAULT_CHANGED.format(calendar)

        else:
            result_sentence = RESULT_INVALID_CALENDAR.format(calendar)

        hermes.publish_end_session(intent_message.session_id, result_sentence)

    def reset_default_calendar_callback(self, hermes, intent_message):
        """Callback for intent ResetDefaultCalendar"""

        self.config["secret"]["default_calendar"] = ""

        SnipsConfigParser.write_configuration_file(CONFIG_INI, self.config)
        result_sentence = RESULT_RESET

        hermes.publish_end_session(intent_message.session_id, result_sentence)

    def master_callback(self, hermes, intent_message):
        """
        Master callback function, triggered everytime an intent is recognized.
        """
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'koan:Event':
            self.event_callback(hermes, intent_message)
        if coming_intent == 'koan:WhatIsDefaultCalendar':
            self.what_is_default_calendar_callback(hermes, intent_message)
        if coming_intent == 'koan:ChangeDefaultCalendar':
            self.change_default_calendar_callback(hermes, intent_message)
        if coming_intent == 'koan:ResetDefaultCalendar':
            self.reset_default_calendar_callback(hermes, intent_message)
        if coming_intent == 'koan:ListOfCalendars':
            self.list_of_calendars_callback(hermes, intent_message)

    def start_blocking(self):
        """Register callback function and start MQTT"""
        with Hermes(MQTT_ADDR) as hermes:
            hermes.subscribe_intents(self.master_callback).start()


if __name__ == "__main__":
    WhatIsHappening()
