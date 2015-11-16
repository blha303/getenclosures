#!/usr/bin/env python3
import argparse
import errno
import json
import os
import sys

import appdirs
import requests

from bs4 import BeautifulSoup as Soup

cachepath = appdirs.user_cache_dir("getenclosures", "blha303")
configpath = appdirs.user_config_dir("getenclosures", "blha303")

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

mkdir(cachepath)
mkdir(configpath)

try:
    with open(cachepath + "/done") as f:
        done = [line.strip() for line in f.readlines()]
except:
    done = []

try:
    with open(configpath + "/config.json") as f:
        names = json.load(f)
except IOError:
    names = []

def get_uris(rssurl):
    """ Yields tuples: (torrent display name, uri) """
    global done
    soup = Soup(requests.get(rssurl).text, "lxml")
    for item in soup.findAll("item"):
        title = item.find("title").text
        if not title in done:
            yield title, item.find("enclosure")["url"]
            done.append(title)

def save_done():
    global done
    if not done:
        print("Not writing to cache file, no results", file=sys.stderr)
    else:
        with open(cachepath + "/done", "w") as f:
            f.write("\n".join(done))

def main():
    global cachepath
    global configpath
    configexample='{ "arch-releases": "https://www.archlinux.org/feeds/releases",\n  "linuxmint-releases": "http://torrents.linuxmint.com/rss/rss.xml" }'
    parser = argparse.ArgumentParser(prog="getenclosures")
    parser.add_argument("--config-dir", help="Set config directory. Defaults to " + configpath)
    parser.add_argument("--cache-dir", help="Set cache directory. Defaults to " + cachepath)
    args = parser.parse_args()
    if args.config_dir:
        configpath = args.config_dir
    if args.cache_dir:
        cachepath = args.cache_dir
    if not names:
        print("No names specified in {}/config.json, an example file has been created.".format(configpath), file=sys.stderr)
        with open("{}/config.json".format(configpath), "w") as f:
            f.write(configexample)
        return 10
    for name,uri in names.items():
        print("{}:".format(name), file=sys.stderr)
        for title,uri in get_uris(uri):
            print("    {}".format(title), file=sys.stderr)
            print("{}".format(uri))
    save_done()
    return 0

if __name__ == "__main__":
    sys.exit(main())