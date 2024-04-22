#!/usr/bin/python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/number/<int:n>", strict_slashes=False)
def testNum(n):
    "Prints n is a number only if n is a number"
    if isinstance(n, int):
        if n % 2 == 1:
            oddEven = 'odd'
        elif n % 2 == 0:
            oddEven = 'even'
    return render_template('6-number_odd_or_even.html', n=n, oddEven=oddEven)

if __name__ == '__main__':
    app.run(debug=None)
