import json
import asyncio
import websockets
import telegram_send

class Binance:
    '''Подключение к бирже Binance по websocket. Используется асинхронное
    подключение для получения данных по криптовалютным парам, где с помощью
    итератора можно вызывать асинхронный код на любом этапе перебора.'''

    connections = list()
    connections.append('wss://stream.binance.com:9443/stream?streams=btcusdt@trade')
    connections.append('wss://stream.binance.com:9443/stream?streams=ethbtc@trade')
    connections.append('wss://stream.binance.com:9443/stream?streams=dotusdt@trade')
    connections.append('wss://stream.binance.com:9443/stream?streams=ethusdt@trade')

    # Метод подключения и сравнения цен криптопар с conf.json
    async def connect(self, wss):
        async with websockets.connect(wss) as websocket:
            async for message in websocket:
                with open(f"config.json") as second:
                    json_data = json.loads(message)['data']
                    config = json.load(second)
                    # Форматирование данных json для читабельности
                    json_result = {
                        json_data['s']: {
                            'price': json_data['p'],
                        }
                    }
                    print(json_result)
                    result = []
                    # Перебор элементов json binance
                    for binc in json_result.values():
                        result.append(binc)
                        # Перебор элементов json conf.json
                        for conf in config.values():
                            result.append(conf)
                            # Сравнение цен binance с файлом conf.json
                            if binc['price'][:3] == conf['price'][:3]:
                                '''Отправка сообщений в телеграм при 
                                совпадении цен с conf.json.'''
                                telegram_send.send(messages=[
                                                     "Валюта:\t"
                                                     + json_data['s']
                                                     + "\nЦена:\t"
                                                     + json_data['p']
                                                    ])
    # Метод открытия и перебора соединений с websocket
    async def handler(self):
        await asyncio.wait([self.connect(wss) for wss in self.connections])

if __name__ == '__main__':
    handler = Binance()
    asyncio.get_event_loop().run_until_complete(handler.handler())
