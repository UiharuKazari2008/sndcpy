import socket
import threading
import queue
import asyncio
import uuid
import argparse

print('sndcpy Relay Server\n(C)2022 CyberRex')

parser = argparse.ArgumentParser()
parser.add_argument('--sndcpy-host', type=str, default='localhost', help='sndcpy server host')
parser.add_argument('--sndcpy-port', type=int, default=28200, help='sndcpy server port')
parser.add_argument('-p', '--port', type=int, default=28201, help='relay server port number')
parser.add_argument('-b', '--bind', type=str, default='localhost', help='address to bind')

args = parser.parse_args()

sndcpy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sndcpy.connect((args.sndcpy_host, args.sndcpy_port))
except:
    print('sndcpy is not running')
    exit()

print('Connected to sndcpy')

queues = []
stopFlag = False

# キュー管理
def create_queue():
    qid = str(uuid.uuid4())
    d = {'queue': queue.Queue(), 'id': qid}
    queues.append(d)
    return qid

def get_queue(qid):
    for q in queues:
        if q['id'] == qid:
            return q

def delete_queue(qid):
    for q in queues:
        if q['id'] == qid:
            queues.remove(q)

# sndcpyから受け取ったデータを各コネクションに配る
def data_queue():
    while not stopFlag:
        data = sndcpy.recv(1024)
        for q in queues:
            q: queue.Queue = q['queue']
            q.put(data)

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    conninfo = writer.get_extra_info("peername")
    qid = create_queue()
    print(f'Accepted connection from {conninfo[0]} port {conninfo[1]}\nCID: {qid}\n')
    while True:
        if writer.is_closing():
            print(f'Disconnected from {conninfo[0]} port {conninfo[1]}')
            delete_queue(qid)
            break

        q: queue.Queue = get_queue(qid)['queue']
        data = q.get()
        try:
            writer.write(data)
            await writer.drain()
        except:
            print(f'Disconnected from {conninfo[0]} port {conninfo[1]}')
            delete_queue(qid)
            break

async def run_server():
    server = await asyncio.start_server(handle_client, args.bind, args.port)
    print(f'Listening on {args.bind} port {args.port}\n')
    async with server:
        await server.serve_forever()

data_queue_thread = threading.Thread(target=data_queue)
data_queue_thread.start()

try:
    asyncio.get_event_loop().run_until_complete(run_server())
except:
    stopFlag = True