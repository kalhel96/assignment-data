# 🔍 Problem 1: Find Most Frequent Element
# Given a list of integers, return the value that appears most frequently.
# If there's a tie, return any of the most frequent.
#
# Example:
# Input: [1, 3, 2, 3, 4, 1, 3]
# Output: 3

def most_frequent(numbers):
    if not numbers:          # empty list has no answer
        return None

    counts = {}              # number -> how many times we saw it
    best = numbers[0]

    for num in numbers:
        counts[num] = counts.get(num, 0) + 1
        if counts[num] > counts[best]:
            best = num

    return best

"""
Time and Space Analysis for problem 1:
- Best-case: O(n). We always have to look at every number to count it,
  so even the best input needs one full loop.
- Worst-case: O(n). One loop through the list. Each dictionary lookup
  and update is O(1) (amortized), so the total is O(n).
- Average-case: O(n). Same as above, there is no early exit.
- Space complexity: O(n). In the worst case every number is different,
  so the dictionary holds n keys.
- Why this approach? A dictionary lets us count each number in one pass.
  We also keep track of the best number while counting, so we don't need
  a second loop at the end.
- Could it be optimized? Not in time. We must see every number at least
  once, so O(n) is the best possible. A slower option would be calling
  numbers.count(x) for each x, which is O(n^2).
- Trade-offs: We use extra memory (the dictionary) to get fast time.
  Sorting first could avoid the dictionary, but sorting is O(n log n),
  which is slower.
"""


# 🔍 Problem 2: Remove Duplicates While Preserving Order
# Write a function that returns a list with duplicates removed but preserves order.
#
# Example:
# Input: [4, 5, 4, 6, 5, 7]
# Output: [4, 5, 6, 7]

def remove_duplicates(nums):
    seen = set()       # numbers we already added
    result = []        # final list, keeps the original order

    for num in nums:
        if num not in seen:      # set lookup is O(1)
            seen.add(num)
            result.append(num)

    return result

"""
Time and Space Analysis for problem 2:
- Best-case: O(n). We still have to check every item once.
- Worst-case: O(n). One loop. Checking "in seen" and adding to a set
  are both O(1) amortized, and append is amortized O(1).
- Average-case: O(n). No early exit, every item is checked once.
- Space complexity: O(n). If there are no duplicates, both the set and
  the result list grow to n items.
- Why this approach? The set makes "have I seen this before?" very fast.
  The list keeps the order, which a set alone cannot do.
- Could it be optimized? Time is already the best possible, O(n).
  A simpler but slower way is checking "if num not in result", but that
  searches a list each time, which makes it O(n^2).
- Trade-offs: We store the items twice (set + list), so we use more memory
  to get faster speed.
"""


# 🔍 Problem 3: Return All Pairs That Sum to Target
# Write a function that returns all unique pairs of numbers in the list that sum to a target.
# Order of output does not matter. Assume input list has no duplicates.
#
# Example:
# Input: ([1, 2, 3, 4], target=5)
# Output: [(1, 4), (2, 3)]

# ---- ORIGINAL solution (nested loops) ----
def find_pairs_original(nums, target):
    pairs = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):    # only look ahead, so no repeats
            if nums[i] + nums[j] == target:
                pairs.append((nums[i], nums[j]))
    return pairs

"""
Time and Space Analysis for ORIGINAL problem 3:
- Best-case: O(n^2). There is no early exit. We must check every pair
  to find ALL pairs, even if the first pair works.
- Worst-case: O(n^2). Nested loops check about n*n/2 pairs.
- Average-case: O(n^2). Same, every pair is always checked.
- Space complexity: O(n) for the output list (at most n/2 pairs).
  No other extra storage.
- Why this approach? It is easy to read and easy to get correct.
- Could it be optimized? Yes. Use a set to look up the "missing"
  number in O(1) instead of looping again. See the refactor below.
- Trade-offs: Very little memory, but very slow for big lists.
"""


# ---- OPTIMIZED solution (set lookup) ----
# OPTIMIZATION NOTE:
# The original version used two nested loops, which is O(n^2) time.
# For every number, it scanned the rest of the list looking for a partner.
# This version uses a set. For each number, we calculate the partner we need
# (target - num) and check if we have already seen it. Set lookups are O(1),
# so the whole thing is ONE loop: O(n) time.
# Cost: the set uses extra memory, O(n) space.
# Example: with 10,000 numbers, the original does about 50,000,000 checks,
# while this version does about 10,000.
def find_pairs(nums, target):
    seen = set()
    pairs = []

    for num in nums:
        partner = target - num
        if partner in seen:                  # O(1) lookup
            pairs.append((partner, num))     # smaller-seen number first
        seen.add(num)

    return pairs

"""
Time and Space Analysis for OPTIMIZED problem 3:
- Best-case: O(n). One loop through the list.
- Worst-case: O(n). One loop, each set lookup/add is O(1) amortized.
- Average-case: O(n). Same, no nested loops.
- Space complexity: O(n). The set can hold all n numbers, plus the
  output list.
- Why this approach? It turns "search the whole list for a partner"
  into "check one set", which is much faster.
- Could it be optimized? Not in time; we must look at each number once.
- Trade-offs:
    Original:  O(n^2) time, O(1) extra space (besides the output)
    Optimized: O(n)   time, O(n) extra space (the set)
  We trade some memory for a huge speed gain on large lists.
"""


# 🔍 Problem 4: Simulate List Resizing (Amortized Cost)
# Create a function that adds n elements to a list that has a fixed initial capacity.
# When the list reaches capacity, simulate doubling its size by creating a new list
# and copying all values over (simulate this with print statements).
#
# Example:
# add_n_items(6) → should print when resizing happens.

def add_n_items(n, initial_capacity=2):
    capacity = initial_capacity
    storage = [None] * capacity    # fixed-size "memory"
    size = 0                       # how many real items we have

    for i in range(n):
        if size == capacity:
            # List is full: make a new list twice as big and copy everything
            new_capacity = capacity * 2
            print(f"Resizing: capacity {capacity} -> {new_capacity}, copying {size} items")
            new_storage = [None] * new_capacity
            for j in range(size):
                new_storage[j] = storage[j]
            storage = new_storage
            capacity = new_capacity

        storage[size] = i
        size += 1
        print(f"Added {i} (size={size}, capacity={capacity})")

    return storage[:size]

"""
Time and Space Analysis for problem 4:
- When do resizes happen? Every time the list is full. Starting at
  capacity 2, resizes happen when size hits 2, 4, 8, 16, ...
  So for n = 6 there are 2 resizes (2 -> 4 and 4 -> 8).
- What is the worst-case for a single append? O(n). If the list is full,
  that one append must copy every existing item to the new list.
- What is the amortized time per append overall? O(1). The copies add up
  to about 2 + 4 + 8 + ... which is less than 2n total. Spread over n
  appends, that is a constant amount of extra work per append.
- Space complexity: O(n). The list never gets bigger than about 2n slots,
  and 2n is still O(n).
- Why does doubling reduce the cost overall? Because each resize makes
  room for MANY future appends. If we only grew by 1 slot each time,
  we would copy on every append, which adds up to O(n^2). Doubling means
  resizes happen rarely (only about log n times), so the total copying
  stays O(n).
"""


# 🔍 Problem 5: Compute Running Totals
# Write a function that takes a list of numbers and returns a new list
# where each element is the sum of all elements up to that index.
#
# Example:
# Input: [1, 2, 3, 4]
# Output: [1, 3, 6, 10]
# Because: [1, 1+2, 1+2+3, 1+2+3+4]

def running_total(nums):
    totals = []
    current = 0

    for num in nums:
        current += num          # keep adding, don't re-sum from the start
        totals.append(current)

    return totals

"""
Time and Space Analysis for problem 5:
- Best-case: O(n). We visit each number once.
- Worst-case: O(n). One loop, append is amortized O(1).
- Average-case: O(n). No early exit, same work for every input.
- Space complexity: O(n). The new list has the same length as the input.
- Why this approach? We keep a running "current" sum, so each step is
  just one addition. A slower way would be sum(nums[:i+1]) for each i,
  which re-adds everything every time and is O(n^2).
- Could it be optimized? Time is already the best possible. We could save
  space by changing the input list in place (O(1) extra space).
- Trade-offs: Changing the input in place saves memory but destroys the
  original list, which the caller might still need. Returning a new list
  is safer.
"""


# ===================== TEST CASES =====================
if __name__ == "__main__":
    # Problem 1
    assert most_frequent([1, 3, 2, 3, 4, 1, 3]) == 3
    assert most_frequent([7]) == 7                     # one item
    assert most_frequent([]) is None                   # empty list
    assert most_frequent([2, 2, 5, 5]) in (2, 5)       # tie
    assert most_frequent([-1, -1, 0]) == -1            # negative numbers
    print("Problem 1 passed")

    # Problem 2
    assert remove_duplicates([4, 5, 4, 6, 5, 7]) == [4, 5, 6, 7]
    assert remove_duplicates([]) == []                 # empty list
    assert remove_duplicates([1, 1, 1]) == [1]         # all the same
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]   # no duplicates
    print("Problem 2 passed")

    # Problem 3 (test both versions; sort so order doesn't matter)
    for fn in (find_pairs_original, find_pairs):
        assert sorted(fn([1, 2, 3, 4], 5)) == [(1, 4), (2, 3)]
        assert fn([], 5) == []                         # empty list
        assert fn([1, 2, 3], 100) == []                # no pairs
        assert fn([5], 10) == []                       # one item can't pair with itself
        assert sorted(fn([-1, 6, 2, 3], 5)) == [(-1, 6), (2, 3)]  # negatives
    print("Problem 3 passed")

    # Problem 4
    assert add_n_items(6) == [0, 1, 2, 3, 4, 5]
    assert add_n_items(0) == []                        # add nothing
    assert add_n_items(1) == [0]                       # no resize needed
    print("Problem 4 passed")

    # Problem 5
    assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert running_total([]) == []                     # empty list
    assert running_total([5]) == [5]                   # one item
    assert running_total([3, -3, 2]) == [3, 0, 2]      # negatives
    print("Problem 5 passed")

    print("\nAll tests passed!")