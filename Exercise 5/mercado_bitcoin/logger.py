import logging
import os
# Color number definition
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# These are the sequences need to get colored output
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
	'WARNING': YELLOW,
	'INFO': WHITE,
	'DEBUG': BLUE,
	'CRITICAL': RED,
	'ERROR': RED
}

# Special function used to ease a message formatting edition


def formatter_message(message, use_color=True):
	if use_color:
		message = message.replace(
			"$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
	else:
		message = message.replace("$RESET", "").replace("$BOLD", "")
	return message

# Format log level name color accordinly


class ColoredFormatter(logging.Formatter):
	def __init__(self, msg, use_color=True):
		logging.Formatter.__init__(self, msg)
		self.use_color = use_color

	def format(self, record):
		levelname = record.levelname
		if self.use_color and levelname in COLORS:
			levelname_color = COLOR_SEQ % (
				30 + COLORS[levelname]) + levelname + RESET_SEQ
			record.levelname = levelname_color
		return logging.Formatter.format(self, record)

# Logger class used in all logging operations


class log(logging.Logger):
	# Message format with collors \033[1;35m = Magenta
	FORMAT = '\033[35m%(asctime)s\033[0m [$BOLD%(levelname)-18s$RESET]\033[35m [%(processName)s][%(threadName)s][%(module)s]\033[0m %(message)s - $BOLDLine:%(lineno)d$RESET'
	COLOR_FORMAT = formatter_message(FORMAT, True)

	def __init__(self, name='my_logger'):
		# Create logger with debug level
		logging.Logger.__init__(self, name, logging.DEBUG)

		# create console handler and set level to debug
		if not self.handlers:
			color_formatter = ColoredFormatter(self.COLOR_FORMAT)
			ch = logging.StreamHandler()
			ch.setLevel(logging.DEBUG)
			# add formatter to ch
			ch.setFormatter(color_formatter)
			# add ch to logger
			self.addHandler(ch)

			os.makedirs('logs', exist_ok=True)
			log_file = logging.FileHandler(
				filename=os.getcwd()+f'/logs/{name}.log', mode='w+', encoding='utf8')
			formatter = logging.Formatter(
				'%(asctime)s [%(levelname)-18s][%(processName)s][%(threadName)s][%(module)s] %(message)s - %(lineno)d')
			log_file.setFormatter(formatter)
			log_file.setLevel(logging.DEBUG)
			self.addHandler(log_file)