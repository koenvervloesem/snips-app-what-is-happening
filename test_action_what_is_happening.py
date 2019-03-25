#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module tests the What is happening Snips skill."""

from unittest import TestCase, main, skip
from hermes_python.ontology.dialogue import CustomValue, InstantTimeValue, \
     IntentClassifierResult, IntentMessage, SlotMap, TimeIntervalValue, \
     SlotsList, NluSlot
import tools_what_is_happening as tools
import calendar_command as cal


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

    def test_events_with_asterisk(self):
        """
        Test the events method from CalendarCommand with an asterisk after the date.
        """
        events = self.command.events("world", "20181121")
        # $ calendar -A 0 -f world -t 20181121
        # Nov 21  Announcement of 18 1/2 minute gap on Watergate tape, 1973
        # Nov 21* Day of Prayer and Repentance (Buss- und Bettag) in Federal Republic of Germany
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0],
                         'Nov 21. Announcement of 18 1/2 minute gap on Watergate tape, 1973')
        self.assertEqual(events[1],
                         'Nov 21. Day of Prayer and Repentance (Buss- und Bettag) in Federal Republic of Germany')

    def test_multiline_events(self):
        """
        Test the events method from CalendarCommand with multi-line events.
        """
        events = self.command.events("world", "20181030")
        # $ calendar -A 0 -f world -t 20181030
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

@skip("Doesn't work anymore, I should rewrite this test")
class TestTools(TestCase):
    """Test the helper functions of the What is happening skill."""

    def test_get_calendar_from_intent_without_calendar(self):
        """
        Test whether the function get_calendar returns
        the default calendar if the intent doesn't have a calendar.
        """
        slot_map = SlotMap({})
        intent = IntentClassifierResult("koan:Event", 1.0)
        intent_message = IntentMessage("session_id",
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
        calendar_file_value = CustomValue("computer")
        slot_map = SlotMap({"calendar_file":
                            SlotsList([NluSlot(calendar_file_value)])})
        intent = IntentClassifierResult("koan:Event", 1.0)
        intent_message = IntentMessage("session_id",
                                       "custom_data",
                                       "site_id",
                                       "what is happening today in computers",
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
        calendar_date_value = InstantTimeValue("2018-10-31 00:00:00"
                                               " +01:00",
                                               "grain",
                                               "precision")
        slot_map = SlotMap({"calendar_date":
                            SlotsList([NluSlot(calendar_date_value)])})
        intent = IntentClassifierResult("koan:Event", 1.0)
        intent_message = IntentMessage("session_id",
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
        calendar_date_value = TimeIntervalValue("2018-11-05 18:00:00"
                                                " +01:00",
                                                "2018-11-06 00:00:00"
                                                " +01:00")
        slot_map = SlotMap({"calendar_date":
                            SlotsList([NluSlot(calendar_date_value)])})
        intent = IntentClassifierResult("koan:Event", 1.0)
        intent_message = IntentMessage("session_id",
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
        slot_map = SlotMap({})
        intent = IntentClassifierResult("koan:Event", 1.0)
        intent_message = IntentMessage("session_id",
                                       "custom_data",
                                       "site_id",
                                       "what is happening",
                                       intent, slot_map)

        self.assertEqual(tools.get_date(intent_message), "")


if __name__ == '__main__':
    main()
