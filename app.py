from flask import Flask, render_template, request
from flask_cors import cross_origin, CORS
import re

app = Flask(__name__)
CORS(app)


class Calculator:
    def __init__(self, s):
        self.s = s

    @staticmethod
    def compute(s):
        s = s.replace(" ", "")
        s = s.replace("+-", "-")
        s = s.replace("--", "+")
        if s[0] == '+':
            s = s[1:]

        nums = re.split("[\\+\\-\\*\\/]", s)
        ops = re.findall("[\\+\\-\\*\\/]", s)

        for n, i in enumerate(ops):
            if (i == '+') | (i == '-'):
                nums[n + 1] = i + nums[n + 1]
            if i == "-":
                ops[n] = '+'

        if s[0] == '-':
            del (nums[0])
            del (ops[0])

        blanks = [i for i in range(len(nums)) if nums[i] == ""]
        for n, i in enumerate(blanks):
            del (nums[i - n])
            del (ops[i - n])

        while len(nums) > 1:
            for n, o in enumerate(ops):
                if o == '/':
                    nums[n] = float(nums[n]) / float(nums[n + 1])
                    del (nums[n + 1])
                    del (ops[n])
                    break

                if o == '*':
                    if ops.count("/") == 0:
                        nums[n] = float(nums[n]) * float(nums[n + 1])
                        del (nums[n + 1])
                        del (ops[n])
                        break

                if o == '+':
                    if (ops.count("/") == 0) & (ops.count("*") == 0):
                        nums[n] = float(nums[n]) + float(nums[n + 1])
                        del (nums[n + 1])
                        del (ops[n])
                        break

                if o == '-':
                    if (ops.count("/") == 0) & (ops.count("*") == 0) & (ops.count("+") == 0):
                        nums[n] = float(nums[n]) - float(nums[n + 1])
                        del (nums[n + 1])
                        del (ops[n])
                        break

        return nums[0]

    @staticmethod
    def calculate(s):
        while s.count("(") > 0:
            left_par = sorted([i for i in range(len(s)) if s[i] == "("], reverse=True)[0]
            right_par = s.index(")", left_par) + 1
            ss = s[left_par: right_par]
            ss1 = ss.replace("(", "")
            ss1 = ss1.replace(")", "")
            com = str(Calculator.compute(ss1))
            s = s.replace(ss, com, 1)
        s = str(Calculator.compute(s))
        if s.endswith(".0"):
            s = s.split(".")[0]
        return s


@app.route("/")
@cross_origin()
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
@cross_origin()
def result():
    inp = ""
    try:
        inp = request.form.get('in')
        res = str(Calculator.calculate(inp))
    except:
        res = 'error'
    return render_template('index.html', result=res, input=inp)


if __name__ == "__main__":
    app.run()
