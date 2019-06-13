from src.main import Canary
from src.app.core.get_arguments import get_arguments
import os
import sys
import platform
import multiprocessing


if __name__ == '__main__':
	current_dir = os.path.dirname(os.path.realpath(__file__))
	src_dir = current_dir + os.sep + 'src' + os.sep
	print("Running Canary on ", str(platform.system()))
	# Change environment variable to allow multiprocessing
	if platform.system() == 'Darwin':
		try:
			if not 'OBJC_DISABLE_INITIALIZE_FORK_SAFETY' in os.environ:
				os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
		except Exception as e:
			print(e)
			print("If you experience errors when executing, Set the environment variable to allow multiprocessing:")
			print("to set in bash: 'export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES'")
			pass
	if not len(sys.argv) > 1:  # No Args Defined
		python_path = sys.executable
		try:
			print("Running GUI")
			os.system(str(sys.executable) + " " + src_dir + "canary_gui.py")
		except Exception as e:
			print(e)
			pass
		# if platform == 'Windows':
			# subprocess.Popen(['start /b "', str(sys.executable), 'canary_gui.py'])
			# os.system('start /b "' + str(sys.executable) + ' canary_gui.py')
		# else:
			# subprocess.Popen([str(sys.executable), 'canary_gui.py'])
			# os.system(str(sys.executable) + ' canary_gui.py &>/dev/null &')

		# exit()
	else:
		multiprocessing.freeze_support()
		arguments = get_arguments()
		Canary(arguments)
