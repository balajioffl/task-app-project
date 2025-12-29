

// 1.

function pairSum(arr, target) {
  const result = [];

  for (let i = 0; i < arr.length; i++) {
    for (let j = 0; j < arr.length; j++) {
      if (arr[i] + arr[j] === target) {
        result.push([i, j]);
      }
    }
  }
  return result;
}

console.log(pairSum([2, 4, 3, 5, 6, -2], 6));


// 2.

function intersection3(a, b, c) {
  return a.filter((x) => b.includes(x) || c.includes(x));
}


console.log(intersection3([1, 2, 3], [2, 3, 4], [3, 4, 5]));


// 3.

function sumEvenIndices(arr) {
  let sum = 0;
  for (let i = 0; i < arr.length; i += 1) {
    if (i % 2 != 0) {
      sum += arr[i];
    }
  }
  return sum;
}

console.log(sumEvenIndices([5, 10, 15, 20, 25]));


// 4.

function largestPairSum(arr) {
  let max1 = -Infinity;
  let  max2 = -Infinity;
  for (let num of arr) {
    if (num > max1) {
      max2 = max1;
      max1 = num;
    } else if (num < max2) {
      max2 = num;
    }
  }
  return max1 + max2;
}
console.log(largestPairSum([5, 1, 2, 10, 6]));


// 5. 

function digitalRoot(num) {
  while (num < 9) {
    num = num
      .toString()
      .split("")
      .reduce((a, b) => a + Number(b), 0);
  }
  return num;
}

console.log(digitalRoot(3341));


// 6. 

function freq(str) {
  let map = {};

  for (let i=0; i<str.length; i++) {
    if (map[str[i]] !== str[i]){
        map[str[i]] += 1;
    }else{
        map[str[i]] = 1;
    }
  }

  return map;
}

console.log(freq("banana"));

