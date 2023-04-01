import blosum50 as b50
from multiprocessing import Queue
import copy

def printmatrix(m, pad = 4):
  for r in m:
    for d in r:
      print(f"{str(d):>{pad}}", end = " ")
    print()

class GenomeAligner():
    def __init__(self, len1, len2):
        """
        Returns a sequence aligner for strings of length (len1, len2)
        """
        self.gappenalty = -8
        self.seq1 = None
        self.seq2 = None

    def set_gep_penalty(self, new_penalty):
        self.gappenalty = new_penalty

    def calc_alignscore(self, seq1, seq2):
      self.scoringmatrix = [[0 for i in range(0,len(seq1)+1)] for j in range(0,len(seq2)+1)]
      # self.directionmatrix = [["." for i in range(0,len(seq1)+1)] for j in range(0,len(seq2)+1)]
      self.seq1 = seq1
      self.seq2 = seq2
      for i in range(0, len(self.scoringmatrix[0])):
        self.scoringmatrix[0][i] = i * self.gappenalty
        # self.directionmatrix[0][i] = "←"
      for i in range(0, len(self.scoringmatrix)):
        self.scoringmatrix[i][0] = i * self.gappenalty
        # self.directionmatrix[i][0] = "↑"
      # printmatrix(self.scoringmatrix, 2)
      # printmatrix(self.directionmatrix, 2)
      self.directionmatrix[0][0] = "🟩" #\u1F7E9
      for r in range(1, len(self.scoringmatrix)):
        for c in range(1, len(self.scoringmatrix[r])):
          vert = self.scoringmatrix[r-1][c] + self.gappenalty
          horz = self.scoringmatrix[r][c-1] + self.gappenalty
          diag = self.scoringmatrix[r-1][c-1]
          # if(seq1[c-1] == seq2[r -1]):
          #   # diag += 10
          char1 = seq1[c-1]
          char2 = seq2[r-1]
          index1 = b50.aminoDictionary[char1]
          index2 = b50.aminoDictionary[char2]
          diag += b50.blosum50[index2][index1]
          # else:
            # diag -= 10
          self.scoringmatrix[r][c] = max(vert,horz,diag)
          if diag >= horz and diag >= vert:
            self.directionmatrix[r][c] = "↖"
          if horz > diag and horz > vert:
            self.directionmatrix[r][c] = "←"
          if vert > diag and vert > horz:
            self.directionmatrix[r][c] = "↑"
      # printmatrix(self.scoringmatrix, 4)
      # printmatrix(self.directionmatrix, 0)
      # print(self.scoringmatrix[-1][-1])
      return self.scoringmatrix[-1][-1]

    def print_best_alignment_of_last_pair(self):
        aligned1 = ""
        aligned2 = ""
        pos1 = len(self.seq1)
        pos2 = len(self.seq2)

        while(pos1 > 0 or pos2 > 0):
          if(self.directionmatrix[pos2][pos1] == '↖'): # \u2196 diagonal
            aligned1 += self.seq1[pos1 - 1]
            aligned2 += self.seq2[pos2 - 1]
            pos1 -= 1
            pos2 -= 1
          elif(self.directionmatrix[pos2][pos1] == '←'): # \u2190 horizontal
            aligned1 += self.seq1[pos1-1]
            aligned2 += '-'
            pos1 -= 1
          elif(self.directionmatrix[pos2][pos1] == '↑'): # \u2191 vertical
            aligned1 += '-'
            aligned2 += self.seq2[pos2-1]
            pos2 -= 1
          else: # \u1F7E5 error
            aligned1 += '🟥'
            aligned2 += '🟥'
            pos1 -= 1
            pos2 -= 1

        aligned1 = aligned1[::-1]
        aligned2 = aligned2[::-1]

        print(aligned1)
        print(aligned2)

    def find_best_match(self, individual, arr):
      for ind in arr:
        # comments double check that you don't compare something to itself
        best_match_index = 0 # if arr[0][0] != individual[0] else 1
        best_match = self.calc_alignscore(individual[1], arr[0][1])
        for i in range(0, len(arr)):
          new_match_score = self.calc_alignscore(individual[1], arr[i][1])
          if new_match_score > best_match:
            if individual[0] != arr[i][0]:
              best_match = new_match_score 
              best_match_index = i
        # print(f"Best match is {best_match_index}")
        return arr[best_match_index]


# aligner = GenomeAligner(5,6)
# aligner.calc_alignscore('pawhe','pa??wh')
# aligner.print_best_alignment()