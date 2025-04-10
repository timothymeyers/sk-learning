import sys

def main():
    print("Welcome to the Backend Driver Console App!")
    print("Type 'exit' to quit.")

    while True:
        command = input("Enter a command: ")
        if command.lower() == 'exit':
            print("Exiting the app. Goodbye!")
            break
        else:
            print(f"You entered: {command}")

if __name__ == "__main__":
    main()