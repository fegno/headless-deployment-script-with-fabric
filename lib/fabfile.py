import os
from fabric2 import Connection
from fabric2.tasks import task
from config import Settings
import db_utils

import node_utils
import python_utils
import django_utils
import infra_utils
from . import users_mannual

from lib import users_mannual       # from __init__.py
from . import infra_utils

def get_instance_ips():
    """
    Function to get instance IPs of your servers.
    Sometimes you'd want to do this, if your IPs are
    allocated dynamically, e.g. an auto-scaling group
    within AWS.

    if you have only one system. you can simpley use localhost or its ip for that.
    """
    return [
        'ip-172-31-22-63.ap-south-1.compute.internal',  # master
        'ip-172-31-21-222.ap-south-1.compute.internal',  # replica_01
    ]


@task
def deploy(c, migrate=True, dependencies=True, collectstatic=False, django=False, react=False, deploy_together=False,
           django_branch='master', react_branch='master', help=False):
    """
    Main command line task to deploy.
    This ensures validation and other primary checks. and call _deploy() to put in action.
    """
    if not (django or react or deploy_together):
        print("You do not have selected which application to deploy.")
        print("please mention --django or --react or --deploy_together to proceeed! ")
        return None

    if help:
        return users_mannual()

    infra_utls.deploy(
        c,
        migrate=migrate, dependencies=dependencies, collectstatic=collectstatic, django=django, react=react,
        deploy_together=deploy_together, django_branch=django_branch, react_branch=react_branch, help=help,
    )










