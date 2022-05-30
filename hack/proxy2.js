const net = require('net');
const server = net.createServer((c) => {
  // 'connection' listener.
  console.log('client connected:' + c.remoteAddress);
  client = c
  c.on('data', (e) => {
    console.log(e.length);
    try {
      console.log("client", new String(e));
    } catch (error) {
    }
  });
  c.on('end', () => {
    console.log('client disconnected');
  });
  c.write('RFB 005.000\n');
  //c.pipe(c);
});
server.on('error', (err) => {
  throw err;
});
//server.address("127.0.0.1")
server.listen(5901, () => {
  console.log('server bound');
});

// Protocol error: invalid SecInit message type 8242

// var buf = '80 24 00 15 6d cf 0b 9e 43 81 a6 06 fb 5f 4f 66 fb bb 13 b5 8f 43 87 dc cb 63 4d ce 55 5e d9 16 73 46 c7 1c 02 02 81 2c 00 17 20 8f 58 e0 3f ba 60 e1 e7 4c 2b d7 a8 5a 17 fe e8 8b 0e c8 dc 9b 9a d1 64 28 64 27 48 8f 3f fd 67 00 00 08 00 a3 19 4e 2d 4c cf a5 aa 86 44 f5 10 4b c8 b4 63 87 09 d6 ce fe 6f 94 4c df af 00 bd 98 0b ea e6 f0 fc ea 52 a6 91 95 cd aa 0b a0 46 b6 2b 25 e6 87 9d ae 40 da 8d dc dd 99 d9 c9 9a 8a 35 dd ac 41 89 5e 3f 9d d6 59 44 e9 07 c0 9c 8d 80 8f 2a 11 77 82 49 df a0 54 38 02 db fd 77 1c b7 1c 82 56 80 9a 10 c1 e1 2a bc 4a a5 7d bf cb 74 53 e5 db 2a 95 83 bf 75 30 3e d8 fe 18 a9 d0 54 60 1c db 2b 41 ec 81 80 78 2e bb 09 1d 9b 0b d1 32 64 4a 68 17 c9 89 bc e7 53 8b e8 28 c6 6f a8 ca 82 2d f8 27 e5 6b c1 e5 3b ab 2d 92 7c 90 19 af 68 85 a4 0f 59 a7 97 7b 3a 68 da b8 b7 26 f0 23 14 ec 85 3b 8d 39 32 2b 73 55 20 cb 73 aa 22 54 26 b0 dd cf ae 12 da c9 fc 78 b3 c6 18 99 d4 f0 0d 3c ca 60 1d 2c 09 56 68 de 97 d0 54 58 ef 52 a6 92 0e 60 82 48 c2 56 1f 64 38 0b 10 12 09 8f 89 00 03 01 00 01'.split(' ').map(e=>parseInt("0x"+e))
// client.write(Buffer.from(buf))


