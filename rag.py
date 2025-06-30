def calculate_sum_and_average():
    # Ask the user to enter the first number
    num1 = float(input("Enter the first number: "))

    # Ask the user to enter the second number
    num2 = float(input("Enter the second number: "))

    # Calculate the sum
    sum_result = num1 + num2

    # Calculate the average
    average = sum_result / 2

    # Print the results
    print("Sum of the two numbers:", sum_result)
    print("Average of the two numbers:", average)


# Call the function
if __name__ == "__main__":
    calculate_sum_and_average()
