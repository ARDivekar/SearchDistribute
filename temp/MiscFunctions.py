import random


##-------------------------MISC FUNCTIONS------------------------##


def write_to_file(text, filepath, make_if_not_exists=True, encoding='utf-8'):
	text=text.encode(encoding)
	if make_if_not_exists:
		with open(filepath, 'w+') as some_file:
			some_file.write(text)
	else: 
		with open(filepath) as some_file:
			some_file.write(text)



def do_some_waiting(wait, printing=True):
	wait_time=random.uniform(0.3*wait, 1.5*wait)
	if printing:
		print "\n\t\tWAITING %s seconds between searches.\n"%(wait_time)
	time.sleep(wait_time)


