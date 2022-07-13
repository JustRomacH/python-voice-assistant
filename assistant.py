import pyttsx3
import os
import speech_recognition as sr
from termcolor import cprint


def create_assist() -> pyttsx3.Engine:
    assist = pyttsx3.init()

    evg_ru = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Evgeniy-Rus"

    assist.setProperty("volume", 0.01)
    assist.setProperty("voice", evg_ru)

    return assist


class Voice_assistant:

    def __init__(self):

        self.assist = create_assist()
        self.stop_commands = ["стоп", "хватит", "прекращай", "замолчи"]
        self.commands = {
            "repeat": ["скажи", "повтори", "repeat"],
            "create_task": ["задача", "создать задачу", "заметка", "записка"],
            "shutdown_pc": ["выключай", "выключи пк", "выключи комп"],
            "reload_pc": ["перезагрузка", "перезагрузи пк", "перезагрузи комп", "перезагрузи"]
        }

    # Say that user said
    def say(self, text):
        self.assist.say(text)

        self.assist.runAndWait()

    # Reloads your pc
    def reload_pc(self):
        os.system('shutdown -r -t 0')

    # Turns off your PC
    def shutdown_pc(self):
        os.system('shutdown -s -t 0')

    # Repeats after user
    def repeat(self):
        print("Скажи, что повторить")
        self.assist.say(self.get_user_text())

        self.assist.runAndWait()

    # Returns a string with what the user said
    def get_user_text(self) -> str:

        r = sr.Recognizer()
        r.pause_threshold = 0.75
        try:
            with sr.Microphone(device_index=1) as mic:
                r.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = r.listen(mic)

            query = r.recognize_google(audio, language="ru-RU")

            return query

        except sr.UnknownValueError as ex:
            return "Не понял что ты сказал"

        except Exception as ex:
            cprint(f"[ERROR] {repr(ex)}", "red")

    # Creates task in todo_list.txt
    def create_task(self):
        print("Скажи, что записать")
        # say("Скажи, что записать")
        task = self.get_user_text()
        if task != "Не понял что ты сказал":
            with open("todo_list.txt", "a", encoding="utf-8") as f:
                f.write(f"{task}\n")
            print(f"Задача {task} успешно записана")
        else:
            self.say("Не понял что ты сказал")
            self.create_task()

    # Starts assistant
    def start(self) -> None:
        while True:
            command = self.get_user_text()

            for key, value in self.commands.items():
                if command in value:
                    # Calls function by key in commands dict
                    globals()[key]()

                elif command in self.stop_commands:
                    self.say("Пока")
                    return


if __name__ == "__main__":
    assistant = Voice_assistant()
    assistant.start()
