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
"""

#--------- Classes, Functions, etc ---------------------------------------------

#-------------------------------------------------------------------------------
#    Main 
#-------------------------------------------------------------------------------
if __name__=="__main__":
    import sys
    import json, requests

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('storedir', nargs=1, help='storage directory')

    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='show more verbose output')

    args = parser.parse_args()
    storedir = args.storedir[0]
    if not storedir.endswith("/"):
        storedir = storedir + "/"

    url = "https://www.teamspeak.com/versions/server.json"

    req = requests.get(url)
    if args.verbose:
        print("[INFO] got headers: {}".format(req.headers))
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
            version = info["version"]
            downloadlink = info["mirrors"]["4Netplayers.de"]
            checksum = info["checksum"]
            guid = checksum

            FEED = dict(
                title='Teamspeak3 Server Update Feed',
                subtitle="Teamspeak3 Server for {}-{}".format(platform, arch),
                link='http://www.csachweh.de/ts3/',
                description="""This feed shows always the latest version of the Teamspeak3 Server for {}'.format(platform))
                """,
                author_name='Conrad Sachweh',
                author_email='spam@spamthis.space',
                feed_url='http://www.csachweh.de/ts3',
                language='en',
            )

            FEED_ITEM = dict(
                title='Version {} is available!'.format(version),
                link='https://forum.teamspeak.com/forums/91-Latest-News',
                description='Version {} was released'.format(version),
                content='Version {} was released, get more information at <a href=\"https://forum.teamspeak.com/forums/91-Latest-News\">the forums</a>.<br>Download here: <a href=\"{}\">{}</a><br>SHA256: {}'.format(version, downloadlink, downloadlink, checksum),
                pubdate=timestamp,
                unique_id=guid
            )

            if args.verbose:
              print("[INFO] FEED: {}".format(FEED))
              print("[INFO] ITEM: {}".format(FEED_ITEM))
            import feedgenerator
            atomfeed = feedgenerator.Atom1Feed(**FEED)
            rssfeed  = feedgenerator.Rss201rev2Feed(**FEED)

            atomfeed.add_item(**FEED_ITEM)
            rssfeed.add_item(**FEED_ITEM)

            with open('{}{}_{}-atom.xml'.format(storedir, platform, arch), 'w') as f:
                result = atomfeed.writeString('utf-8')
                f.write(result)
            with open('{}{}_{}-rss.xml'.format(storedir, platform, arch), 'w') as f:
                result = rssfeed.writeString('utf-8')
                f.write(result)
