# Data Types Demonstration

# -------------------------------
# Numeric Data Types
# -------------------------------

# Integer
num1 = 10

# Float
num2 = 5.5

# Arithmetic operations
sum_result = num1 + num2
product = num1 * num2

print("Integer:", num1)
print("Float:", num2)
print("Sum:", sum_result)
print("Product:", product)

# -------------------------------
# String Data Types
# -------------------------------

# String variables
name = "Vraj"
message = "Hello"

# String concatenation
greeting = message + " " + name

print("Greeting:", greeting)

# String formatting
formatted = f"My name is {name} and sum is {sum_result}"
print("Formatted:", formatted)

# -------------------------------
# Type Mismatch Example
# -------------------------------

num_str = "20"   # string
num_int = 10     # integer

# This would cause error if uncommented:
# result = num_str + num_int

print("String value:", num_str)
print("Integer value:", num_int)

# -------------------------------
# Type Conversion
# -------------------------------

converted = int(num_str) + num_int
print("After conversion:", converted)