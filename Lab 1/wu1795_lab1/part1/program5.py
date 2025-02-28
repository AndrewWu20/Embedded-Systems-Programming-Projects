class FindPair:
    def __init__(self, numbers):
        self.numbers = numbers

    def find_pair(self, target):
        stored_indicies = {}
        for i, num in enumerate(self.numbers):
            complement = target - num
            if complement in stored_numbers:
                return stored_numbers[complement], i
            stored_indicies[num] = i 
        return None
    
numbers = [10, 20, 10, 40, 50, 60, 70]
find = FindPair(numbers)

target_num = int(input("What is your target number? "))
result = find.find_pair(target_num)

if result:
    index1, index2 = result
    print(f"index1={index1}, index2={index2}")
else:
    print("No pair found that adds up to the target number.")