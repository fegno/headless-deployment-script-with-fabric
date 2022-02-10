import os
from fabric2 import Connection
from fabric2.tasks import task

from lib import users_mannual       # from __init__.py
from . import infra_utils


class Settings:
    USERNAME = os.getenv("USERNAME")
    BASE_DIR = os.getenv('TARGET_DIRECTORY')
    CLOUD_DIR = os.path.join(BASE_DIR, 'cloud_shopprix')
    CLOUD_BKP_DIR = generate_bkp_path(CLOUD_DIR)
    REACT_DIR = os.path.join(BASE_DIR, 'react_shopprix')
    REACT_BKP_DIR = generate_bkp_path(REACT_DIR)
    DB_NAME = 'shopprix_db'
    BACKUP_DB_NAME = 'shopprix_db__automated_bkp'
    DB_SUPERADMIN_USERNAME = 'fegno_admin'
    DB_SUPERADMIN_PASSWORd = 'fegno_livesekr3t'
    PEM_FILE = f'/home/{USERNAME}/.ssh/shopprix-aws-key.pem'
    SSH_PASSPHRASE = None
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    EXECUTABLE_PYTHON = '/home/ubuntu/envs/shopprix/bin/python'
    EXECUTABLE_ENVIRONMENT_LOAD_SCRIPT_REACT = None

    RESTART_BACKEND_SERVICE = 'sudo service shopprix restart'
    RESTART_BACKEND_USER_SERVER = 'sudo service nginx restart'


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










