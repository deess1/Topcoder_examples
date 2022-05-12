# https://community.topcoder.com/stat?c=problem_statement&pm=17502
# Once there was a planet with S inhabitants.
# The planet then faced N bad years in a row. Each year exactly one bad thing happened: either the planet got hit by a small asteroid, or the planet got visited by the space dragon.
	
# Once there was a planet with S inhabitants.
# . The planet then faced N bad years in a row. Each year exactly one bad thing happened: either the planet got hit by a small asteroid, or the planet got visited by the space dragon.
# . Preserved historical records tell us the following:

class DecreasingPopulation():
    def add_node(self, S, N):
        if N==0:
            self.variants.add(S)
        else:
            if S>0 and S % 2 == 0:
                self.add_node(S // 2, N-1)
            if S>0:
                self.add_node(S - 1, N-1)
        

    def count(self, S, N):
        self.variants = set()
        self.add_node(S, N)
        return len(self.variants)

test = DecreasingPopulation()
print('{24,1}', test.count(24,1))
print('{17,1}', test.count(17,1))
print('{2,2}', test.count(2,2))
print('{30,3}', test.count(30,3))
print('{4451,12}', test.count(4451,12))