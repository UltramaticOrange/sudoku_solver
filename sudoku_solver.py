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
		
		self._validate_puzzle()

	def _load_puzzle(self, puzzle_file):
		try:
			f = open(puzzle_file, 'r')
		except IOError as e:
			raise self.PuzzleException(C.ERR_FILE%args.sudoku_file)

		text_puzzle = f.read()
		f.close()
		# TODO: puzzleObj._load_puzzle: convert all values to ints and handle hex values.
		return [self._puzzleCell(l) for l in text_puzzle.splitlines()]

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
				print e
				for v in range(1,self.size+1):
					if e.count(v) > 1:
						raise self.PuzzleException(C.ERR_INVALID_PUZZLE%'Value repeated in block')

	def _strip_blanks(self, l):
		return filter(lambda v: v!=C.BLANK_SPACE_VALUE, l)

	def _row_exclusions(self, row_index):
		exclusions = deepcopy(self.board[row_index])
		return self._strip_blanks(exclusions)
		
	def _col_exclusions(self, col_index):
		exclusions = []
		for row in self.board:
			exclusions.append(row[col_index])
			
		return self._strip_blanks(exclusions)
		
	def _block_exclusions(self, row_index, col_index):
		exclusions = []
		block_row = int(row_index-row_index%self.block_size)
		block_col = int(col_index-col_index%self.block_size)

		for rows in self.board[block_row:block_row+self.block_size]:
			for val in rows[block_col:block_col+self.block_size]:
				exclusions.append(val)
		
		return self._strip_blanks(exclusions)

	class _puzzleCell(list):
		possible = set()

	class PuzzleException(Exception):
		pass

if __name__ == "__main__":
    main()

