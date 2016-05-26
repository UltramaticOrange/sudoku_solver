import logging
import argparse
from   copy import deepcopy
from   math import sqrt

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('sudoku_file', default='', help='file name containing the sodoku problem to solve.')
	args = parser.parse_args()
	puzzle = puzzleObj(args.sudoku_file)

class C(object):
	BLANK_SPACE_VALUE = '0'
	
	ERR_FILE = 'Could not open file: %s'
	ERR_INVALID_PUZZLE = 'The puzzle is invalid: %s'

class puzzleObj(object):
	def __init__(self, puzzle_file):
		self.board = self._load_puzzle(puzzle_file)

		self.size = len(self.board)
		self.block_size = int(sqrt(self.size))
		
		self.VALUES = range(1, self.size+1)
		
		self._validate_puzzle()
		self.dirty = True
		
		while self.dirty:
			self.dirty = False
			self.solve()

	def _load_puzzle(self, puzzle_file):
		try:
			f = open(puzzle_file, 'r')
		except IOError as e:
			raise self.PuzzleException(C.ERR_FILE%args.sudoku_file)

		text_puzzle = f.read()
		f.close()

		return [self._puzzleList(l) for l in text_puzzle.splitlines()]

	def _validate_puzzle(self):
		if self.block_size - int(self.block_size) > 0:
			raise self.PuzzleException(C.ERR_INVALID_PUZZLE%'Incorrect size')
			
		# TODO: puzzleObj._validate_puzzle: check that all rows and cols are the same as self.size

		for ri in range(0, self.size):
			e = self._row_exclusions(ri)
			for v in range(1,self.size+1):
				if e.count(v) > 1:
					raise self.PuzzleException(C.ERR_INVALID_PUZZLE%'Value repeated in row')
			
		for ci in range(0, self.size):
			e = self._col_exclusions(ci)
			for v in range(1,self.size+1):
				if e.count(v) > 1:
					raise self.PuzzleException(C.ERR_INVALID_PUZZLE%'Value repeated in column')

		for ri in range(0, self.size, self.block_size):
			for ci in range(0, self.size, self.block_size):
				e = self._block_exclusions(ri, ci)
				for v in range(1,self.size+1):
					if e.count(v) > 1:
						raise self.PuzzleException(C.ERR_INVALID_PUZZLE%'Value repeated in block')
						
	def solve(self):
		for ri in range(0, self.size):
			for ci in range(0, self.size):
				if not self.board[ri][ci]:
					exclusions = self._row_exclusions(ri) + self._col_exclusions(ci) + self._block_exclusions(ri, ci)
					self.board[ri][ci].possible = filter(lambda n: n not in exclusions, self.VALUES)
					if len(self.board[ri][ci].possible) == 1:
						self.board[ri][ci] = self._puzzleCell(self.board[ri][ci].possible[0])
						self.dirty = True
		print ''
		for row in self.board:
			print row
			
	# it'd make more sense to just take the whole row instead of the index, but can't do that with columns
	# so I'm stickiing with index for consistancy.
	def _row_possible(self, row_index):
		possible = {}
		for ci in range(0, self.size):
			if self.board[row_index][ci] == 0:
				possible[ci] = self.board[row_index][ci].possible
		return possible

	def _strip_blanks(self, l):
		return filter(lambda v: v!=C.BLANK_SPACE_VALUE, l)

	def _row_exclusions(self, row_index):
		exclusions = self.board[row_index]
		return self._strip_blanks(exclusions)
		
	def _col_exclusions(self, col_index):
		exclusions = []
		for row in self.board:
			exclusions.append(row[col_index])
			
		return self._strip_blanks(exclusions)
		
	def _block_exclusions(self, row_index, col_index):
		exclusions = []
		block_row, block_col = self._block_first_index(row_index, col_index)

		for rows in self.board[block_row:block_row+self.block_size]:
			for val in rows[block_col:block_col+self.block_size]:
				exclusions.append(val)
		
		return self._strip_blanks(exclusions)
		
	def _block_first_index(self, row_index, col_index):
		return int(row_index-row_index%self.block_size), int(col_index-col_index%self.block_size)

	class _puzzleList(list):
		def __init__(self, l):
			super(puzzleObj._puzzleList, self).__init__(l)
			for i in range(0, len(self)):
				self[i] = puzzleObj._puzzleCell(self[i], 16)
				
	class _puzzleCell(int):
		possible = []

	class PuzzleException(Exception):
		pass

if __name__ == "__main__":
    main()

