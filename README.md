timetrack
=========

_timetrack_ pulls the title of the active X window every 5 secons and records information to a csv file. The data recorded is

	*WM_CLIENT_MACHINE(STRING)* as the hostname
	*WM_CLASS(STRING)*as the application class
	*NET_WM_NAME(UTF8_STRING)* as the window title

