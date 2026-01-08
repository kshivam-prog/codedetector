from flask import Flask, render_template, request

app = Flask(__name__)

# -------------------------------
# INPUT TYPE & LANGUAGE DETECTION
# -------------------------------

def is_code(text):
    symbols = ["def ", "{", "}", ";", "#include", "public static", "()"]
    return any(s in text for s in symbols)

def detect_language(code):
    if "def " in code:
        return "Python"
    if "#include" in code:
        return "C / C++"
    if "public static void main" in code:
        return "Java"
    if "function" in code:
        return "JavaScript"
    return "Unknown"

# -------------------------------
# STATIC COMPLEXITY ANALYSIS
# -------------------------------

def estimate_time_complexity(code):
    loops = code.count("for") + code.count("while")
    sorting = any(k in code for k in ["sort(", "sorted("])
    recursion = code.count("def ") > 1

    if sorting and loops:
        return "O(n log n)"
    if loops >= 2:
        return "O(n²)"
    if recursion:
        return "O(n)"
    if loops == 1:
        return "O(n)"
    return "O(1)"

def estimate_space_complexity(code):
    if any(k in code.lower() for k in ["list", "[]", "{}", "dict", "set"]):
        return "O(n)"
    return "O(1)"

# -------------------------------
# PERFORMANCE ESTIMATION (REALISTIC)
# -------------------------------

def estimate_compile_time(language):
    if language == "Python":
        return "0 ms (interpreted)"
    if language == "C / C++":
        return "40–150 ms"
    if language == "Java":
        return "200–500 ms"
    return "Unknown"

def estimate_execution_time(tc, language):
    # Assumed input size
    n = 100000  

    # Base operations count (approx)
    if tc == "O(1)":
        ops = 1
    elif tc == "O(n)":
        ops = n
    elif tc == "O(n log n)":
        ops = int(n * 17)  # log2(1e5) ≈ 17
    elif tc == "O(n²)":
        ops = n * n
    else:
        ops = n

    # Ops per millisecond (rough, realistic)
    ops_per_ms = {
        "Python": 5_000_000,
        "Java": 15_000_000,
        "C / C++": 30_000_000
    }.get(language, 5_000_000)

    ms = ops / ops_per_ms
    return f"{ms:.2f} ms (n = 10⁵)"


def speed_class(tc):
    if tc in ["O(1)", "O(log n)"]:
        return "Very Fast ⚡"
    if tc == "O(n)":
        return "Fast"
    if tc == "O(n log n)":
        return "Risky ⚠️"
    return "Slow 🐢"

def platform_runtimes(tc, language):
    time = estimate_execution_time(tc, language)

    return {
        "leetcode": time,
        "codeforces": time,
        "hackerrank": time
    }


    if tc == "O(n log n)":
        return {
            "leetcode": exec_time,
            "codeforces": "Higher variance (may TLE for large n)",
            "hackerrank": exec_time
        }

    return {
        "leetcode": "Likely TLE",
        "codeforces": "Likely TLE",
        "hackerrank": "Likely TLE"
    }

# -------------------------------
# MAIN ROUTE
# -------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        user_input = request.form["code"]

        if is_code(user_input):
            language = detect_language(user_input)
            tc = estimate_time_complexity(user_input)
            runtimes = platform_runtimes(tc, language)

            result = {
                "type": "Code",
                "language": language,
                "time_complexity": tc,
                "space_complexity": estimate_space_complexity(user_input),
                "compile_time": estimate_compile_time(language),
                "execution_time": estimate_execution_time(tc, language),
                "speed": speed_class(tc),
                "leetcode_runtime": runtimes["leetcode"],
                "codeforces_runtime": runtimes["codeforces"],
                "hackerrank_runtime": runtimes["hackerrank"],
                "note": "All metrics are static estimates based on code structure, not real execution"
            }
        else:
            result = {
                "type": "Text / Problem Statement",
                "language": "N/A",
                "time_complexity": "Paste code to estimate",
                "space_complexity": "Paste code to estimate",
                "compile_time": "N/A",
                "execution_time": "N/A",
                "speed": "N/A",
                "leetcode_runtime": "N/A",
                "codeforces_runtime": "N/A",
                "hackerrank_runtime": "N/A",
                "note": "Static performance analysis requires actual source code"
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)


