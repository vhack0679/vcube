// Write a JavaScript program to check whether a given number is prime or not.
let num,
  is_prime = true;
num = 2;
for (let i = 2; i <= num / 2; i++) {
  if (num % i == 0) {
    is_prime = false;
  }
}
if (is_prime) {
  console.log("Prime");
} else {
  console.log("Not Prime");
}
