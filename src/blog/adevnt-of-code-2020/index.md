Title:        Adevnt of Code 2020
Date:         Dec 04, 2020  
Author:       Mahmoud Ashraf  
Description:  advent of code solutions by @22mahmoud
Keywords:     aoc, programming

## Advent of Code

This blog will be updated every day to show you my solutions 
for [aoc-2020](https://adventofcode.com/).

### 2020

#### Day 01

##### part 01 ⭐

The first part of day one is a two-sum problem needs to get the 
multiply of two entries that sum to `2020`

The naive solution you can do two loops and make a condition whenever 
the two numbers sum to `2020` break the loop and return the value.

```javascript
function p1(input) {
  for (let i = 0; i < input.length; i++)
    for (let j = 0; j < input.length; j++)
      if (input[i] + input[j] === 2020) 
        return input[i] * input[j];
}
```

This solution will take `O(n^2)` time complexity for each element.

We can enhance our solution by using `Map` data structure and only one loop

```javascript
function p1(input) {
  const map = new Map();
  for (let i = 0; i < input.length; i++) {
    const complement = 2020 - input[i];
    if (map.has(complement))
      return input[map.get(complement)] * input[i]

    map.set(input[i], i);
  }
}
```

this solution will take `O(n)` time complexity by traverse the list containing 
`n` element only once.

##### part 02 ⭐

The difference in the part two that we need to get the multiply for 
`three` numbers that sum to `2020`

We can use the same naive solution by using brute force with three loops.

```javascript
function p2(input) {
  for (let i = 0; i < input.length; i++)
    for (let j = 0; j < input.length; j++)
      for (let k = 0; k < input.length; k++)
        if (input[i] + input[j] + input[k] === 2020)
          return input[i] * input[j] * input[k];
}
```


