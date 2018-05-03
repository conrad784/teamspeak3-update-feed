TeamSpeak3 Update RSS Feed
===============

As the makers of [TeamSpeak3](http://teamspeak.com/) are only publishing a [json file](https://www.teamspeak.com/versions/server.json) for their current version of the TeamSpeak3 server I wanted to have a RSS feed of updates.

Everyday I will read my RSS feeds and can then add the new version to my [ansible-playbook](https://github.com/conrad784/ansible-teamspeak) to update the server.

How-to
------

Go to [csachweh.de/ts3/](https://csachweh.de/ts3/) and select the right feed and add it to your RSS feed reader.

How-to host urself
------

1. Install Python3

1. Install dependencies `requests json feedgenerator`

1. Change author of feed in 'main.py'

1. Install the systemd files in your system and change them according to your setup.


