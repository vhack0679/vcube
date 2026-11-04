//Write a JavaScript program to find the factorial of a given number using a loop.
let num,
  f = 1;
num = 5;
for (let i = 1; i <= num; i++) {
  f = f * i;
}
console.log(f);
