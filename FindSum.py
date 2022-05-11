import random

N = 80
M = 2
MAX_INT = 100

src_array = [random.randint(1,MAX_INT) for i in range(N)]
src_array.sort()

def find_two_elements(arr, find_sum):
    i = 0
    j = len(arr)-1
    while j>i:
        if arr[i]+arr[j] < find_sum:
            i += 1
        elif arr[i]+arr[j] > find_sum:
            j -= 1
        else:
            return [arr[i], arr[j]]

def find_approx_two(arr, find_sum):
    i = 0
    j = len(arr)-1
    best = []
    min_delta = MAX_INT
    while j>i:
        delta = arr[i]+arr[j]-find_sum
        if abs(delta)<min_delta:
            best = [arr[i], arr[j]]
        if delta<0:
            i += 1
        elif delta>0:
            j -= 1
        else:
            break
    return best

def find_any_elements(arr, find_sum):
    indexes = [0] + [i for i in range(1, M-1)] + [N-1]
    delta = sum([arr[i] for i in indexes]) - find_sum
    if delta>0:
        indexes[-1] -= 1  # move last element to the left
        move    



#print(src_array)
#print(find_two_elements(src_array, 198))
print(find_any_elements(src_array, 198))
