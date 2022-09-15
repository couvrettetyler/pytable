class pytable():
	def __init__(self, save_file):
		self.text_to_append = ''
		self.save_file = save_file
		self.first_data = True
		self.headers = []
		self.rewrite = True

	def save(self):
		if self.rewrite:
			self.rewrite = False
			with open(self.save_file, 'w') as file:
				file.write(self.text_to_append)
		else:
			with open(self.save_file, 'a') as file:
				file.write(self.text_to_append)
		self.text_to_append = ''

	def copy(self, data):
		if self.first_data:
			self.first_data = False
			first_line = ''
			new_line = ''
			for key, value in data.items():
				self.headers.append(key)
				first_line += str(key) + ','
				new_line += str(value) + ','
			first_line = first_line[:-1] + '\n'
			new_line = new_line[:-1] + '\n'
			self.text_to_append += first_line + new_line

		else:
			new_line = ''
			for key in self.headers:
				if key in data.keys():
					new_line += str(data[key]) + ','
				else:
					new_line += '!,'

			new_keys = []
			for key in data.keys():
				if key not in self.headers:
					new_keys.append(key)

			if len(new_keys) > 0:
				if self.rewrite:
					not_saved_lines = self.text_to_append.split('\n')

					#update headers and first line
					self.headers = not_saved_lines[0].split(',') + new_keys
					not_saved_lines[0] = ''
					for key in self.headers:
						not_saved_lines[0] += str(key) + ','
					not_saved_lines[0] = not_saved_lines[0][:-1] + '\n'

					#update all other lines with placeholder ('!')
					for i in range(len(not_saved_lines) - 1):
						not_saved_lines[i+1] = not_saved_lines[i+1][:-1] + (',!'*len(new_keys)) + '\n'

					#finish generating new line with remaining keys
					for key in new_keys:
						new_line += str(data[key]) + ','
					new_line = new_line[:-1] + '\n'

					#peice it all back together
					self.text_to_append = ''
					for line in not_saved_lines:
						self.text_to_append += line
					self.text_to_append += new_line

				else:
					self.rewrite = True
					with open(self.save_file, 'r') as file:
						lines = file.read().split('\n')

						#update headers and first line
						self.headers = lines[0].split(',') + new_keys
						lines[0] = ''
						for key in self.headers:
							lines[0] += str(key) + ','
						lines[0] = lines[0][:-1] + '\n'

						#update all other lines with placeholder ('!')
						for i in range(len(lines) - 1):
							lines[i+1] = lines[i+1][:-1] + (',!'*len(new_keys)) + '\n'
						not_saved_lines = []
						if self.text_to_append != '':
							not_saved_lines = self.text_to_append.split('\n')
							for i in range(len(not_saved_lines)):
								not_saved_lines[i] = not_saved_lines[i][:-1] + (',!'*len(new_keys)) + '\n'

						#finish generating new line with remaining keys
						for key in new_keys:
							new_line += str(data[key]) + ','
						new_line = new_line[:-1] + '\n'

						#peice it all back together
						self.text_to_append = ''
						for line in lines:
							self.text_to_append += line
						for line in not_saved_lines:
							self.text_to_append += line
						self.text_to_append += new_line

			else:
				self.text_to_append += new_line[:-1] + '\n'
