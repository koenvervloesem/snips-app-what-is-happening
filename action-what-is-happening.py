#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains a Snips skill to tell you what is happening
this or another day.
"""

import importlib
import json
import random
from hermes_python.hermes import Hermes
from snips_tools import SnipsConfigParser
import tools_what_is_happening as tools
import calendar_command as cal
import toml

CONFIG_INI = "config.ini"


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

        # Use the assistant's language.
        with open("/usr/share/snips/assistant/assistant.json") as json_file:
            language = json.load(json_file)["language"]

        self.i18n = importlib.import_module("translations." + language)

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
                    calendar = self.i18n.DEFAULT
                result_sentence = self.i18n.RESULT_EVENT_NOTHING.format(calendar)

        else:
            result_sentence = self.i18n.RESULT_INVALID_CALENDAR.format(calendar)

        hermes.publish_end_session(intent_message.session_id, result_sentence)

    def what_is_default_calendar_callback(self, hermes, intent_message):
        """Callback for intent WhatIsDefaultCalendar"""

        calendar = self.config["secret"]["default_calendar"]

        if not calendar:
            calendar = self.i18n.EMPTY

        hermes.publish_end_session(intent_message.session_id,
                                   self.i18n.RESULT_DEFAULT_CALENDAR.format(calendar))

    def list_of_calendars_callback(self, hermes, intent_message):
        """Callback for intent ListOfCalendars"""
        calendars = self.calendar_command.available_calendars()

        last = calendars.pop()
        result_sentence = self.i18n.RESULT_LIST + ", ".join(calendars) + self.i18n.AND + last
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    def change_default_calendar_callback(self, hermes, intent_message):
        """Callback for intent ChangeDefaultCalendar"""

        calendar = str(intent_message.slots.calendar_file.first().value)
        if self.calendar_command.is_valid_calendar(calendar):
            self.config["secret"]["default_calendar"] = calendar

            SnipsConfigParser.write_configuration_file(CONFIG_INI, self.config)
            result_sentence = self.i18n.RESULT_DEFAULT_CHANGED.format(calendar)

        else:
            result_sentence = self.i18n.RESULT_INVALID_CALENDAR.format(calendar)

        hermes.publish_end_session(intent_message.session_id, result_sentence)

    def reset_default_calendar_callback(self, hermes, intent_message):
        """Callback for intent ResetDefaultCalendar"""

        self.config["secret"]["default_calendar"] = ""

        SnipsConfigParser.write_configuration_file(CONFIG_INI, self.config)
        result_sentence = self.i18n.RESULT_RESET

        hermes.publish_end_session(intent_message.session_id, result_sentence)

    def master_callback(self, hermes, intent_message):
        """
        Master callback function, triggered everytime an intent is recognized.
        """
        coming_intent = intent_message.intent.intent_name
        if coming_intent == self.i18n.INTENT_EVENT:
            self.event_callback(hermes, intent_message)
        if coming_intent == self.i18n.INTENT_WHAT_IS_DEFAULT_CALENDAR:
            self.what_is_default_calendar_callback(hermes, intent_message)
        if coming_intent == self.i18n.INTENT_CHANGE_DEFAULT_CALENDAR:
            self.change_default_calendar_callback(hermes, intent_message)
        if coming_intent == self.i18n.INTENT_RESET_DEFAULT_CALENDAR:
            self.reset_default_calendar_callback(hermes, intent_message)
        if coming_intent == self.i18n.INTENT_LIST_CALENDARS:
            self.list_of_calendars_callback(hermes, intent_message)

    def start_blocking(self):
        """Register callback function and start MQTT"""
        # Get the MQTT host and port from /etc/snips.toml.
        try:
            mqtt_addr = toml.load('/etc/snips.toml')['snips-common']['mqtt']
        except KeyError:
            # If the mqtt key doesn't exist, use the default value.
            mqtt_addr = 'localhost:1883'

        with Hermes(mqtt_addr) as hermes:
            hermes.subscribe_intents(self.master_callback).start()


if __name__ == "__main__":
    WhatIsHappening()
