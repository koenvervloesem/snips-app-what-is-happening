#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains a provisional translation for a Spanish (Spain) version
of the What is happening skill.
This is a workaround, Spanish sources may be smaller than English originals 'til translations catch up.
Please remember to change the default user to the one in your Snips console (Ctrl + F "yourusername").
"""

# Result sentences and their parts:
DEFAULT = "por defecto"
EMPTY = "vacío"
AND = "y"
RESULT_EVENT_NOTHING = "No hay nada en el calendario {}."
RESULT_INVALID_CALENDAR = "{} es un calendario inválido. Por favor elige otro."
RESULT_DEFAULT_CALENDAR = "Mi calendario por defecto es {}."
RESULT_LIST = "Esta es la lista de calendarios a elegir: "
RESULT_RESET = "He reseteado tu calendario por defecto."
RESULT_DEFAULT_CHANGED = "He cambiado tu calendario por defecto a {}."

# Intents
INTENT_EVENT = 'yourusername:Event'
INTENT_WHAT_IS_DEFAULT_CALENDAR = 'yourusername:WhatIsDefaultCalendar'
INTENT_CHANGE_DEFAULT_CALENDAR = 'yourusername:ChangeDefaultCalendar'
INTENT_RESET_DEFAULT_CALENDAR = 'yourusername:ResetDefaultCalendar'
INTENT_LIST_CALENDARS = 'yourusername:ListOfCalendars'
