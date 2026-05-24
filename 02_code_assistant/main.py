def is_palindrome(text):
    # Convert to lowercase
    text = text.lower()

    # Remove spaces
    text = text.replace(" ", "")

    # Check if text is same as reverse
    return text == text[::-1]
    
if __name__ == "__main__":
    user_input = input("Enter a word or sentence: ")

    if is_palindrome(user_input):
        print("It is a palindrome.")
    else:
        print("It is not a palindrome.")
