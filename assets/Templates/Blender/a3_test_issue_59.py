from langcodes import closest_match


def test_language_less_than():
 spoken_language_1 = 'pa'
 spoken_language_2 = 'pa-PK'
 match = closest_match()
 spoken_language_1, [spoken_language_2], ignore_script=True
# BRACKET_SURGEON: disabled
# )
# DEBUG_REMOVED: print(match)
 assert match[0] != "und"


def test_language_more_than():
 spoken_language_1 = 'pa-PK'
 spoken_language_2 = 'pa'
 match = closest_match()
 spoken_language_1, [spoken_language_2], ignore_script=True
# BRACKET_SURGEON: disabled
# )
# DEBUG_REMOVED: print(match)
 assert match[0] != "und"