import re
import os

def check_currency(text):
    pattern = re.compile(r'^\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?$|^\$\d+(?:\.\d{2})?$')
    return bool(pattern.fullmatch(text.strip()))

def check_phone(text):
    pattern = re.compile(r'^(\+\d{1,3}[\s.-]?)?(\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}$')
    return bool(pattern.fullmatch(text.strip()))

def check_html_tag(text):
    pattern = re.compile(
        r'^<\/?[a-zA-Z][a-zA-Z0-9]*(\s+[a-zA-Z_:][-a-zA-Z0-9_:.]*=(["\'])[^\2]*?\2)*\s*\/?>$'
    )
    return bool(pattern.fullmatch(text.strip()))

def check_url(text):
    pattern = re.compile(
        r'^https?://([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(/[^\s]*)?(\?[^\s]*)?(#[^\s]*)?$'
    )
    return bool(pattern.fullmatch(text.strip()))

def check_email(text):
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.fullmatch(text.strip()))

def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def ensure_output_folder():
    os.makedirs("output", exist_ok=True)

def process_file(file_path, validator, label):
    ensure_output_folder()

    valid_output = os.path.join("output", f"extracted_{label.replace(' ', '_')}.txt")
    invalid_output = os.path.join("output", f"invalid_{label.replace(' ', '_')}.txt")

    valid_count = 0
    invalid_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as infile, \
             open(valid_output, 'w', encoding='utf-8') as valid_file, \
             open(invalid_output, 'w', encoding='utf-8') as invalid_file:

            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue
                if validator(line):
                    valid_file.write(line + '\n')
                    print(f"Line {line_num}: {color_text('✅', '92')} '{line}'")
                    valid_count += 1
                else:
                    invalid_file.write(line + '\n')
                    print(f"Line {line_num}: {color_text('❌', '91')} '{line}'")
                    invalid_count += 1

        total = valid_count + invalid_count
        print(f"\n{color_text('📄 Total lines processed:', '96')} {total}")
        print(f"{color_text('✅ Valid entries:', '92')} {valid_count} ➜ {valid_output}")
        print(f"{color_text('❌ Invalid entries:', '91')} {invalid_count} ➜ {invalid_output}\n")

    except FileNotFoundError:
        print(color_text("❌ File not found. Please check the path.\n", "91"))

def main():
    print("\n" + "\t" * 2 + color_text("Welcome To The Regex Pattern Finder & Checker!\n", "94"))

    menu = [
        "Check Currency Amount From currency.txt",
        "Check Phone Number From phones.txt",
        "Check HTML Tag From htmltags.txt",
        "Check Email Address From emails.txt",
        "Check URL Address From urls.txt",
        "Check All Files",
        "Close The Program"
    ]

    validators = [
        ("currency amount", check_currency),
        ("phone number", check_phone),
        ("HTML tag", check_html_tag),
        ("email address", check_email),
        ("URL address", check_url),
    ]

    file_paths = {
        "currency amount": "currency.txt",
        "phone number": "phones.txt",
        "HTML tag": "htmltags.txt",
        "email address": "emails.txt",
        "URL address": "urls.txt",
    }

    while True:
        for idx, item in enumerate(menu, 1):
            print(f"{idx}. {item}")
        print()

        try:
            choice = int(input("Please select an option from the menu (1-7): "))
        except ValueError:
            print(color_text("\n❌ Invalid input! Please enter a number between 1 and 7.\n", "91"))
            continue

        if 1 <= choice <= 5:
            label, validator = validators[choice - 1]
            file_path = file_paths[label]
            process_file(file_path, validator, label)
        elif choice == 6:
            print(color_text("\n🔁 Processing all files...\n", "96"))
            for label, validator in validators:
                file_path = file_paths[label]
                process_file(file_path, validator, label)
        elif choice == 7:
            print(color_text("\nThank you for using the Regex Pattern Finder & Checker. Goodbye!\n", "92"))
            break
        else:
            print(color_text("\n❌ Invalid choice! Please select a number between 1 and 7.\n", "91"))

if __name__ == '__main__':
    main()

