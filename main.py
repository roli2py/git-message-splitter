from sys import exit
from pathlib import Path


class Main:

    def __init__(self, text_path: Path) -> None:
        self.__text_path = text_path
    
    def __ensure_file(self) -> None:
        self.__text_path.open("w", encoding="utf-8").close()

    def __get_text(self) -> str:
        try:
            with self.__text_path.open(encoding="utf-8") as text_file:
                text = text_file.read()
        except OSError:
            not_found_text = (f"{self.__text_path.name} not found. Please, "
                              "restart the program.")
            print(not_found_text)
            input("Press enter to close the program...\n")
            exit(1)
        if not text:
            empty_text = (
                f"{self.__text_path.name} is empty. Please, restart the "
                f"program and put your message into the "
                f"{self.__text_path.name} file."
            )
            print(empty_text)
            input("Press enter to close the program...\n")
            exit(1)
        return text

    @staticmethod
    def __format_text(text: str) -> str:
        chars = list(text)
        reset_chars = (
            "\n",
            "\r",
            "\r\n",
            "\v",
            "\f",
            "\x1c",
            "\x1d",
            "\x1e",
            "\x85",
            "\u2028",
            "\u2029",
        )

        limit = 72
        count = 0
        last_space_index = None
        for index, char in enumerate(chars):
            if char in reset_chars:
                last_space_index = None
                count = 0
                continue
            count += len(char)
            if char == " ":
                last_space_index = index
            if count > limit:
                if last_space_index is None:
                    chars[index] = char + "\n"
                else:
                    chars[last_space_index] = "\n"
                count = index - last_space_index

        formatted_text = "".join(chars)

        return formatted_text

    def __write_text_to_file(self, text: str) -> None:
        with self.__text_path.open("w", encoding="utf-8") as text_file:
            text_file.write(text)
        message_formatted_text = (
            "Message successfully formatted and written to"
            f" {self.__text_path.name}"
        )
        print(message_formatted_text)

    def start(self) -> None:
        self.__ensure_file()

        put_text = (
            "Put your Git message into the message.txt file.\n"
            "When you're ready, press enter.\n"
        )
        input(put_text)

        message = self.__get_text()
        formatted_message = self.__format_text(message)
        self.__write_text_to_file(formatted_message)

        print("Done!")
        input("Press enter to close the program...\n")


if __name__ == "__main__":
    text_path = Path("message.txt")
    main = Main(text_path)
    main.start()
