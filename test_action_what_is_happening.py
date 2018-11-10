#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""This module tests the What is happening Snips skill."""

from unittest import TestCase, main
from hermes_python import ontology
import tools_what_is_happening as tools
import calendar_command as cal


class ListWithFirst(list):
    """"Helper class to add the first() method to a list."""
    def first(self):
        """Return the first element of the ListWithFirst object."""
        return self[0]


class TestCalendarCommand(TestCase):
    """Test the CalendarCommand class."""

    def setUp(self):
        """Create the CalendarCommand object to test."""
        self.command = cal.CalendarCommand("/usr/share/calendar")

    def test_is_valid_calendar(self):
        """Test the is_valid_calendar method from CalendarCommand."""
        self.assertTrue(self.command.is_valid_calendar("computer"))
        self.assertTrue(self.command.is_valid_calendar("usholiday"))
        self.assertTrue(self.command.is_valid_calendar("judaic"))
        self.assertFalse(self.command.is_valid_calendar("judaic.2021"))
        self.assertFalse(self.command.is_valid_calendar("foobar"))

    def test_empty_events(self):
        """Test the events method from CalendarCommand with no events."""
        events = self.command.events("computer", "20181109")
        # $ calendar -A 0 -f /usr/share/calendar/calendar.computers -t 20181109
        # $
        self.assertEqual(len(events), 0)

    def test_multiline_events(self):
        """
        Test the events method from CalendarCommand with multi-line events.
        """
        events = self.command.events("", "20181030")
        # $ calendar -A 0 -t 20181030
        # Oct 30  John Adams, 2nd President of the United States, born Quincy,
        #                 Massachusetts 1735.
        # Oct 30  Orson Welles' "War of the Worlds" broadcast, 1938
        # Oct 30  Grace Slick is born in Chicago, 1939
        # Oct 30  Ubuntu 8.10 (Intrepid Ibex) released, 2008
        self.assertEqual(len(events), 4)
        self.assertEqual(events[0],
                         'Oct 30. John Adams, 2nd President of the United'
                         ' States,'
                         ' born Quincy, Massachusetts 1735.')
        self.assertEqual(events[1],
                         'Oct 30. Orson Welles\' "War of the Worlds"'
                         ' broadcast, 1938')
        self.assertEqual(events[2],
                         'Oct 30. Grace Slick is born in Chicago, 1939')
        self.assertEqual(events[3],
                         'Oct 30. Ubuntu 8.10 (Intrepid Ibex) released, 2008')


class TestTools(TestCase):
    """Test the helper functions of the What is happening skill."""

    def test_get_calendar_from_intent_without_calendar(self):
        """
        Test whether the function get_calendar returns
        the default calendar if the intent doesn't have a calendar.
        """
        slot_map = ontology.SlotMap({})
        intent = ontology.IntentClassifierResult("koan:Event", 1.0)
        intent_message = ontology.IntentMessage("session_id",
                                                "custom_data",
                                                "site_id",
                                                "what is happening today",
                                                intent, slot_map)

        # No calendar in intent message, no default calendar
        # -> no calendar
        self.assertEqual(tools.get_calendar(intent_message, ""), "")
        # No calendar in intent message, default calendar thai
        # -> default calendar thai
        self.assertEqual(tools.get_calendar(intent_message, "thai"), "thai")

    def test_get_calendar_from_intent_with_calendar(self):
        """
        Test whether the function get_calendar returns
        the calendar in the intent, even if a default calendar is set.
        """
        calendar_file_value = ontology.CustomValue("computer")
        slot_map = ontology.SlotMap({"calendar_file":
                                     ListWithFirst([calendar_file_value])})
        intent = ontology.IntentClassifierResult("koan:Event", 1.0)
        intent_message = ontology.IntentMessage("session_id",
                                                "custom_data",
                                                "site_id",
                                                "what is happening today in"
                                                " computers",
                                                intent, slot_map)

        # Calendar computer in intent message, no default calendar
        # -> calendar computer
        self.assertEqual(tools.get_calendar(intent_message, ""), "computer")
        # Calendar computer in intent message, default calendar thai
        # -> calendar computer
        self.assertEqual(tools.get_calendar(intent_message, "thai"),
                         "computer")

    def test_get_date_from_intent_with_time(self):
        """
        Test whether the function get_date returns
        the data in the intent if it contains an instant time value.
        """
        calendar_date_value = ontology.InstantTimeValue("2018-10-31 00:00:00"
                                                        " +01:00",
                                                        "grain",
                                                        "precision")
        slot_map = ontology.SlotMap({"calendar_date":
                                     ListWithFirst([calendar_date_value])})
        intent = ontology.IntentClassifierResult("koan:Event", 1.0)
        intent_message = ontology.IntentMessage("session_id",
                                                "custom_data",
                                                "site_id",
                                                "what is happening today",
                                                intent, slot_map)

        self.assertEqual(tools.get_date(intent_message), "20181031")

    def test_get_date_from_intent_with_interval(self):
        """
        Test whether the function get_date returns
        the start date in the intent if it contains a time interval.
        """
        calendar_date_value = ontology.TimeIntervalValue("2018-11-05 18:00:00"
                                                         " +01:00",
                                                         "2018-11-06 00:00:00"
                                                         " +01:00")
        slot_map = ontology.SlotMap({"calendar_date":
                                     ListWithFirst([calendar_date_value])})
        intent = ontology.IntentClassifierResult("koan:Event", 1.0)
        intent_message = ontology.IntentMessage("session_id",
                                                "custom_data",
                                                "site_id",
                                                "what is happening this night",
                                                intent, slot_map)

        self.assertEqual(tools.get_date(intent_message), "20181105")

    def test_get_date_from_intent_without_date(self):
        """
        Test whether the function get_date returns an empty string
        if an intent doesn't contain a date.
        """
        slot_map = ontology.SlotMap({})
        intent = ontology.IntentClassifierResult("koan:Event", 1.0)
        intent_message = ontology.IntentMessage("session_id",
                                                "custom_data",
                                                "site_id",
                                                "what is happening",
                                                intent, slot_map)

        self.assertEqual(tools.get_date(intent_message), "")


if __name__ == '__main__':
    main()
