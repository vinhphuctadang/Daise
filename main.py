#!/usr/bin/env python
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.key_binding import KeyBindings
import os

from prompt_toolkit.shortcuts import print_formatted_text 
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
interpreter = None # global interpreter

kb = KeyBindings()

@kb.add('escape')
def _(event):
	'''
		Escaped is pressed:
	'''


	pass

WordCompleter = FuzzyWordCompleter
class Interpreter:
	'''
		Core system:
			- Underlying features 
			- Interactive Screen:
				+ Auto hint
	'''
	def getPromptString(self):
		return 'Daise %s$ '%(os.getcwd())
	def getGreetString(self):
		return 'Terminal wrapper\nDaise version 0.0.1 beta\n---------------------------'

	def loadFilesIntoCompleter(self):
		root, dirs, files = next(os.walk('.'))
		self.prompt_completer = WordCompleter(dirs+files)
	def __init__(self):
		self.history = InMemoryHistory()
		self.commands = {}
		# Todo: add tab key for completion
		for func in dir(self):
			if func.startswith('cmd_'):
				self.history.append_string(func[4:])
				self.commands[func[4:]] = getattr(self, func)
	
	def cmd_exit(self, args):
		if len(args):
			status = args[0]
		else:
			status = 0
		os._exit(status)

	def cmd_cat(self, args):
		if not len(args):
			print('[ERROR] Must have input file')
		filename = args[0]
		try:
			f = open(filename, 'r')
		except Exception as e:  
			print('[ERROR]',e)
			return
		for _ in f.readlines():
			print(_,end='')
		print()
		f.close()
	def cmd_cd(self, args):
		target = '.'
		if len(args):
			target = args[0]
		try:
			os.chdir(target)
			self.loadFilesIntoCompleter()
		except: 
			print('[ERROR] Directory not exist')
		pass
	def executeCommand(self, cmd):
		cmd = cmd.strip()
		syntax  = cmd.split()
		if len(syntax):
			if syntax[0] in self.commands:
				self.commands[syntax[0]](syntax[1:])
			else:
				os.system(cmd)


	def run(self):
		print(self.getGreetString())
		self.loadFilesIntoCompleter()
		style = Style.from_dict({
			'b': '#00ff00',
		})
		while True:
			try:
				text = prompt(HTML('<b>%s</b>'%(self.getPromptString())), 
					style=style,
					history=self.history,
					auto_suggest=AutoSuggestFromHistory(),
					enable_history_search=True,
					completer=self.prompt_completer,
					complete_while_typing=True,
					key_bindings=kb
				)
				self.executeCommand(text)
				self.history.append_string(text)
			except Exception as e:
				print('Exception')
			except KeyboardInterrupt:
				# print('Keyboard interrupted')
				pass
def main():
	global interpreter
	interpreter = Interpreter()
	interpreter.run()
if __name__ == "__main__":
	main()