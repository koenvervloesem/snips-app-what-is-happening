# What is happening app for Snips 
[![Build status](https://api.travis-ci.com/koenvervloesem/snips-app-what-is-happening.svg?branch=master)](https://travis-ci.com/koenvervloesem/snips-app-what-is-happening) [![Maintainability](https://api.codeclimate.com/v1/badges/f1feccc2fe9ca35daad7/maintainability)](https://codeclimate.com/github/koenvervloesem/snips-app-what-is-happening/maintainability) [![Test coverage](https://api.codeclimate.com/v1/badges/f1feccc2fe9ca35daad7/test_coverage)](https://codeclimate.com/github/koenvervloesem/snips-app-what-is-happening/test_coverage) [![Code quality](https://api.codacy.com/project/badge/Grade/41a7787006614fcf8c7c76376ae10c41)](https://app.codacy.com/app/koenvervloesem/snips-app-what-is-happening) [![Python versions](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org) [![GitHub license](https://img.shields.io/github/license/koenvervloesem/snips-app-what-is-happening.svg)](https://github.com/koenvervloesem/snips-app-what-is-happening/blob/master/LICENSE) [![Languages](https://img.shields.io/badge/i18n-en-brown.svg)](https://github.com/koenvervloesem/snips-app-what-is-happening/tree/master/translations) [![Snips App Store](https://img.shields.io/badge/snips-app-blue.svg)](https://console.snips.ai/store/en/skill_mN45remOonk)

**Important information: Following the acquisition of Snips by Sonos, the Snips Console is not available anymore after January 31, 2020. As such, I have exported all Snips Console data of this app and made these available in the directory [console](https://github.com/koenvervloesem/snips-app-what-is-happening/tree/master/console) with the same MIT license as the rest of this project. This project has been archived. If you're searching for an alternative to Snips, I believe that [Rhasspy](https://rhasspy.readthedocs.io/) is currently the best choice for an offline open source voice assistant.**

With this [Snips](https://snips.ai/) app, you can ask your voice assistant about today's or any other day's events. This app knows about births and deaths of famous people, holidays, historical events, and so on. The app gets its information from the Linux program `calendar`, hence it's able to work offline.

## Installation
The easiest way to install this app is by adding the Snips app [What is happening on this day](https://console.snips.ai/store/en/skill_mN45remOonk) to your assistant in the [Snips Console](https://console.snips.ai).

The `calendar` program is installed by default on Raspbian and many other Linux distributions. If not, you can find it in the package `bsdmainutils`. Install it with `sudo apt install bsdmainutils` on a Debian- or Ubuntu-based system.

## Configuration
If you want to change the default calendar, you can specify this in the user parameter `default_calendar`, in Snips Console, by editing the `config.ini` file of the app manually or by a voice command.

If you want to use a combination of calendars by default, leave the `default_calendar` parameter in this app empty, and then execute this command:

``` shell
sudo cp /usr/share/calendar/calendar.all /etc/calendar/
```

After this, edit the file `/etc/calendar/calendar.all` to your taste.

I have included an example calendar file with only English-language calendars. To use this file by default, copy it into `/etc/calendar/calendar.all`:

``` shell
sudo cp /var/lib/snips/skills/snips-app-what-is-happening/calendar.english-speaking /etc/calendar/calendar.all
```

The location of the calendar files is specified in the parameter `calendar_location`, with the default value `/usr/share/calendar`.

## Usage
This app recognizes the following intents:

*   koan:Event - The user asks about today's or any other day's event. The app responds with a random event for this day in the specified calendar or the default calendar.
*   koan:WhatIsDefaultCalendar - The user asks what the default calendar is. The app responds with the name of the default calendar.
*   koan:ChangeDefaultCalendar - The user asks to change the default calendar. The app changes its default calendar to the specified calendar.
*   koan:ResetDefaultCalendar - The user asks to reset the default calendar. The app changes its default calendar to the calendar program's default calendar.
*   koan:ListOfCalendars - The user asks for the list of available calendars. The app responds with the list of calendars it recognizes.

## Copyright
This app is provided by [Koen Vervloesem](mailto:koen@vervloesem.eu) as open source software. See LICENSE for more information.
