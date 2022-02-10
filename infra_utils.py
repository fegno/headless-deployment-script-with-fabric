import os
import shutil
from lib import git_utils
from lib import code_utils
from lib import db_utils


def get_hosts(settings, get_instance_ips):

    """
    Returns a list of dictionaries which can be passed as keyword arguments
    to instantiate a `Connection`.
    Example:
        >>> hosts = get_hosts()
        >>> c = Connection(**hosts[0])

    """
    ips = sorted(get_instance_ips())
    return [{
        'host': f"{Settings.USERNAME}@{ip}",
        'connect_kwargs': {
            "passphrase": settings.SSH_PASSPHRASE,
            'key_filename': settings.PEM_FILE
        },
    } for ip in ips]


def provision(for_master, for_slave, is_master=True):
    """
    
    Args:
        for_master: value for master node 
        for_slave: value for slave node
        is_master: bool. is that loop running to configure master not slave

    Returns: either for_master ir for_slave depends on loop.

    """
    return for_master if is_master else for_slave


def deploy(shell, migrate=True, dependencies=True, collectstatic=False, backend=False, frontend=False, deploy_together=False,
           django_branch='master', react_branch='master', help=False):
    """
    
    Args:
        shell: pointer to connected terminal at the curresponding server.
        migrate: bool. no it needs migration?
        dependencies: bool. no it needs to install dependencies?
        collectstatic: bool. no it needs to collect static files?
        backend:
        frontend:
        deploy_together: 
        backend_branch:
        frontend_branch:
        help: 

    Returns:

    """
    hosts = get_hosts(Settings, get_instance_ips)

    for index, host in enumerate(hosts):
        print(f"****** Deploying to host {index} at {host['host']} ******")
        is_master = index == 0
        deploy_on_host(
            Connection(**host),
            migrate=provision( migrate, False, is_master=is_master),
            collectstatic=provision( collectstatic, False, is_master=is_master),
            dependencies=dependencies,
            deploy_django=django_only or deploy_together,
            deploy_react=react_only or deploy_together,
            django_branch=django_branch,
            react_branch=react_branch,
            meta={
                "settings": Settings,
            }
        )

def deploy_on_host(shell, migrate, collectstatic, dependencies, deploy_django, deploy_react, django_branch,
                   react_branch, meta=dict()):
    """
    Full deployment for a host, including migrations and collectstatic

    """

    if deploy_django:
        _deploy_django(
            shell, migrate=migrate, collectstatic=collectstatic, 
            dependencies=dependencies, django_branch=django_branch,
            meta=meta
        )
    if deploy_react:
        _deploy_react(
            shell, react_branch, meta=meta
      )


def _deploy_django(shell, migrate, collectstatic, dependencies, django_branch, meta):
    """
        ###### DJANGO
        # point 01 = Backup database
        # point 02 = Copy Current code Base
        # point 03 = check out changes
        # point 04 = git pull origin branch
        # point 05 - install dependencies
        # point 06 = collectstatic
        # point 07 = migrate
        # point 08 = restart gunicorn
        # point 09 = restart nginx
        # point 10 = check health and reset if necessery
    """
    #  definition
    settings = meta.get('settings', {})
    python = meta['settings'].EXECUTABLE_PYTHON

    # if exists
    db_utils.drop_backup(shell, db_name=settings.BACKUP_DB_NAME)
    code_utils.drop_backup(backup_path=settings.CLOUD_BKP_DIR)

    # generate new backup.
    db_utils.backup_current_database(shell, db_name=settings.DB_NAME, bkp_db_name=settings.BACKUP_DB_NAME)
    code_utils.backup_current_code(shell, source_path=settings.CLOUD_DIR, backup_path=settings.CLOUD_BKP_DIR)

    with shell.cd(settings.CLOUD_DIR):
        try:
            git_utils.clear_and_checkout(shell, branch=django_branch)
            print("Pulling Shell...")
            git_utils.pull(shell, branch=django_branch)

            if dependencies:
                print("Installing dependencies...")
                shell.run(f"{python} -m pip3 install -r requirements.txt")

            if migrate:
                print("Migrating database...")
                shell.run(f"{python} manage.py migrate")

            if collectstatic:
                print("Running collectstatic...")
                shell.run(f"{python} manage.py collectstatic")

            if meta['settings'].RESTART_BACKEND_SERVICE:
                shell.run(meta['settings'].RESTART_BACKEND_SERVICE)

            if meta['settings'].RESTART_BACKEND_USER_SERVER:
                shell.run(meta['settings'].RESTART_BACKEND_USER_SERVER)
        except Exception as e:
            code_utils.restore_from_backup(restore_to_path=settings.CLOUD_DIR, restore_from_path=settings.CLOUD_BKP_DIR)
            # code_utils.drop_backup(backup_path=settings.CLOUD_BKP_DIR)
            db_utils.restore_from_backup(shell, bkp_db_name=settings.BACKUP_DB_NAME, db_name=settings.DB_NAME)

        else:
            # code_utils.drop_backup(backup_path=settings.CLOUD_BKP_DIR)
            # db_utils.drop_backup(shell, db_name=settings.BACKUP_DB_NAME)
            pass


def _deploy_react(shell, react_branch, meta):
    """
    ####### NODEJS
    # point 01 = backup current code base.
    # point 02 = git checkout changes
    # point 03 = npm install
    # point 04 = npm restart pm2
    # point 05 = restart nginx
    # point 06 = check health and reset if necessery
    """

    code_utils.drop_backup(backup_path=settings.REACT_DIR)
    code_utils.backup_current_code(shell, source_path=settings.REACT_DIR, backup_path=settings.REACT_BKP_DIR)

    with shell.cd(settings.REACT_DIR):
        try:
            shell.run(f"git pull origin {react_branch}")
            shell.run(f"pm2 stop {settings.PROJECT_NAME}")
            shell.run(f"npm i")
            shell.run(f"npm run build")
            shell.run(f"pm2 start npm --name={settings.PROJECT_NAME} -- start")
        except  Exception as e:
            shell.run(f"pm2 stop {settings.PROJECT_NAME}")
            code_utils.restore_from_backup(restore_to_path=settings.REACT_DIR, restore_from_path=settings.REACT_BKP_DIR)
            shell.run(f"pm2 start npm --name={settings.PROJECT_NAME} -- start")
        else:
            # code_utils.drop_backup(backup_path=settings.REACT_DIR)
            # code_utils.backup_current_code(shell, source_path=settings.REACT_DIR, backup_path=settings.REACT_BKP_DIR)
            pass





