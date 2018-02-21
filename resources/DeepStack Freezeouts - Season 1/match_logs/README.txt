The logs from DeepStack's public freezeout matches are provided in two formats in the following sub-directories:

ACPC/
PokerStars/

In both sub-directories there are directories for each series of freezeouts.  The directories for each of these "episodes" contain log files for each match played.  Match logs are also divided by player for episodes where we played multiple people.

Logs in the ACPC directory use a format based on the one used by the Annual Computer Poker Competition and are the official logs.  The directory also contains a brief README file that explains the format.

To make it easier for people within the online poker community to examine the matches, we also provide a set of full information logs for each match that are consistent with the format used by PokerStars.  The PokerStars format is usually supported by existing poker analytics software and you should be able to import the logs.  However, note that the PokerStars logs are synthetic in a sense, as we only mimic the PokerStars format.  In particular, the hand numbers are generated and may conflict with existing PokerStars hands in tools like Hold'em Manager.  Although we have tried to construct the hand numbers to avoid this, you may want to use a separate database to avoid any potential issues if you plan to import these logs.
