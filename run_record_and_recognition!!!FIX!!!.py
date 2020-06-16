import subprocess

from services.audio_service.management import record_by_time
from services.text_service.text_service import add_to_database


#front = subprocess.Popen(f"cd src-front; ng serve", shell=True) #запускаем фронтенд
#back = subprocess.Popen(f"python3 services/fts_service/fts_service.py", shell=True)


def ui():
    print('Чтобы записать аудио с устройства, введите "1 t", где'
          '"t" — время записи,\n'
          'Чтобы распознать аудио, введите 2;\n'
          'Чтобы выйти, введите "exit".\n')

    inp = input().split()

    if len(inp) < 1:
        ui()
    else:
        command, *attrib = inp
        if command == '1':
            record_by_time(0, 0, attrib[0])
        elif command == '2':
            add_to_database()
        elif command == 'exit':
            return True
        else:
            print('Команда не распознана')
    return ui()


if __name__ == '__main__':
    ui()