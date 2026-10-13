import json
import random
from datetime import datetime

# ==========================================
# FILE NAMES
# ==========================================

QUESTIONS_FILE = "questions.json"
USERS_FILE = "users.json"
RESULTS_FILE = "results.json"
LEADERBOARD_FILE = "leaderboard.json"


# ==========================================
# JSON FILE FUNCTIONS
# ==========================================

def load_data(filename):
    """
    JSON file se data read karta hai.
    Agar file exist nahi karti to empty list return karta hai.
    """

    try:
        with open(filename, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print(f"Error: {filename} mein invalid JSON data hai.")
        return []


def save_data(filename, data):
    """
    Data ko JSON file mein save karta hai.
    """

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# ==========================================
# REGISTER
# ==========================================

def register():

    print("\n========== REGISTER ==========")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username == "" or password == "":
        print("Username and password cannot be empty.")
        return

    users = load_data(USERS_FILE)

    # Check username already exists
    for user in users:

        if user["username"] == username:
            print("Username already exists.")
            return

    # Create new user
    new_user = {
        "username": username,
        "password": password
    }

    users.append(new_user)

    save_data(USERS_FILE, users)

    print("Registration successful!")


# ==========================================
# LOGIN
# ==========================================

def login():

    print("\n========== LOGIN ==========")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    users = load_data(USERS_FILE)

    for user in users:

        if (
            user["username"] == username
            and user["password"] == password
        ):

            print(f"\nWelcome, {username}!")

            return username

    print("Invalid username or password.")

    return None


# ==========================================
# LOAD QUESTIONS
# ==========================================

def load_questions():

    questions = load_data(QUESTIONS_FILE)

    return questions


# ==========================================
# GET DIFFICULTIES
# ==========================================

def get_difficulties(questions):

    difficulties = []

    for question in questions:

        difficulty = question["difficulty"]

        if difficulty not in difficulties:
            difficulties.append(difficulty)

    return difficulties


# ==========================================
# START QUIZ
# ==========================================

def start_quiz(username):

    questions = load_questions()

    if len(questions) == 0:

        print("\nNo Python questions available.")

        return

    print("\n================================")
    print("         PYTHON QUIZ")
    print("================================")

    # --------------------------------------
    # DIFFICULTY
    # --------------------------------------

    difficulties = get_difficulties(questions)

    print("\nAvailable Difficulties:")

    for i, difficulty in enumerate(
        difficulties,
        start=1
    ):

        print(f"{i}. {difficulty}")

    print("0. All Difficulties")

    try:

        choice = int(
            input("Choose difficulty: ")
        )

    except ValueError:

        print("Please enter a number.")

        return

    if choice == 0:

        selected_difficulty = "All"

    elif 1 <= choice <= len(difficulties):

        selected_difficulty = difficulties[
            choice - 1
        ]

    else:

        print("Invalid choice.")

        return

    # --------------------------------------
    # FILTER QUESTIONS
    # --------------------------------------

    filtered_questions = []

    for question in questions:

        difficulty_match = (
            selected_difficulty == "All"
            or question["difficulty"]
            == selected_difficulty
        )

        if difficulty_match:

            filtered_questions.append(question)

    if len(filtered_questions) == 0:

        print("No questions found.")

        return

    # --------------------------------------
    # NUMBER OF QUESTIONS
    # --------------------------------------

    print(
        f"\nAvailable questions: "
        f"{len(filtered_questions)}"
    )

    try:

        number = int(
            input("How many questions? ")
        )

    except ValueError:

        print("Please enter a number.")

        return

    if number <= 0:

        print("Number must be greater than 0.")

        return

    if number > len(filtered_questions):

        number = len(filtered_questions)

        print(
            f"Only {number} questions available."
        )

    # --------------------------------------
    # RANDOM QUESTIONS
    # --------------------------------------

    selected_questions = random.sample(
        filtered_questions,
        number
    )

    score = 0

    # --------------------------------------
    # ASK QUESTIONS
    # --------------------------------------

    for i, question in enumerate(
        selected_questions,
        start=1
    ):

        print("\n")
        print("--------------------------------")
        print(f"Question {i}/{number}")
        print("--------------------------------")

        print(question["question"])

        options = question["options"]

        for index, option in enumerate(
            options,
            start=1
        ):

            print(f"{index}. {option}")

        # ----------------------------------
        # USER ANSWER
        # ----------------------------------

        while True:

            answer = input(
                "Your answer (1-4): "
            ).strip()

            if answer in ["1", "2", "3", "4"]:
                break

            print(
                "Please enter a number "
                "between 1 and 4."
            )

        answer = int(answer)

        # ----------------------------------
        # CHECK ANSWER
        # ----------------------------------

        if answer == question["answer"]:

            print("Correct!")

            score += 1

        else:

            correct_answer_number = (
                question["answer"]
            )

            correct_answer = options[
                correct_answer_number - 1
            ]

            print("Wrong!")

            print(
                f"Correct answer: "
                f"{correct_answer}"
            )

    # --------------------------------------
    # RESULT
    # --------------------------------------

    percentage = (
        score / number
    ) * 100

    print("\n")
    print("================================")
    print("          QUIZ RESULT")
    print("================================")

    print(f"Username   : {username}")
    print(f"Subject    : Python")
    print(f"Difficulty : {selected_difficulty}")
    print(f"Score      : {score}/{number}")
    print(f"Percentage : {percentage:.2f}%")

    print("================================")

    # --------------------------------------
    # SAVE RESULT
    # --------------------------------------

    save_result(
        username,
        selected_difficulty,
        score,
        number,
        percentage
    )

    # --------------------------------------
    # SAVE LEADERBOARD
    # --------------------------------------

    save_leaderboard(
        username,
        score,
        number,
        percentage
    )


# ==========================================
# SAVE RESULT
# ==========================================

def save_result(
    username,
    difficulty,
    score,
    total,
    percentage
):

    results = load_data(RESULTS_FILE)

    date = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    result = {

        "username": username,

        "subject": "Python",

        "difficulty": difficulty,

        "score": score,

        "total": total,

        "percentage": round(
            percentage,
            2
        ),

        "date": date
    }

    results.append(result)

    save_data(
        RESULTS_FILE,
        results
    )


# ==========================================
# SAVE LEADERBOARD
# ==========================================

def save_leaderboard(
    username,
    score,
    total,
    percentage
):

    leaderboard = load_data(
        LEADERBOARD_FILE
    )

    date = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    record = {

        "username": username,

        "subject": "Python",

        "score": score,

        "total": total,

        "percentage": round(
            percentage,
            2
        ),

        "date": date
    }

    leaderboard.append(record)

    save_data(
        LEADERBOARD_FILE,
        leaderboard
    )


# ==========================================
# SHOW LEADERBOARD
# ==========================================

def show_leaderboard():

    print("\n========== PYTHON LEADERBOARD ==========")

    leaderboard = load_data(
        LEADERBOARD_FILE
    )

    if len(leaderboard) == 0:

        print("No scores available.")

        return

    # Sort by percentage
    leaderboard.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )

    print()

    print(
        f"{'Rank':<6}"
        f"{'Username':<15}"
        f"{'Score':<10}"
        f"{'Percentage':<12}"
    )

    print("-" * 43)

    for rank, record in enumerate(
        leaderboard,
        start=1
    ):

        print(
            f"{rank:<6}"
            f"{record['username']:<15}"
            f"{record['score']}/{record['total']:<7}"
            f"{record['percentage']}%"
        )


# ==========================================
# SHOW MY RESULTS
# ==========================================

def show_my_results(username):

    print("\n========== MY PYTHON RESULTS ==========")

    results = load_data(
        RESULTS_FILE
    )

    found = False

    for result in results:

        if result["username"] == username:

            found = True

            print("\n------------------------")

            print(
                f"Date       : "
                f"{result['date']}"
            )

            print(
                f"Subject    : "
                f"{result['subject']}"
            )

            print(
                f"Difficulty : "
                f"{result['difficulty']}"
            )

            print(
                f"Score      : "
                f"{result['score']}/"
                f"{result['total']}"
            )

            print(
                f"Percentage : "
                f"{result['percentage']}%"
            )

    if not found:

        print(
            "You have not attempted "
            "any Python quiz yet."
        )


# ==========================================
# ADMIN - ADD PYTHON QUESTION
# ==========================================

def add_question():

    print("\n========== ADD PYTHON QUESTION ==========")

    question_text = input(
        "Question: "
    ).strip()

    if question_text == "":
        print("Question cannot be empty.")
        return

    # --------------------------------------
    # OPTIONS
    # --------------------------------------

    option1 = input(
        "Option 1: "
    ).strip()

    option2 = input(
        "Option 2: "
    ).strip()

    option3 = input(
        "Option 3: "
    ).strip()

    option4 = input(
        "Option 4: "
    ).strip()

    if (
        option1 == ""
        or option2 == ""
        or option3 == ""
        or option4 == ""
    ):

        print("Options cannot be empty.")

        return

    # --------------------------------------
    # CORRECT ANSWER
    # --------------------------------------

    while True:

        try:

            answer = int(
                input(
                    "Correct option (1-4): "
                )
            )

            if 1 <= answer <= 4:
                break

            print(
                "Please enter 1, 2, 3 or 4."
            )

        except ValueError:

            print("Please enter a number.")

    # --------------------------------------
    # DIFFICULTY
    # --------------------------------------

    while True:

        difficulty = input(
            "Difficulty (Easy/Medium/Hard): "
        ).strip().capitalize()

        if difficulty in [
            "Easy",
            "Medium",
            "Hard"
        ]:

            break

        print(
            "Please enter Easy, Medium or Hard."
        )

    # --------------------------------------
    # LOAD QUESTIONS
    # --------------------------------------

    questions = load_questions()

    # --------------------------------------
    # GENERATE NEW ID
    # --------------------------------------

    if len(questions) == 0:

        new_id = 1

    else:

        new_id = max(
            question["id"]
            for question in questions
        ) + 1

    # --------------------------------------
    # NEW QUESTION
    # --------------------------------------

    new_question = {

        "id": new_id,

        "question": question_text,

        "options": [
            option1,
            option2,
            option3,
            option4
        ],

        "answer": answer,

        "difficulty": difficulty,

        "subject": "Python"
    }

    questions.append(new_question)

    save_data(
        QUESTIONS_FILE,
        questions
    )

    print("\nPython question added successfully!")


# ==========================================
# ADMIN - VIEW QUESTIONS
# ==========================================

def view_questions():

    print("\n========== PYTHON QUESTIONS ==========")

    questions = load_questions()

    if len(questions) == 0:

        print("No questions available.")

        return

    for question in questions:

        print("\n--------------------------------")
        print(f"ID         : {question['id']}")
        print(f"Question   : {question['question']}")
        print(f"Difficulty : {question['difficulty']}")

        for index, option in enumerate(
            question["options"],
            start=1
        ):

            print(f"{index}. {option}")


# ==========================================
# ADMIN LOGIN
# ==========================================

def admin_login():

    print("\n========== ADMIN LOGIN ==========")

    username = input(
        "Admin username: "
    ).strip()

    password = input(
        "Admin password: "
    ).strip()

    # Demo credentials
    if (
        username == "admin"
        and password == "admin123"
    ):

        print("Admin login successful!")

        admin_menu()

    else:

        print("Invalid admin credentials.")


# ==========================================
# ADMIN MENU
# ==========================================

def admin_menu():

    while True:

        print("\n================================")
        print("          ADMIN MENU")
        print("================================")

        print("1. Add Python Question")
        print("2. View Questions")
        print("3. View Leaderboard")
        print("4. Logout")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            add_question()

        elif choice == "2":

            view_questions()

        elif choice == "3":

            show_leaderboard()

        elif choice == "4":

            print("Admin logged out.")

            break

        else:

            print("Invalid choice.")


# ==========================================
# USER MENU
# ==========================================

def user_menu(username):

    while True:

        print("\n================================")
        print("           USER MENU")
        print("================================")

        print("1. Start Python Quiz")
        print("2. My Results")
        print("3. Leaderboard")
        print("4. Logout")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            start_quiz(username)

        elif choice == "2":

            show_my_results(username)

        elif choice == "3":

            show_leaderboard()

        elif choice == "4":

            print("Logged out successfully.")

            break

        else:

            print("Invalid choice.")


# ==========================================
# MAIN MENU
# ==========================================

def main():

    while True:

        print("\n")
        print("================================")
        print("       PYTHON QUIZ APPLICATION")
        print("================================")

        print("1. Register")
        print("2. Login")
        print("3. Admin Login")
        print("4. Exit")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            register()

        elif choice == "2":

            username = login()

            if username:

                user_menu(username)

        elif choice == "3":

            admin_login()

        elif choice == "4":

            print(
                "\nThank you for using "
                "Python Quiz Application!"
            )

            break

        else:

            print("Invalid choice.")


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":

    main()
