import os
import pyttsx3
import speech_recognition as sr
from termcolor import cprint


class Voice_assistant:

    def __init__(self):

        # self.assist = create_assist()
        self.assist = self.__create_assist()
        self.stop_commands = ["стоп", "хватит", "прекращай", "замолчи"]
        self.commands = {
            self.repeat: ["скажи", "повтори", "repeat"],
            self.create_task: ["задача", "создать задачу", "заметка", "записка"],
            self.shutdown_pc: ["выключай", "выключи пк", "выключи комп"],
            self.reload_pc: ["перезагрузка", "перезагрузи пк",
                             "перезагрузи комп", "перезагрузи"]
        }

    # Returns voice assiastant
    def __create_assist(self) -> pyttsx3.Engine:
        assist = pyttsx3.init()

        evg_ru = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Evgeniy-Rus"

        assist.setProperty("volume", 0.01)
        assist.setProperty("voice", evg_ru)

        return assist

    # Say that user said
    def say(self, text: str) -> None:
        self.assist.say(text)

        self.assist.runAndWait()

    # Reloads your pc
    def reload_pc(self) -> None:
        os.system('shutdown -r -t 0')

    # Turns off your PC
    def shutdown_pc(self) -> None:
        os.system('shutdown -s -t 0')

    # Repeats after user
    def repeat(self) -> None:
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
    def create_task(self) -> None:
        print("Скажи, что записать")
        # say("Скажи, что записать")
        match task := self.get_user_text().capitalize():
            case "Не понял что ты сказал":
                self.say("Не понял что ты сказал")
                self.create_task()
            case _:
                with open("todo_list.txt", "a", encoding="utf-8") as f:
                    f.write(f"{task}\n")
                print(f"Задача \"{task}\" успешно записана")

    # Starts assistant
    def start(self) -> None:
        while True:
            command = self.get_user_text()
            for _, value in self.commands.items():
                if command in value:
                    # Calls function by key in commands dict
                    locals()["_"]()

                elif command in self.stop_commands:
                    self.say("Пока")
                    return


if __name__ == "__main__":
    assistant = Voice_assistant()
    assistant.start()
