def greeting():
    print("Hello, world!")

def calculate_pi(digits=5):
    """
    Calculate the value of pi to the specified number of digits.
    Uses the Nilakantha series which converges relatively quickly.
    
    Args:
        digits: Number of decimal digits of precision (default=5)
        
    Returns:
        float: The value of pi calculated to the specified precision
    """
    # For 5 digits of precision, we need more iterations to ensure accuracy
    iterations = 1000
    
    # Start with the base value of pi according to the series
    pi = 3.0
    
    # Flag to determine whether to add or subtract the next term
    add = True
    
    # Calculate using Nilakantha series: π = 3 + 4/(2×3×4) - 4/(4×5×6) + 4/(6×7×8) - ...
    for i in range(2, iterations * 2, 2):
        denominator = i * (i + 1) * (i + 2)
        if add:
            pi += 4 / denominator
        else:
            pi -= 4 / denominator
        add = not add
    
    # Round to the specified number of digits
    return round(pi, digits)

# Example usage
if __name__ == "__main__":
    pi_value = calculate_pi()
    print(f"Pi to the 5th digit is: {pi_value}")