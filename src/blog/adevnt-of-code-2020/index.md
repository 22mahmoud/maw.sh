---
title-prefix: Adevnt of Code 2020
date: 2020-12-04T00:00+02:00
author: Mahmoud Ashraf
description: advent of code solutions by @22mahmoud
keywords: aoc, programming
category: aoc
blog: true
---

This blog will be updated every day to show you my solutions
for [aoc-2020](https://adventofcode.com/).

## TOC

- [day 01](#Day 01) _⭐⭐_
- [day 02](#Day 02) _⭐⭐_
- day 03
- day 04
- day 05
- day 06
- day 07
- day 08
- day 09
- day 10
- day 11
- day 12
- day 13
- day 14
- day 15
- day 16
- day 17
- day 18
- day 19
- day 20
- day 21
- day 22
- day 23
- day 24
- day 25

---

## Day 01

[[part 01](#part 01 ⭐) - [part 02](#part 02 ⭐)]

### part 01 ⭐

The first part of day one is a two-sum problem needs to get the
multiply of two entries that sum to `2020`

The naive solution you can do two loops and make a condition whenever
the two numbers sum to `2020` break the loop and return the value.

```javascript
function p1(input) {
  for (let i = 0; i < input.length; i++)
    for (let j = 0; j < input.length; j++)
      if (input[i] + input[j] === 2020) return input[i] * input[j];
}
```

This solution will take `O(n^2)` time complexity for each element.

We can enhance our solution by using `Map` data structure and only one loop

```javascript
function p1(input) {
  const map = new Map();
  for (let i = 0; i < input.length; i++) {
    const complement = 2020 - input[i];
    if (map.has(complement)) return input[map.get(complement)] * input[i];

    map.set(input[i], i);
  }
}
```

this solution will take `O(n)` time complexity by traverse the list containing
`n` element only once.

### part 02 ⭐

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

---

## Day 02

[[part 01](#part 01 ⭐-2) - [part 02](#part 02 ⭐-2)]

### part 01 ⭐

We have a list of passwords with validation rules,
So we should validate each password and submit the
total number of valid passwords.

```
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
```

First, let's create an parser to extract information from each line.

```javascript
const getPasswordsList = () =>
  readFileSync(path.resolve(__dirname, 'input.txt'), 'utf8')
    .split('\n')
    .filter(Boolean)
    .map((i) => i.split(/[-,:,\s]+/));
```

We read the `input.txt` file and convert it into an array by split each line using
`.split(\n)` then we will use regex to extract min, max, target, and password
on each line by using multi separator: `-`, `:`, and `\s` for space.

If you interred to learn more about split with regex I highly recommend to watch
[Regular Expressions: split() - Programming with Text](https://www.youtube.com/watch?v=fdyqutmcI2Q) video.

Now we are ready to write the validator function:

```javascript
function getValidPasswordsP1(passwords) {
  return passwords.reduce((ans, [min, max, letter, password]) => {
    const count = password.match(new RegExp(letter, 'g'))?.length;
    return count >= +min && count <= +max ? ++ans : ans;
  }, 0);
}
```

### part 02 ⭐

Actually the part two is a lot easier than the part one it assume the first two numbers
are the positions for the target letter to only occurs in one of them.

```javascript
function getValidPasswordsP2(passwords) {
  return passwords.reduce((ans, [pos1, pos2, letter, password]) => {
    return (password.charAt(+pos1 - 1) === letter) ^
      (password.charAt(+pos2 - 1) === letter)
      ? ++ans
      : ans;
  }, 0);
}
```

Use the bitwise `XOR` to make sure it only occurs in only exact one position.
you can check the MDN [reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_XOR).
