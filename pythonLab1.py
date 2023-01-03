# Zachary Baker
# Gabor, Period 4
# 8/22/22

# Warmup 1

def sleep_in(weekday, vacation):
   return (not weekday or vacation)

def monkey_trouble(a_smile, b_smile):
   return (a_smile and b_smile) or (not a_smile and not b_smile)

def sum_double(a, b):
   return (a+b)*2 if (a == b) else a + b

def diff21(n):
   return abs(n-21)*2 if n > 21 else abs(n-21)

def parrot_trouble(talking, hour):
   return (hour < 7 or hour > 20) and talking

def makes10(a, b):
   return True if (a + b == 10) or (a == 10 or b == 10) else False

def near_hundred(n):
   return abs(n-100) <= 10 or abs(n-200) <= 10

def pos_neg(a, b, negative):
   return True if (a > 0 and b < 0 and not negative) or (b > 0 and a < 0 and not negative) or (a < 0 and b < 0 and negative) else False

# String 1

def hello_name(name):
   return "Hello " + name + "!"

def make_abba(a, b):
   return a + b + b + a

def make_tags(tag, word):
   return "<" + tag + ">" + word + "</" + tag + ">"

def make_out_word(out, word):
   return out[:len(out)//2] + word + out[len(out)//2:]

def extra_end(str):
   return str[len(str) - 2:len(str)] + str[len(str) - 2:len(str)] + str[len(str) - 2:len(str)]

def first_two(str):
   return str[0:2]

def first_half(str):
   return str[0:len(str)//2]

def without_end(str):
   return str[1:len(str) - 1]

# List 1

def first_last6(nums):
   return nums[0] == 6 or nums[len(nums) - 1] == 6

def same_first_last(nums):
   return len(nums) >= 1 and nums[0] == nums[len(nums) - 1]

def make_pi(n):
   return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7][:n]

def common_end(a, b):
   return a[0] == b[0] or a[len(a)-1] == b[len(b)-1]

def sum3(nums):
   return sum(nums)

def rotate_left3(nums):
   return nums[1:] + nums[:1]

def reverse3(nums):
   return nums[::-1]

def max_end3(nums):
   return [nums[0]] * len(nums) if nums[0] > nums[len(nums) - 1] else [nums[len(nums) - 1]] * len(nums)


# Logic 1

def cigar_party(cigars, is_weekend):
   return False if (cigars < 40 or (cigars > 60 and not is_weekend)) else True

def date_fashion(you, date):
   return 0 if (you <= 2 or date <= 2) else 2 if (you >= 8 or date >= 8) else 1

def squirrel_play(temp, is_summer):
   return False if temp < 60 or (temp > 90 and not is_summer) or (temp > 100 and is_summer) else True

def caught_speeding(speed, is_birthday):
   return 0 if speed <= 60 and not is_birthday else 1 if speed > 60 and speed <= 80 and not is_birthday else 2 if speed > 80 and not is_birthday else 0 if speed <= 65 and is_birthday else 1 if speed > 65 and speed <= 85 and is_birthday else 2

def sorta_sum(a, b):
   return a + b if a + b < 10 or a + b > 19 else 20

def alarm_clock(day, vacation):
   return "7:00" if day > 0 and day < 6 and not vacation else "10:00" if not vacation or (vacation and (day > 0 and day < 6)) else "off"

def love6(a, b):
   return a == 6 or b == 6 or a + b == 6 or abs(a-b) == 6

def in1to10(n, outside_mode):
   return True if (not outside_mode and n >= 1 and n <=10) or (outside_mode and (n <=1 or n >=10)) else False