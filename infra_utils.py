import os
import shutil
import git_utils

def generate_bkp_path(source_path):
    dir_name = source_path.rstrip('/').split('/')
    return os.path.join(source_path, '..', f'._{dir_name}_automated_bkp')



	
def drop_backup(backup_path):
	print("dropping backing")
	shell.run(f"rm -rf {backup_path};")


def backup_current_code(shell, source_path, backup_path):
	print("backing up current code")
	shell.run(f"cp {source_path} {backup_path};")
	

def restore_from_backup(restore_to_path, restore_from_path):
	print("dropping backing")
	shell.run(f"rm -rf {restore_to_path};")
	shell.run(f"cp -r  {restore_from_path} {restore_to_path};")
	

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
    return for_master if is_master else for_slave


def _deploy_(c, migrate=True, dependencies=True, collectstatic=False, django=False, react=False, deploy_together=False, 
             django_branch='master', react_branch='master', help=False):

    hosts = get_hosts(Settings, get_instance_ips)
    
    for index, host in enumerate(hosts):
	    print(f"****** Deploying to host {index} at {host['host']} ******")
	     is_master = index == 0
        deploy_on_host(
            Connection(**host),
            migrate = provision( migrate, False, is_master=is_master),
            collectstatic = provision( collectstatic, False, is_master=is_master),
            dependencies = dependencies,
            deploy_django = django_only or deploy_together,
            deploy_react = react_only or deploy_together,
            django_branch = django_branch,
            react_branch = react_branch,
            meta = {
		        "settings": Settings,

            }
        )
        

	
def deploy_on_host(c, migrate, collectstatic, dependencies, deploy_django, deploy_react, django_branch, react_branch, meta=dict()):
    """
    Full deployment for a host, including migrations and collectstatic

    """
    
    if deploy_django:
	    _deploy_django()
    if deploy_react:
	    _deploy_react()


def _deploy_django(shell):
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
    settings = meta.get('settings', {})
    
    db_utils.backup_current_database(shell, settings=settings )
    
    backup_current_code(shell, source_path=settings.CLOUD_DIR, backup_path=settings.CLOUD_BKP_DIR)
    
    shell.run('')
    
    with shell.cd(settings.CLOUD_DIR):
        
        git_utils.clear_and_checkout(shell, brnach=django_branch)
        
        git_utils.pull(shell, brnach=django_branch)
              
        if dependencies:
            print("Installing dependencies...\n")
            c.run(f"{PIPENV} install")
        if migrate:
            print("Migrating database...\n")
            c.run(f"{PIPENV} run python manage.py migrate")
        if collectstatic:
            print("Running collectstatic...\n")
            c.run(f"{PIPENV} run python manage.py collectstatic")


def _deploy_react():
	"""
	####### NODEJS
    # point 01 = backup current code base.
    # point 02 = git checkout changes
    # point 03 = npm install
    # point 04 = npm restart pm2
    # point 05 = restart nginx
    # point 06 = check health and reset if necessery
    """
    





