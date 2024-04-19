#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import env, put, run
from datetime import datetime
from os import path
import re


env.hosts = ['100.25.16.150', '54.173.184.128']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server
    """
    try:
        if not path.exists(archive_path):
            print("Archive file {} doesn't exist.".format(archive_path))
            return False

        # upload archive to /temp/ dir of server
        put(archive_path, '/tmp/')

        # Extract timestamp from archive filename using any of the methods
        # timestamp = archive_path[-18:-4]
        timestamp = re.search(r'web_static_(\d+)\.tgz', archive_path).group(1)

        # create target dir
        target_dir = 'sudo mkdir -p /data/web_static/releases/web_static_{}/'
        run(target_dir.format(timestamp))

        # uncompress archive and delete .tgz
        uncompress_arch = 'sudo tar -xzf /tmp/web_static_{}.tgz ' \
                          '-C /data/web_static/releases/web_static_{}/'
        run(uncompress_arch.format(timestamp, timestamp))

        # remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move extracted contents into host web_static_{} from web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # remove extraneous web_static dir
        rm_web_static = 'sudo rm -rf /data/web_static/releases/' \
                        'web_static_{}/web_static'
        run(rm_web_static.format(timestamp))

        # delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # re-establish symbolic link to link to point to new web_static_{} dir
        new_sm_link = 'sudo ln -s /data/web_static/releases/' \
                      'web_static_{}/ /data/web_static/current'
        run(new_sm_link.format(timestamp))
    except Exception as e:
        return False

        # return True on success of all operations
    return True
