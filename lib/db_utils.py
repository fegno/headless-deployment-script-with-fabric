

DB_ADMIN_USER_NAME = ''
DB_ADMIN_PASSWORD = ''


def backup_current_database(conn, db_name, bkp_db_name):
	print("backing up database :", db_name)
	print("backing up completed!!")


def drop_backup(conn, db_name):
	print("dropping backup for  database :", db_name)
	print("dropping backup completed!!")


def restore_from_backup(conn, bkp_db_name, db_name ):
	print("restoring database :", db_name)
	print("restoring completed!!")
	

