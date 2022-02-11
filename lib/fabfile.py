
import node_utils
import python_utils
import django_utils
import infra_utils
from fabric2.tasks import task
from lib import users_mannual       # from __init__.py


def get_instance_ips():
    """
    Function to get instance IPs of your servers.
    Sometimes you'd want to do this, if your IPs are
    allocated dynamically, e.g. an auto-scaling group
    within AWS.

    if you have only one system. you can simpley use localhost or its ip for that.
    Returns: None
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

    Args:
        c: connection to local server.
        migrate: bool. no it needs migration?
        dependencies: bool. no it needs to install dependencies?
        collectstatic: bool. no it needs to collect static files?
        django: bool. weather to deploy django application or not.
        react: bool. weather to deploy react application or not.
        deploy_together: bool. a shortcut to tell deploy both.
        django_branch: str. Branch name to get deployed.
        react_branch: str. Branch name to get deployed.
        help: to display user mannual

    Returns: None

    """
    if not (django or react or deploy_together):
        print("You do not have selected which application to deploy.")
        print("please mention --django or --react or --deploy_together to proceeed! ")
        return None

    if help:
        return users_mannual()

    infra_utils.deploy(
        c,
        migrate=migrate, dependencies=dependencies, collectstatic=collectstatic, django=django, react=react,
        deploy_together=deploy_together, django_branch=django_branch, react_branch=react_branch, help=help,
    )









