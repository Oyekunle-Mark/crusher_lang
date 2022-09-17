# crusher_lang

Crusher is a lightweight, interpreted procedural programming language.

Inspired in large part by boredom and wishful thinking.

Written in Python, with a hand-written lexer and parser, Crusher packs enough features to satisfy my aimless vanity.

## What does Crusher look like?

Below is what Crusher code looks like. This snippet doesn't achieve anything in particular. It's purpose is to show you some of Crusher's feature and how writing procedures in Crusher (like the `fibonacci` function below) is quite similar to most C-like programming language

```rust
let age = 12;

print age;

fn sum(a, b, c) {
    let age = 10;
    print age;

    return a + b + c;
}

let result = sum(2, 3, 5);
print result;

result = 0;
print result;

let start = 10;
let inc = 0;

fn increment_sum() {
    inc = inc + 1;
}

while (start > 0) {
    increment_sum();
    start = start - 1;
}

print start;
print inc;

fn fibonacci(n) {
    if (n <= 1) {
        return n;
    }

    return fibonacci(n - 1) + fibonacci(n - 2);
}

let thirteenth_fib = fibonacci(13);

if (thirteenth_fib == 233) {
    print "Crusher is crushing it";
} else {
    print "Oooh oooo. Damn bugs!!!!";
}

print true and false;
print false or true;

print null == null;
print 1 != 2;
```

## Running Crusher

You can choose to run crusher as a REPL and play with around with it in your terminal.
Or execute a Crusher source code (A file ending with `.crush` extension).

To begin, clone this repo and `cd` into the project directory.

Be sure that your `python` command isn't using python 2. You can check using the `python --version` command.
If it is, there are resources on the internet with information on how to install python 3. You can replace the **python** in the commands below with **python3** or use a command alias.

### Crusher REPL
To start the Crusher REPL, use `python crusher_lang/crusher_interpreter.py`. You can exit the REPL by using the `exit` command when you're done.

```bash
$ python crusher_lang/crusher_interpreter.py

Welcome to Crusher Lang.
Version 0.0.1 - Written by Oye Oloyede

> // and away we go
> fn say_hello_n_time(n) { while(n > 0) { print "Hello!"; n = n - 1;}}
> say_hello_n_time(5);
"Hello!"
"Hello!"
"Hello!"
"Hello!"
"Hello!"
>
> exit

Quitting...
Goodbye. Thank you for using Crusher Lang

```

### Crusher source codde
To execute a Crusher source code, use `python crusher_lang/crusher_interpreter.py test.crush` replacing ****test.crush**** with the name of your file.

## Improvements?
- Fair to say I should spend more time on better error reporting. The `Token` struct have line and column properties. I just got too lazy to use em :(
- Closures? Would be a neat idea.
- `for` loops? Even though you could achieve the same thing with the existing while loop, but a little syntactic sugar wouldn't hurt anyone.
