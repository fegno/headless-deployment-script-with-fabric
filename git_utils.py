

def clear_and_checkout(shell, branch):
	shell.run(f"git checkout .")
	shell.run(f"git checkout {branch}")

	
def pull(shell, branch):
	shell.run(f"git fetch")
	shell.run(f"git pull origin {branch}")




	
