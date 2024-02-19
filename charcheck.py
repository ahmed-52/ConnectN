def check_line_length(file_path, max_length=80):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if len(line) > max_length:
                print(f"Line {line_number} exceeds {max_length} characters: {line}")

if __name__ == "__main__":
    file_path = input("Enter the path of your code file: ")
    check_line_length(file_path)