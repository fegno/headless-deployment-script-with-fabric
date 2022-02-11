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


def get_instance_ips():
    """
    Function to get instance IPs of your servers.
    Sometimes you'd want to do this, if your IPs are
    allocated dynamically, e.g. an auto-scaling group
    within AWS.
    
    if you have only one system. you can simpley use localhost or its ip for that. 
    """
    return [
        os.getenv('MASTER_IP'), # master
        os.getenv('REPLICA_IP'), # replica01
    ]



@task
def deploy(c, migrate=True, dependencies=True, collectstatic=False, django=False, react=False, deploy_together=False, 
           django_branch='master', react_branch='master', help=False):
    """
    Main command line task to deploy.
    This ensures validation and other primary checks. and call _deploy() to put in action.
    """
    if not (django or  react or deploy_together):
        print("You donot have selected which application to deploy.")
        print("please mention --django or --react or --deploy_together to proceeed! ")
        return
    if help:
        users_mannual():
        return
    
    python_utils._deploy_(
        c, 
        migrate=migrate, dependencies=dependencies, collectstatic=collectstatic, django=django, react=react, 
        deploy_together=deploy_together, django_branch=django_branch, react_branch=react_branch, help=help,
    )
    
    








