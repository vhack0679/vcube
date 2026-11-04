//Write a JavaScript program to calculate the sum of all even numbers between 1 and 50.
let sum = 0;
for (let i = 1; i <= 50; i++) {
  if (i % 2 === 0) {
    sum += i;
  }
}
console.log("The sum of all even numbers between 1 and 50 is: " + sum);
