# XMPP Status Monitor

A simple flask application that records XMPP status events to a sqlite database (there's an early mongodb database adapter that doesn't really work yet) and displays a summary page of the results.

## Installation

Run the following commands from the root of the project:

    virtualenv -p python3 xmppmon
    source xmppmon/bin/activate
    pip install .

## Running the Application

Set the following environment variables (you could add them to `xmppmon/bin/activate`):

- `XMPP_DOMAIN` the domain of the JIDs you want to monitor.
- `XMPP_USER` the XMPP user to log in as (the contact list of this user will be monitored)
- `XMPP_PASSWORD` the password of the `XMPP_USER` above.

Ensure you are within the virtual environment and execute the following command line:

    xmpp_monitor scan

This will start collecting the data; to serve the reports run the following command (in a separate process):

    xmpp_monitor start

You can start both processes simultaneously (for testing) using the `start_all` command (see command_line.py for the code).
