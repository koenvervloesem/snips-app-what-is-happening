# What is happening skill for Snips 
[![Build Status](https://api.travis-ci.com/koenvervloesem/snips-app-what-is-happening.svg?branch=master)](https://travis-ci.com/koenvervloesem/snips-app-what-is-happening)

With this [Snips](https://snips.ai/) skill, you can ask your voice assistant about today's or any other day's events. This app knows about births and deaths of famous people, holidays, historical events, and so on. The app gets its information from the Linux program `calendar`, hence it's able to work offline.

## Installation
The easiest way to install this skill is by adding the Snips app [What is happening on this day](https://console.snips.ai/store/en/skill_mN45remOonk) to your assistant in the [Snips Console](https://console.snips.ai).

The `calendar` program is installed by default on Raspbian and many other Linux distributions. If not, you can find it in the package `bsdmainutils`. Install it with `sudo apt install bsdmainutils` on a Debian- or Ubuntu-based system.

## Configuration
If you want to change the default calendar, you can specify this in the user parameter `default_calendar`, in Snips Console, by editing the `config.ini` file of the app manually or by a voice command (if the config.ini file is writable: chmod a+w /var/lib/snips/skills/snips-app-what-is-happening/config.ini).

If you want to use a combination of calendars by default, leave the `default_calendar` parameter in this app empty, and then execute this command:

```
sudo cp /usr/share/calendar/calendar.all /etc/calendar/
```

After this, edit the file `/etc/calendar/calendar.all` to your taste.

The location of the calendar files is specified in the parameter `calendar_location`, with the default value `/usr/share/calendar`.

## Usage
This app recognizes the following intents:

koan:Event
:  The user asks about today's or any other day's event. The app responds with a random event for this day in the specified calendar or the default calendar.

koan:WhatIsDefaultCalendar
:  The user asks what the default calendar is. The app responds with the name of the default calendar.

koan:ChangeDefaultCalendar
:  The user asks to change the default calendar. The app changes its default calendar to the specified calendar.

koan:ResetDefaultCalendar
:  The user asks to reset the default calendar. The app changes its default calendar to the calendar program's default calendar.

koan:ListOfCalendars
:  The user asks for the list of available calendars. The app responds with the list of calendars it recognizes.

## Copyright
This skill is provided by [Koen Vervloesem](mailto:koen@vervloesem.eu) as open source software. See LICENSE for more information.
