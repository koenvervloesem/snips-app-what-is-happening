#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the result sentences and intents for the Spanish (Spain) version
of the What is happening skill.
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
INTENT_EVENT = 'koan:Event'
INTENT_WHAT_IS_DEFAULT_CALENDAR = 'koan:WhatIsDefaultCalendar'
INTENT_CHANGE_DEFAULT_CALENDAR = 'koan:ChangeDefaultCalendar'
INTENT_RESET_DEFAULT_CALENDAR = 'koan:ResetDefaultCalendar'
INTENT_LIST_CALENDARS = 'koan:ListOfCalendars'
