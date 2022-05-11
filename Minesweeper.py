# https://community.topcoder.com/stat?c=problem_statement&pm=17584
# This problem references the well-known puzzle game Minesweeper. Prior knowledge of the game is not necessary, the problem statement explains everything you need to know.

class TwoLineMinesweeper:
    templates = [ ['___'], ['*__', '_*_', '__*'], ['**_', '*_*', '_**'], ['***'] ]

    def next_variant(self, index):
        if self.indx[index]+1<len(self.templates[self.line[index]]):
            self.indx[index] += 1
            return True
        elif index+1<len(self.indx):
            self.indx[index] = 0
            return self.next_variant(index+1)
        else:
            return False

    def solve(self, firstLine):
        self.line = firstLine
        self.indx = [0]*len(firstLine)  # array of indexes for template
        result = []
        while True:
            variant = ' ' * len(firstLine)

            for i in range(len(firstLine)):
                t = self.templates[self.line[i]][self.indx[i]]   # current template for i position
                j = 0      # index inside current template [t]
                i2 = i - 1 # index in firstLine to apply template
                if i==0:
                    j = 1
                    i2 = 0
                
                if (i==0 and t[0]=='*') or (i==len(firstLine)-1 and t[2]=='*'):
                    variant = None
                    break

                while j<len(t):
                    if variant[i2] == ' ':
                        variant = variant[:i2] + t[j] + variant[i2+1:]    
                    elif variant[i2]!=t[j]:
                        variant = None
                        break
                    j += 1
                    i2 += 1
                    if i2>len(firstLine)-1:
                        break

                if not variant:
                    break
            
            if variant:
                result.append(variant)

            if not self.next_variant(0):
                break
        result.sort()
        return result
    
# test
obj = TwoLineMinesweeper()
print(obj.solve((2, 2, 2, 2, 2)))
print(obj.solve((0, 1, 1, 1, 0, 0, 1, 2, 3, 3, 2, 2, 1, 1, 0)))
#print(obj.solve((0,1,0,1,0,0)))