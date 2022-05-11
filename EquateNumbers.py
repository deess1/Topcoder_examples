# https://community.topcoder.com/stat?c=problem_statement&pm=13901
# Problem Statement
# Given an array A consisting of n integers. You have to tell whether you can make all of them equal by applying following operation as many times as you want.
# .  Choose any number in the array and replace it by any non trivial divisor of it.
# Return "yes" or "no" according to the situation.

class EquateNumbers():

    def arrIsEqual(self, arr):
        for i in range(1, len(arr)):
            if arr[i] != arr[0]:
                return False
        return True

    def GetNextPrime(self, prime_num):
        if prime_num<3:
            return prime_num + 1
        else:
            while True:
                prime_num += 2
                is_prime = True
                for i in range(3, int(prime_num ** 0.5 +1)):
                    if prime_num % i == 0:
                        is_prime = False
                if is_prime:
                    return prime_num 
        
    def canMakeEqual(self, arr):
        prime_num = 1    
        while True:
            if self.arrIsEqual(arr):
                return 'yes'
            arr.sort()
            prime_num = self.GetNextPrime(prime_num)
            if prime_num>arr[0] or prime_num>50:
                return 'no'
            cnt = [0]*len(arr)
            for i in range(len(arr)):
                while arr[i] % prime_num == 0:
                    arr[i] = arr[i] // prime_num
                    cnt[i] = 1
            if sum(cnt) == len(arr):
                return 'yes'

test = EquateNumbers()

print('[1,1,1]', test.canMakeEqual([1,1,1]))                
print('[2, 4]', test.canMakeEqual([2, 4]))                
print('[3, 6, 7]', test.canMakeEqual([3, 6, 7]))                
print('[516489004,351371688,811236122,359319772]', test.canMakeEqual([516489004,351371688,811236122,359319772]))                
print('[774790715,541447280,142096365,445121785,583653195,71374815,798454490,409670625,942953335,8997395]', test.canMakeEqual([774790715,541447280,142096365,445121785,583653195,71374815,798454490,409670625,942953335,8997395]))                