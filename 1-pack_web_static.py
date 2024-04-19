#!/usr/bin/python3
from fabric.api import local
from time import strftime
from datetime import date
from os import path


def do_pack():
    """ A script that generates archive the contents of web_static folder"""
    
    if not path.exists("versions"):
        local("mkdir -p versions")

    timestamp = strftime("%Y%m%d%H%M%S")

    print("Packing web_static to versions/web_static_{}.tgz".format(timestamp))
    try:
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(timestamp))

        return "versions/web_static_{}.tgz".format(timestamp)

    except Exception as e:
        return None
