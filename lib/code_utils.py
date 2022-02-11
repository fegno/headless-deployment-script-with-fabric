import os


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


