

class Settings:
    USERNAME = 'ubuntu'
    BASE_DIR = os.getenv('TARGET_DIRECTORY', f'/home/{USERNAME}/code/')
    CLOUD_DIR = os.path.join(BASE_DIR, 'cloud_shopprix')
    CLOUD_BKP_DIR = generate_bkp_path(CLOUD_DIR)

    REACT_DIR = os.path.join(BASE_DIR, 'react_shopprix')
    REACT_BKP_DIR = generate_bkp_path(REACT_DIR)

    DB_NAME = 'shopprix_db'
    BACKUP_DB_NAME = 'shopprix_db__automated_bkp'
    DB_SUPERADMIN_USERNAME = 'fegno_admin'
    DB_SUPERADMIN_PASSWORd = 'fegno_livesekr3t'

    PEM_FILE = f'/home/{USERNAME}/.ssh/shopprix-aws-key.pem'  # none for default.
    SSH_PASSPHRASE = None
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    EXECUTABLE_PYTHON = '/home/ubuntu/envs/shopprix/bin/python'
    EXECUTABLE_ENVIRONMENT_LOAD_SCRIPT_REACT = None

    RESTART_BACKEND_SERVICE = 'sudo service shopprix restart'
    RESTART_BACKEND_USER_SERVER = 'sudo service nginx restart'
