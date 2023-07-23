import os
import time

from excelgpt.api import core


def run(worksheet: str) -> None:
    if worksheet is None or len(worksheet) == 0:
        print("worksheet can't be empty")
        return None

    cnt: int = 0
    human_format: str = "\033[32m{}.[User-{}]: {} \033[0m"
    ai_format: str = "\033[36m{}.[AI-{}]{}s:\n{} \033[0m"

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    log_dir = os.path.join(base_dir, "history")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    chat_file: str = os.path.join(log_dir, "chat-{}.txt".format(int(time.time())))
    print("chat_file name is: {}".format(chat_file))

    with open(chat_file, "w") as fp:
        while True:
            inputs = "\033[31m{}: \033[0m".format("input")
            task: str = input(inputs)
            if task == "quit":
                break

            if task is None or len(task.strip()) == 0:
                continue

            response = core.go(worksheet, task)

            cnt += 1

            start: int = int(time.time())
            q = human_format.format(cnt, start, task)
            fp.write(q)
            fp.write("\n")
            fp.flush()
            end: int = int(time.time())
            a = ai_format.format(cnt, end, end - start, response)

            print(q)
            print(a)

            fp.write(a)
            fp.write("\n")
            fp.flush()
