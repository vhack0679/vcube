//Write a JavaScript program to count how many numbers between 1 and 100 are divisible by 5.
let i,
  count = 0;
i = 1;
for (i = 1; i <= 100; i++) {
  if (i % 5 === 0) {
    count = count + 1;
  }
}
console.log(
  "The count of numbers between 1 and 100 that are divisible by 5 is: " + count,
);
