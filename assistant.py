import pyttsx3
import os
import speech_recognition as sr
from termcolor import cprint

stop_commands = ["стоп", "хватит", "прекращай", "замолчи"]
commands = {
    "repeat": ["скажи", "повтори", "repeat"],
    "create_task": ["задача", "создать задачу", "заметка", "записка"],
    "shutdown_pc": ["выключай", "выключи пк", "выключи комп"],
    "reload_pc": ["перезагрузка", "перезагрузи пк", "перезагрузи комп", "перезагрузи"]
}


def say(text):
    assist = pyttsx3.init()

    evg_ru = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Evgeniy-Rus"

    assist.setProperty("volume", 0.01)
    assist.setProperty("voice", evg_ru)
    assist.say(text)

    assist.runAndWait()


def reload_pc():
    os.system('shutdown -r -t 0')


def shutdown_pc():
    os.system('shutdown -s -t 0')


def repeat():
    assist = pyttsx3.init()

    evg_ru = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Evgeniy-Rus"

    assist.setProperty("volume", 0.01)
    assist.setProperty("voice", evg_ru)
    print("Скажи, что повторить")
    assist.say(get_user_text())

    assist.runAndWait()


def get_user_text():
    r = sr.Recognizer()
    r.pause_threshold = 0.75
    try:
        with sr.Microphone(device_index=1) as mic:
            r.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = r.listen(mic)

        query = r.recognize_google(audio, language="ru-RU")

        return(query)

    except sr.UnknownValueError as ex:
        return "Не понял что ты сказал"

    except Exception as ex:
        cprint(f"[ERROR] {repr(ex)}", "red")


def create_task():
    print("Скажи, что записать")
    # say("Скажи, что записать")
    task = get_user_text()
    if task != "Не понял что ты сказал":
        with open("todo_list.txt", "a", encoding="utf-8") as f:
            f.write(f"{task}\n")
        print(f"Задача {task} успешно записана")
    else:
        say("Не понял что ты сказал")
        create_task()


def main():
    while True:
        command = get_user_text()
        for key, value in commands.items():
            if command in value:
                globals()[key]()
            elif command in stop_commands:
                say("Пока")
                return


if __name__ == "__main__":
    main()
