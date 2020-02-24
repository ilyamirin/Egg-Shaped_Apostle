import argparse
import yaml
#import os
#os.chdir('./cloudapi/output/')
import grpc
import socket
import yandex.cloud.ai.stt.v2.stt_service_pb2 as stt_service_pb2
import yandex.cloud.ai.stt.v2.stt_service_pb2_grpc as stt_service_pb2_grpc

with open('api-key.yaml') as file:
    api_key = yaml.load(file, Loader=yaml.FullLoader)['secret']

folder_id = 'b1gs8d8gurpgig5h56km'

chunk_size = 1024
s_ip = '127.0.0.1'
s_port = 12345
s_addr = (s_ip, s_port)

s = socket.socket()
s.connect(s_addr)


def gen(folder_id):
    # Задать настройки распознавания.
    specification = stt_service_pb2.RecognitionSpec(
        language_code='ru-RU',
        profanity_filter=False,
        model='general',
        partial_results=True,
        audio_encoding='LINEAR16_PCM',
        sample_rate_hertz=48000
    )
    streaming_config = stt_service_pb2.RecognitionConfig(specification=specification, folder_id=folder_id)

    # Отправить сообщение с настройками распознавания.
    yield stt_service_pb2.StreamingRecognitionRequest(config=streaming_config)

    n = 0
    while n < 30:
        data = b''
        for i in range(0, int(48000 / 1024 * 1)):
            data += s.recv(1024)
        #data += s.recv(chunk_size)
        yield stt_service_pb2.StreamingRecognitionRequest(audio_content=data)
        n += 1

'''    # Прочитать аудиофайл и отправить его содержимое порциями.
    with open(audio_file_name, 'rb') as f:
        data = f.read(CHUNK_SIZE)
        while data != b'':
            yield stt_service_pb2.StreamingRecognitionRequest(audio_content=data)
            data = f.read(CHUNK_SIZE)'''

def run(folder_id):
    # Установить соединение с сервером.
    cred = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('stt.api.cloud.yandex.net:443', cred)
    stub = stt_service_pb2_grpc.SttServiceStub(channel)

    # Отправить данные для распознавания.
    it = stub.StreamingRecognize(gen(folder_id), metadata=(('authorization', 'Api-key %s' % api_key),))
    # Обработать ответы сервера и вывести результат в консоль.
    try:
        for r in it:
            try:
                print('Start chunk: ')
                for alternative in r.chunks[0].alternatives:
                    print('alternative: ', alternative.text)
                print('Is final: ', r.chunks[0].final)
                print('')
            except LookupError:
                print('Not available chunks')
    except grpc._channel._Rendezvous as err:
        print('Error code %s, message: %s' % (err._state.code, err._state.details))
    s.close()

run(folder_id)