"""
Dual-mode AI Code Assistant.
Mock mode: Pattern-based code analysis (no API key needed).
Real mode: Google Gemini API (when GOOGLE_API_KEY is set).
"""
import os
import re
import time

# --- Mode detection ---
def get_mode():
    key = os.environ.get('GOOGLE_API_KEY', '').strip()
    return 'real' if key else 'mock'


# --- Gemini API (real mode) ---
def _call_gemini(prompt):
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI API Error: {str(e)}\n\nFalling back would require mock mode."


LANGUAGE_PROMPTS = {
    'python': "Analyze the following Python code:\n\n```python\n{code}\n```\n\nCarefully examine the code line-by-line. Focus on errors, logic issues, and suggest improvements.",
    'javascript': "Debug the following JavaScript code:\n\n```javascript\n{code}\n```\n\nExplain what it does, identify bugs, and suggest optimizations.",
    'java': "Review the following Java code:\n\n```java\n{code}\n```\n\nCheck for compilation errors, logic issues, and best practices.",
    'cpp': "Analyze the following C++ code:\n\n```cpp\n{code}\n```\n\nCheck for memory issues, syntax errors, and suggest improvements.",
    'html': "Analyze this HTML code:\n\n```html\n{code}\n```\n\nCheck for semantic errors, structure issues, and recommend improvements.",
    'css': "Check this CSS snippet for best practices:\n\n```css\n{code}\n```\n\nSuggest improvements in style, responsiveness, and optimization.",
}

EXPLAIN_PROMPT = "Explain the following {language} code in detail, line by line:\n\n```{language}\n{code}\n```\n\nProvide a clear explanation suitable for a beginner."

REFACTOR_PROMPT = "Refactor the following {language} code for better performance, readability, and best practices:\n\n```{language}\n{code}\n```\n\nProvide the improved version with explanations for each change."

GENERATE_PROMPT = "Generate {language} code for the following task:\n\n{prompt}\n\nProvide clean, well-commented code with example usage."


# --- Mock AI Engine ---
def _mock_analyze(code, language):
    """Pattern-based code analysis."""
    lines = code.strip().split('\n')
    line_count = len(lines)
    issues = []
    info = []

    # Count constructs
    functions = [l.strip() for l in lines if re.match(r'\s*(def |function |public |private |void )', l)]
    classes = [l.strip() for l in lines if re.match(r'\s*(class )', l)]
    loops = [l for l in lines if re.search(r'\b(for|while)\b', l)]
    imports = [l.strip() for l in lines if re.match(r'\s*(import |from |#include|require|using )', l)]
    comments = [l for l in lines if l.strip().startswith(('#', '//', '/*', '*'))]

    info.append(f"**Code Statistics:**")
    info.append(f"- Lines of code: {line_count}")
    info.append(f"- Functions/Methods: {len(functions)}")
    info.append(f"- Classes: {len(classes)}")
    info.append(f"- Loops: {len(loops)}")
    info.append(f"- Imports: {len(imports)}")
    info.append(f"- Comments: {len(comments)}")
    info.append("")

    if language == 'python':
        # Python-specific checks
        try:
            compile(code, '<string>', 'exec')
            info.append("**Syntax Check:** No syntax errors detected.")
        except SyntaxError as e:
            issues.append(f"**Syntax Error** on line {e.lineno}: {e.msg}")

        # Check common issues
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                if re.search(r'\bprint\s*\(', stripped) and stripped.count('(') != stripped.count(')'):
                    issues.append(f"Line {i}: Unmatched parentheses in print statement")
                if 'range(len(' in stripped:
                    issues.append(f"Line {i}: Consider using `enumerate()` instead of `range(len())`")
                if re.match(r'[a-z]\s*=', stripped) and len(stripped.split('=')[0].strip()) == 1:
                    issues.append(f"Line {i}: Single-character variable name — consider a more descriptive name")

        if not comments:
            issues.append("No comments found — consider adding docstrings or comments for clarity")
        if functions and '"""' not in code and "'''" not in code:
            issues.append("Functions lack docstrings — consider adding documentation")

    elif language == 'javascript':
        if 'var ' in code:
            issues.append("Using `var` — consider using `let` or `const` for block scoping")
        if '==' in code and '===' not in code:
            issues.append("Using loose equality (`==`) — consider strict equality (`===`)")
        if 'console.log' in code:
            info.append("Note: `console.log` statements found — remove before production")

    elif language in ('java', 'cpp'):
        if 'public static void main' in code or 'int main' in code:
            info.append("Entry point detected (main method/function)")
        if language == 'cpp' and 'using namespace std' in code:
            issues.append("Using `using namespace std` — may cause naming conflicts in larger projects")

    # Build response
    response = "## Code Analysis\n\n"
    response += '\n'.join(info) + '\n\n'
    if issues:
        response += f"### Issues Found ({len(issues)})\n\n"
        for issue in issues:
            response += f"- {issue}\n"
    else:
        response += "### No Issues Found\n\nThe code looks clean! No common issues detected.\n"

    if functions:
        response += f"\n### Functions/Methods Detected\n\n"
        for f in functions[:10]:
            response += f"- `{f.strip()}`\n"

    return response


def _mock_explain(code, language):
    """Pattern-based code explanation."""
    lines = code.strip().split('\n')
    response = f"## Code Explanation ({language.title()})\n\n"

    # Overall summary
    functions = [l for l in lines if re.match(r'\s*(def |function )', l)]
    classes = [l for l in lines if re.match(r'\s*class ', l)]

    if classes:
        response += f"This code defines **{len(classes)} class(es)** "
    if functions:
        response += f"{'and ' if classes else 'This code defines '}"
        response += f"**{len(functions)} function(s)**.\n\n"
    elif not classes:
        response += "This is a script-style program.\n\n"
    else:
        response += ".\n\n"

    response += "### Line-by-Line Breakdown\n\n"

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue

        explanation = ""
        if stripped.startswith('#') or stripped.startswith('//'):
            explanation = "Comment — " + stripped.lstrip('#/ ').strip()
        elif re.match(r'(import |from .+ import)', stripped):
            module = stripped.split('import')[-1].strip().split()[0]
            explanation = f"Imports the `{module}` module for use in the program"
        elif re.match(r'(def |function )', stripped):
            name = re.search(r'(def|function)\s+(\w+)', stripped)
            if name:
                explanation = f"Defines a function called `{name.group(2)}`"
        elif re.match(r'class ', stripped):
            name = re.search(r'class\s+(\w+)', stripped)
            if name:
                explanation = f"Defines a class called `{name.group(1)}`"
        elif re.match(r'(for |while )', stripped):
            explanation = "Loop — iterates over a sequence or condition"
        elif re.match(r'if ', stripped):
            explanation = "Conditional check — executes the following block if the condition is true"
        elif re.match(r'elif ', stripped):
            explanation = "Alternative condition — checked if the previous `if` was false"
        elif re.match(r'else', stripped):
            explanation = "Default case — executes if no previous conditions were true"
        elif re.match(r'return ', stripped):
            explanation = "Returns a value from the function"
        elif 'print(' in stripped or 'console.log(' in stripped:
            explanation = "Outputs/prints a value to the console"
        elif '=' in stripped and not stripped.startswith('='):
            var_name = stripped.split('=')[0].strip()
            explanation = f"Assigns a value to `{var_name}`"
        else:
            explanation = "Statement execution"

        if explanation:
            response += f"**Line {i}:** `{stripped[:60]}{'...' if len(stripped) > 60 else ''}`\n"
            response += f"  - {explanation}\n\n"

    return response


def _mock_refactor(code, language):
    """Suggest refactoring improvements."""
    lines = code.strip().split('\n')
    suggestions = []
    improved_lines = list(lines)

    if language == 'python':
        for i, line in enumerate(lines):
            stripped = line.strip()
            if 'range(len(' in stripped:
                suggestions.append(f"**Line {i+1}:** Replace `range(len(x))` with `enumerate(x)` for cleaner iteration")
            if re.search(r'(\w+)\s*=\s*(\w+)\s*\+\s*(\w+)', stripped) and 'str' not in stripped:
                pass
            if stripped.startswith('def ') and i + 1 < len(lines) and not lines[i + 1].strip().startswith(('"""', "'''")):
                suggestions.append(f"**Line {i+1}:** Function `{stripped}` — add a docstring for documentation")
            if re.match(r'[a-z]\s*=', stripped) and len(stripped.split('=')[0].strip()) == 1:
                suggestions.append(f"**Line {i+1}:** Use a descriptive variable name instead of `{stripped.split('=')[0].strip()}`")
            if 'print(' in stripped and 'f"' not in stripped and "f'" not in stripped and '+' in stripped:
                suggestions.append(f"**Line {i+1}:** Consider using f-strings instead of string concatenation")
            if stripped == 'pass':
                suggestions.append(f"**Line {i+1}:** Empty block with `pass` — implement the logic or add a TODO comment")

        if '"""' not in code and "'''" not in code:
            suggestions.append("**General:** Add module-level docstring at the top of the file")
        if not any(line.strip().startswith('#') for line in lines):
            suggestions.append("**General:** Add inline comments to explain complex logic")

    elif language == 'javascript':
        for i, line in enumerate(lines):
            if 'var ' in line:
                suggestions.append(f"**Line {i+1}:** Replace `var` with `let` or `const`")
            if '==' in line and '===' not in line:
                suggestions.append(f"**Line {i+1}:** Use strict equality `===` instead of `==`")
            if 'function(' in line and '=>' not in line:
                suggestions.append(f"**Line {i+1}:** Consider using arrow function syntax `() =>`")

    response = "## Refactoring Suggestions\n\n"
    if suggestions:
        response += f"Found **{len(suggestions)}** improvement(s):\n\n"
        for s in suggestions:
            response += f"- {s}\n"
        response += "\n### Best Practices\n\n"
        response += "- Use meaningful variable and function names\n"
        response += "- Keep functions small and focused (single responsibility)\n"
        response += "- Add error handling for edge cases\n"
        response += "- Write unit tests for critical functions\n"
    else:
        response += "The code looks well-structured! No major refactoring needed.\n\n"
        response += "### General Tips\n\n"
        response += "- Consider adding type hints (Python) or JSDoc (JavaScript)\n"
        response += "- Ensure consistent code formatting\n"
        response += "- Add error handling where appropriate\n"

    return response


# --- Code generation snippets ---
CODE_SNIPPETS = {
    'python': {
        'hello world': 'print("Hello, World!")',
        'factorial': '''def factorial(n):
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Example usage
print(factorial(5))  # Output: 120''',
        'fibonacci': '''def fibonacci(n):
    """Generate first n Fibonacci numbers."""
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib[:n]

# Example usage
print(fibonacci(10))  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]''',
        'prime': '''def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Example usage
for num in range(1, 20):
    if is_prime(num):
        print(f"{num} is prime")''',
        'sort': '''def bubble_sort(arr):
    """Sort a list using bubble sort algorithm."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Example usage
numbers = [64, 34, 25, 12, 22, 11, 90]
print(f"Sorted: {bubble_sort(numbers)}")''',
        'binary search': '''def binary_search(arr, target):
    """Search for target in sorted array."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Example usage
numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(numbers, 23))  # Output: 5''',
        'linked list': '''class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements))

# Example usage
ll = LinkedList()
for val in [1, 2, 3, 4, 5]:
    ll.append(val)
ll.display()  # Output: 1 -> 2 -> 3 -> 4 -> 5''',
        'stack': '''class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Stack is empty")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("Stack is empty")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

# Example usage
stack = Stack()
for val in [10, 20, 30]:
    stack.push(val)
print(f"Top: {stack.peek()}")   # Output: 30
print(f"Pop: {stack.pop()}")    # Output: 30
print(f"Size: {stack.size()}")  # Output: 2''',
        'calculator': '''def calculator():
    """Simple calculator with basic operations."""
    print("Simple Calculator")
    print("Operations: +, -, *, /")

    num1 = float(input("Enter first number: "))
    op = input("Enter operation (+, -, *, /): ")
    num2 = float(input("Enter second number: "))

    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
    elif op == '*':
        result = num1 * num2
    elif op == '/':
        result = num1 / num2 if num2 != 0 else "Error: Division by zero"
    else:
        result = "Invalid operation"

    print(f"Result: {num1} {op} {num2} = {result}")

calculator()''',
        'fizzbuzz': '''def fizzbuzz(n):
    """Classic FizzBuzz problem."""
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

fizzbuzz(20)''',
        'palindrome': '''def is_palindrome(text):
    """Check if a string is a palindrome."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

# Example usage
words = ["racecar", "hello", "madam", "python", "level"]
for word in words:
    result = "is" if is_palindrome(word) else "is not"
    print(f"\\"{word}\\" {result} a palindrome")''',
        'class': '''class Student:
    """Student class with basic attributes and methods."""

    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def is_passing(self):
        return self.grade >= 60

    def __str__(self):
        status = "Passing" if self.is_passing() else "Failing"
        return f"{self.name} (Age: {self.age}, Grade: {self.grade}, {status})"

# Example usage
students = [
    Student("Alice", 20, 85),
    Student("Bob", 19, 55),
    Student("Charlie", 21, 92)
]

for student in students:
    print(student)''',
        'matrix': '''def matrix_multiply(A, B):
    """Multiply two matrices."""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError("Incompatible matrix dimensions")

    result = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

# Example
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
result = matrix_multiply(A, B)
for row in result:
    print(row)''',
        'dictionary': '''# Count word frequency in text
text = "the quick brown fox jumps over the lazy dog the fox"
words = text.split()

frequency = {}
for word in words:
    frequency[word] = frequency.get(word, 0) + 1

# Sort by frequency
sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

print("Word Frequency:")
for word, count in sorted_freq:
    print(f"  {word}: {count}")''',
        'decorator': '''import time

def timer(func):
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total

result = slow_function(1000000)
print(f"Result: {result}")''',
        'list comprehension': '''# List comprehension examples
numbers = list(range(1, 21))

# Squares of even numbers
even_squares = [x**2 for x in numbers if x % 2 == 0]
print(f"Even squares: {even_squares}")

# Flatten nested list
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flat = [x for sublist in nested for x in sublist]
print(f"Flattened: {flat}")

# Dictionary comprehension
word_lengths = {word: len(word) for word in ["hello", "world", "python"]}
print(f"Word lengths: {word_lengths}")''',
    },
    'javascript': {
        'hello world': 'console.log("Hello, World!");',
        'factorial': '''function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(factorial(5)); // Output: 120''',
        'fibonacci': '''function fibonacci(n) {
    const fib = [0, 1];
    for (let i = 2; i < n; i++) {
        fib.push(fib[i-1] + fib[i-2]);
    }
    return fib.slice(0, n);
}

console.log(fibonacci(10));''',
        'class': '''class Animal {
    constructor(name, sound) {
        this.name = name;
        this.sound = sound;
    }

    speak() {
        return `${this.name} says ${this.sound}!`;
    }
}

const dog = new Animal("Dog", "Woof");
const cat = new Animal("Cat", "Meow");
console.log(dog.speak());
console.log(cat.speak());''',
    },
    'java': {
        'hello world': '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
        'factorial': '''public class Factorial {
    public static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    public static void main(String[] args) {
        System.out.println("5! = " + factorial(5));
    }
}''',
    },
    'cpp': {
        'hello world': '''#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}''',
        'fibonacci': '''#include <iostream>
using namespace std;

int main() {
    int n = 10, a = 0, b = 1;
    cout << "Fibonacci: ";
    for (int i = 0; i < n; i++) {
        cout << a << " ";
        int temp = a + b;
        a = b;
        b = temp;
    }
    cout << endl;
    return 0;
}''',
    },
}


def _mock_generate(prompt, language):
    """Generate code from a prompt using keyword matching."""
    prompt_lower = prompt.lower().strip()
    lang_snippets = CODE_SNIPPETS.get(language, CODE_SNIPPETS.get('python', {}))

    # Direct match
    for key, code in lang_snippets.items():
        if key in prompt_lower:
            return f"## Generated Code\n\n**Task:** {prompt}\n**Language:** {language.title()}\n\n```{language}\n{code}\n```"

    # Keyword matching
    keywords = {
        'sort': 'sort', 'search': 'binary search', 'prime': 'prime',
        'fib': 'fibonacci', 'fact': 'factorial', 'hello': 'hello world',
        'stack': 'stack', 'queue': 'stack', 'link': 'linked list',
        'calc': 'calculator', 'fizz': 'fizzbuzz', 'palindrome': 'palindrome',
        'class': 'class', 'object': 'class', 'matrix': 'matrix',
        'dict': 'dictionary', 'count': 'dictionary', 'frequency': 'dictionary',
        'decor': 'decorator', 'timer': 'decorator',
        'list comp': 'list comprehension', 'comprehension': 'list comprehension',
    }

    for keyword, snippet_key in keywords.items():
        if keyword in prompt_lower and snippet_key in lang_snippets:
            code = lang_snippets[snippet_key]
            return f"## Generated Code\n\n**Task:** {prompt}\n**Language:** {language.title()}\n\n```{language}\n{code}\n```"

    # Fallback
    default_code = lang_snippets.get('hello world', '# No snippet available for this prompt')
    return (f"## Generated Code\n\n**Task:** {prompt}\n**Language:** {language.title()}\n\n"
            f"*No exact match found. Here's a starter template:*\n\n"
            f"```{language}\n{default_code}\n```\n\n"
            f"*Tip: Try prompts like \"factorial\", \"fibonacci\", \"sorting\", \"linked list\", "
            f"\"binary search\", \"stack\", \"calculator\", \"palindrome\", \"class\", or \"fizzbuzz\".*")


# --- Public API ---
def ai_assist(code, language, action, prompt=''):
    """
    Main entry point for AI assistance.
    action: 'analyze' | 'explain' | 'refactor' | 'generate'
    """
    mode = get_mode()

    if mode == 'real':
        if action == 'analyze':
            tmpl = LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS['python'])
            full_prompt = tmpl.format(code=code)
        elif action == 'explain':
            full_prompt = EXPLAIN_PROMPT.format(language=language, code=code)
        elif action == 'refactor':
            full_prompt = REFACTOR_PROMPT.format(language=language, code=code)
        elif action == 'generate':
            full_prompt = GENERATE_PROMPT.format(language=language, prompt=prompt)
        else:
            return "Unknown action."
        return _call_gemini(full_prompt)

    # Mock mode
    time.sleep(0.3)  # Simulate API delay

    if action == 'analyze':
        return _mock_analyze(code, language)
    elif action == 'explain':
        return _mock_explain(code, language)
    elif action == 'refactor':
        return _mock_refactor(code, language)
    elif action == 'generate':
        return _mock_generate(prompt or 'hello world', language)
    else:
        return "Unknown action."
