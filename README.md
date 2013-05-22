timetrack
=========

**timetrack** pulls the title of the active X window every 5 secons and records some X parameters to a local sqlite database.
The database file is placed in the home directory and it is named timetrack.sqlite.

These are the X parameters the application checks.

* *WM_CLIENT_MACHINE(STRING)* as the hostname
* *WM_CLASS(STRING)* as the application class
* *NET_WM_NAME(UTF8_STRING)* as the window title

for what?
=========

I use it to track my working hours in all my *digital* tasks.

todo
====

* Add encription
* Add cloud support to track all my desktops
* Build an amazing html5 user interface
