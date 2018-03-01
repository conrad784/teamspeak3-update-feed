#!/usr/bin/python3
# -*- coding: utf-8 -*-
# (C) 2018 Conrad Sachweh

"""NAME
        %(prog)s - <description>
    
SYNOPSIS
        %(prog)s [--help]
        
DESCRIPTION
        none
        
FILES  
        none
     
SEE ALSO
        nothing
        
DIAGNOSTICS
        none
        
BUGS    
        none
    
AUTHOR
        Conrad Sachweh, conrad@csachweh.de
        {version}
"""

version="$Id$"
#--------- Classes, Functions, etc ---------------------------------------------
class Example(object):
    """This shows how the docu should be included in a class...
    """
    x=0

def examplefunc():
    """This shows how the docu should be included in a function...
    """
    pass
#-------------------------------------------------------------------------------
import argparse
class MyHelpFormatter(argparse.RawTextHelpFormatter):
    # It is necessary to use the new string formatting syntax, otherwise
    # the %(prog) expansion in the parent function is not going to work
    def _format_text(self, text):
        if '{version}' in text:
            text = text.format(version=version)
        return super(MyHelpFormatter, self)._format_text(text)

def ManOptionParser():
    return argparse.ArgumentParser(description=__doc__, 
                                       formatter_class=MyHelpFormatter)

#-------------------------------------------------------------------------------
#    Main 
#-------------------------------------------------------------------------------
if __name__=="__main__":
    import sys
    import json, requests

    parser = ManOptionParser()
    args = parser.parse_args()

    url = "https://www.teamspeak.com/versions/server.json"

    req = requests.get(url)
    from datetime import datetime
    last_modified = req.headers.get('Last-Modified')
    if last_modified:
        timestamp = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S GMT')
    else:
        timestamp = datetime.now()
    data = req.json()

    platforms = list(data.keys())

    for platform in platforms:
        arches = list(data[platform].keys())
        for arch in arches:
            info = data[platform][arch]
            from feedgen.feed import FeedGenerator
            fg = FeedGenerator()
            fg.id('http://www.csachweh.de/ts3')
            fg.title('Teamspeak3 Server Update Feed')
            fg.author( {'name':'Conrad Sachweh','email':'spam@spamthis.space'} )
            fg.link( href='http://www.csachweh.de/ts3', rel='alternate' )
            fg.logo('https://upload.wikimedia.org/wikipedia/de/thumb/c/c7/Teamspeak-Logo.svg/200px-Teamspeak-Logo.svg.png')
            fg.subtitle("Teamspeak3 Server for {}".format(platform))
            fg.link( href='http://www.csachweh.de/ts3/{}-feed.atom'.format(platform), rel='self' )
            fg.language('en')
            fg.description('This feed shows always the latest version of the Teamspeak3 Server for {}'.format(platform))

            version = info["version"]
            downloadlink = info["mirrors"]["4Netplayers.de"]
            checksum = info["checksum"]
            guid = checksum
    
            fe = fg.add_entry()
            fe.id(guid)
            fe.title('Version {} is available!'.format(version))
            fe.link(href="https://forum.teamspeak.com/forums/91-Latest-News")
            fe.content("Version {} was released, get more information at <a href=\"https://forum.teamspeak.com/forums/91-Latest-News\">the forums</a>.<br>Download here: <a href=\"{}\">{}</a><br>SHA256: {}".format(version, downloadlink, downloadlink, checksum))
        
            atomfeed = fg.atom_str(pretty=True) # Get the ATOM feed as string
            rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
            fg.atom_file('{}_{}-atom.xml'.format(platform, arch)) # Write the ATOM feed to a file
            fg.rss_file('{}_{}-rss.xml'.format(platform, arch)) # Write the RSS feed to a file
