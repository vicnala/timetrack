timetrack
=========

*timetrack* pulls the title of the active X window every 5 secons and records information to a csv file. The data recorded is

	_WM_CLIENT_MACHINE(STRING)_ as the hostname
	_WM_CLASS(STRING)_ as the application class
	_NET_WM_NAME(UTF8_STRING) as the window title

