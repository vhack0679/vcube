// Write a JavaScript program to count the number of digits in a given number. Input: 123456 Output: 6
let num, count;
num = 123456;
count = 0;
while (num > 0) {
  num = parseInt(num / 10);
  count = count + 1;
}
console.log(count);
