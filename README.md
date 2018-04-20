TAGS
======================================================================================================================================================================

	@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
	@date 19 Author 2018
	@project Texas Hold'em AI
	@file README.md

ABOUT
======================================================================================================================================================================

This project started as a project by Fidel Ramirez and me, Tom Lenz, for our
AI course at Lewis University. While the original purpose was fulfilled by the
19th of April, I will still probably be tweaking it when I have free time.

Its original function was to predict an opponent's reaction to a bet.
Specifically, whether an opponent would call, raise, or fold if a bet of a
certain value was made. While this original intent was fulfilled with a good
amount of success, it is still lacking in other areas. Specifically, predicting
an opponent's chance of victory off of the cards available and their betting
patterns. As of the time of this writing, this is the next major objective.

You can read more about the original project once the formal report is
officially released.


PRE-REQ's
======================================================================================================================================================================
Python >= 3.6.4
	This was written on and tested with Python 3.6.4

	While this will most likely work with all versions of 3, the project has
	not been tested on other versions, and stability cannot be guarenteed.

	I can say with certainty that it will *not* work on any version
	of Python2, due to the input methods for human-vs-ai play

TensorFlow >= 1.7.0
	This was tested with version 1.7.0 of the TensorFlow libraries.

	While this may work with lower versions, I can say with certainty that
	it will *not* work with any version less than 1.5.0, due to a lack of
	eager execution. There may be other features which were added after that
	which would block execution, but I am not aware of them.

	Once again, unless TensorFlow v1.7.0 is used, stability cannot
	be guarenteed

PYTHONPATH
	The heirarchy shipped via GitHub currently has a Linux shell script to
	set the PYTHONPATH environment varible appropriately. However, any OS
	with which this script is not compatible will need to do so manually.

	The important directories, relative to the root directory, is as follows:

		src/
		src/agent
		src/game

	In a bash shell, the PYTHONPATH varible can be set by navigating to the
	src/ directory and executing:

		. set-python-path.sh

	This assumes that TensorFlow's libraries are already on your PYTHONPATH


STARTING THE PROGRAM
======================================================================================================================================================================
To start the program, first, set the PYTHONPATH environment varible.
In a bash shell, this can be done by navigating to the src/ directory and doing
the following:

	. set-python-path.sh

After that, executing the following will initiate a game of agent-vs-human
Texas Hold'em

	python3 GameRunner.py

Adding in more agents, changing the starting value, and changing the initial
CSV file used by the neural network will be implemented in the future
For now, you'll need to do so manually. All of these things are present as
constants in GameRunner.py
Be warned, I am not certain how having multiple opponents will affect the agents
behavior. Specifically, I believe at this moment, only the 0th agent's network
will be updated, regardless of how many there are. I would advise against using
more than 2 players due to this, even if most of the code is set up to handle an
ambiguous number of players.
