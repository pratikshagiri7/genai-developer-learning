def is_palindrome(word):
    # Convert word to lowercase for case-insensitive checking
    word = word.lower()

    # Check if word is equal to its reverse
    return word == word[::-1]


# Example usage
if __name__ == "__main__":
    user_input = input("Enter a word: ")
    
    if is_palindrome(user_input):
        print(f"{user_input} is a palindrome.")
    else:
        print(f"{user_input} is not a palindrome.")
