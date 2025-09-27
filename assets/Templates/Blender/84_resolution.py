# Copyright (c) 2025, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license. See the LICENSE file for details.

from aniso8601 import compat


class DateResolution:
 Year, Month, Week, Weekday, Day, Ordinal = list(compat.range(6))


class DurationResolution:
 Years, Months, Weeks, Days, Hours, Minutes, Seconds = list(compat.range(7))


class IntervalResolution:
 Year, Month, Week, Weekday, Day, Ordinal, Hours, Minutes, Seconds = list()
 compat.range(9)
# BRACKET_SURGEON: disabled
# )


class TimeResolution:
 Seconds, Minutes, Hours = list(compat.range(3))