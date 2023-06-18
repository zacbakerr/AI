# Logic 2 DONE

def lone_sum(a, b, c):
   return sum(n for n in [a, b, c] if [a, b, c].count(n) == 1)

def lucky_sum(a, b, c):
   return sum(n for i, n in enumerate([a, b, c]) if (13 not in [a, b, c][:i] and n != 13))

def close_far(a, b, c):
  return (abs(b-a)>=2 and abs(b-c)>=2 and abs(c-a)<=1) or (abs(c-a)>=2 and abs(c-b)>=2 and abs(b-a)<=1)

def make_bricks(small, big, goal):
   return not ((goal > big*5 + small) or (goal%5 > small))

def no_teen_sum(a, b, c):
   return sum(n for n in [a,b,c] if n not in [13,14,17,18,19])

def round_sum(a, b, c):
   return int(round(a+0.1,-1)+round(b+0.1,-1)+round(c+0.1,-1))

def make_chocolate(small, big, goal):
   return (goal-5*min(big,goal//5)) if (goal-5*min(big,goal//5)) <= small else -1

# Warmup 2 DONE

def string_times(str, n):
   return str*n

def front_times(str, n):
   return str[:3]*n

def string_bits(str):
   return str[::2]

def string_splosion(str):
   return "".join(str[:i] for i in range(len(str)+1))

def last2(str):
   return sum(1 for i in range(len(str)-2) if str[i:i+2]==str[-2:])

def array_count9(nums):
   return nums.count(9)

def array_front9(nums):
   return 9 in nums[:4]

def array123(nums):
   return ",1,2,3," in ","+",".join(str(c) for c in nums)+","

def string_match(a, b):
   return sum(1 for i in range(min(len(a), len(b))-1) if a[i:i+2] == b[i:i+2])

# String 2 DONE

def double_char(str):
   return "".join([c+c for c in str])

def count_hi(str):
   return str.count('hi')

def cat_dog(str):
   return str.count('dog') == str.count('cat')

def count_code(str):
   return sum(1 for i in range(len(str) - 3) if (str[i:i+2] == 'co' and str[i+3] == 'e'))

def end_other(a, b):
   return a.lower().endswith(b.lower()) or b.lower().endswith(a.lower())

def xyz_there(str):
   return sum(1 for i in range(len(str)) if ((str[i-1] != '.' or i==0) and str[i:i+3] == 'xyz')) >= 1

# List 2

def count_evens(nums):
   return sum(1 for num in nums if num%2==0)

def big_diff(nums):
   return max(nums)-min(nums)

def centered_average(nums):
   return (sum(nums)-min(nums)-max(nums))//(len(nums)-2)

def sum13(nums):
   return sum(num for i, num in enumerate(nums) if (num != 13 and 13 not in nums[i-1:i]))

def has22(nums):
   return (2,2) in zip(nums, nums[1:])

def sum67(nums):
   return sum(nums[i] for i in range(len(nums)) if ((6 in nums[:i+1] and 7 in nums[:i]) and (nums[:i][::-1].index(7) < nums[:i+1][::-1].index(6))) or (6 not in nums[:i+1] and 7 not in nums[:i]))

# Zachary Baker, 4, 2024