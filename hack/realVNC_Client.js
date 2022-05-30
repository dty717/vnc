
const net = require('net');

function getKey(){
    const client = net.createConnection({ port: 5900, host: "192.168.137.80" }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // client.write('world!\r\n');
    });
    client.on('data', (data) => {
        handleData(data);
    });
    client.on('end', () => {
        console.log('disconnected from server');
    });
    
    var buf = '82, 70, 66, 32, 48, 48, 53, 46, 48, 48, 48, 10, 128, 47, 0, 21, 206, 66, 236, 219, 40, 107, 126, 189, 252, 154, 42, 15, 6, 64, 202, 233, 147, 127, 111, 84, 158, 152, 139, 106, 15, 120, 196, 231, 186, 97, 10, 51, 0, 4, 2, 2, 11, 3, 3, 3, 2, 4, 0, 0, 0'.split(', ').map(e=>parseInt(e))
    client.write(Buffer.from(buf))
}
const handleData = (data)=>{
    console.log([...data].map(e => e < 16 ? '0' + e.toString(16) : e.toString(16)).join(' '))
    try {
        console.log("server", new String(data));
    } catch (error) {
        
    }
}






// '82, 70, 66, 32, 48, 48, 53, 46, 48, 48, 48, 10, 128, 47, 0, 21, 206, 66, 236, 219, 41, 107, 126, 189, 252, 154, 42, 15, 6, 64, 202, 233, 147, 127, 111, 84, 158, 152, 139, 106, 15, 120, 196, 231, 186, 97, 10, 51, 0, 4, 2, 2, 11, 3, 3, 3, 2, 4, 0, 0, 0'.split(', ').map(e=>parseInt(e)<16?"0"+parseInt(e).toString(16):parseInt(e).toString(16))


// 80 24 00 15 d2 0a 31 82 51 b3 33 7e a6 d0 18 24 f4 eb 22 53 f7 10 5d 25 f5 3a f9 6d c9 c0 d6 a4 ed eb 4b 9f 02 02 81 2c 00 17 20 26 4a 73 79 88 fe 64 1a 49 71 28 5a 99 7d 43 ff ed d7 dd 57 49 6a dd 73 b1 22 67 db 99 d8 4f 4e 00 00 08 00 a3 19 4e 2d 4c cf a5 aa 86 44 f5 10 4b c8 b4 63 87 09 d6 ce fe 6f 94 4c df af 00 bd 98 0b ea e6 f0 fc ea 52 a6 91 95 cd aa 0b a0 46 b6 2b 25 e6 87 9d ae 40 da 8d dc dd 99 d9 c9 9a 8a 35 dd ac 41 89 5e 3f 9d d6 59 44 e9 07 c0 9c 8d 80 8f 2a 11 77 82 49 df a0 54 38 02 db fd 77 1c b7 1c 82 56 80 9a 10 c1 e1 2a bc 4a a5 7d bf cb 74 53 e5 db 2a 95 83 bf 75 30 3e d8 fe 18 a9 d0 54 60 1c db 2b 41 ec 81 80 78 2e bb 09 1d 9b 0b d1 32 64 4a 68 17 c9 89 bc e7 53 8b e8 28 c6 6f a8 ca 82 2d f8 27 e5 6b c1 e5 3b ab 2d 92 7c 90 19 af 68 85 a4 0f 59 a7 97 7b 3a 68 da b8 b7 26 f0 23 14 ec 85 3b 8d 39 32 2b 73 55 20 cb 73 aa 22 54 26 b0 dd cf ae 12 da c9 fc 78 b3 c6 18 99 d4 f0 0d 3c ca 60 1d 2c 09 56 68 de 97 d0 54 58 ef 52 a6 92 0e 60 82 48 c2 56 1f 64 38 0b 10 12 09 8f 89 00 03 01 00 01
// 80 24 00 15 ad 50 f8 a9 83 c5 1a dd 6c fa 09 70 b7 67 21 6c 96 fd 15 f5 eb 46 12 97 45 79 ad b7 ce 19 ef 38 02 02 81 2c 00 17 20 2a cc 13 9b 25 ea cd 9d 89 d5 b9 8a c5 e6 7b c6 c1 e1 ff bf 41 de c0 35 18 b0 bb 8f 8e 5c 01 0b 00 00 08 00 a3 19 4e 2d 4c cf a5 aa 86 44 f5 10 4b c8 b4 63 87 09 d6 ce fe 6f 94 4c df af 00 bd 98 0b ea e6 f0 fc ea 52 a6 91 95 cd aa 0b a0 46 b6 2b 25 e6 87 9d ae 40 da 8d dc dd 99 d9 c9 9a 8a 35 dd ac 41 89 5e 3f 9d d6 59 44 e9 07 c0 9c 8d 80 8f 2a 11 77 82 49 df a0 54 38 02 db fd 77 1c b7 1c 82 56 80 9a 10 c1 e1 2a bc 4a a5 7d bf cb 74 53 e5 db 2a 95 83 bf 75 30 3e d8 fe 18 a9 d0 54 60 1c db 2b 41 ec 81 80 78 2e bb 09 1d 9b 0b d1 32 64 4a 68 17 c9 89 bc e7 53 8b e8 28 c6 6f a8 ca 82 2d f8 27 e5 6b c1 e5 3b ab 2d 92 7c 90 19 af 68 85 a4 0f 59 a7 97 7b 3a 68 da b8 b7 26 f0 23 14 ec 85 3b 8d 39 32 2b 73 55 20 cb 73 aa 22 54 26 b0 dd cf ae 12 da c9 fc 78 b3 c6 18 99 d4 f0 0d 3c ca 60 1d 2c 09 56 68 de 97 d0 54 58 ef 52 a6 92 0e 60 82 48 c2 56 1f 64 38 0b 10 12 09 8f 89 00 03 01 00 01
// 80 24 00 15 ec bf c0 09 b1 14 19 fd 5e 76 ed 44 d5 06 0b 7d b0 33 0f 0f 8b 17 0a b7 1d a4 7d dd 40 9f 92 c3 02 02 81 2c 00 17 20 35 61 6b 74 4b 3e 47 70 85 1c 71 ca 10 53 1b 41 f6 7d 19 fa ab d3 82 98 c5 38 60 cd 10 b4 78 5c 00 00 08 00 a3 19 4e 2d 4c cf a5 aa 86 44 f5 10 4b c8 b4 63 87 09 d6 ce fe 6f 94 4c df af 00 bd 98 0b ea e6 f0 fc ea 52 a6 91 95 cd aa 0b a0 46 b6 2b 25 e6 87 9d ae 40 da 8d dc dd 99 d9 c9 9a 8a 35 dd ac 41 89 5e 3f 9d d6 59 44 e9 07 c0 9c 8d 80 8f 2a 11 77 82 49 df a0 54 38 02 db fd 77 1c b7 1c 82 56 80 9a 10 c1 e1 2a bc 4a a5 7d bf cb 74 53 e5 db 2a 95 83 bf 75 30 3e d8 fe 18 a9 d0 54 60 1c db 2b 41 ec 81 80 78 2e bb 09 1d 9b 0b d1 32 64 4a 68 17 c9 89 bc e7 53 8b e8 28 c6 6f a8 ca 82 2d f8 27 e5 6b c1 e5 3b ab 2d 92 7c 90 19 af 68 85 a4 0f 59 a7 97 7b 3a 68 da b8 b7 26 f0 23 14 ec 85 3b 8d 39 32 2b 73 55 20 cb 73 aa 22 54 26 b0 dd cf ae 12 da c9 fc 78 b3 c6 18 99 d4 f0 0d 3c ca 60 1d 2c 09 56 68 de 97 d0 54 58 ef 52 a6 92 0e 60 82 48 c2 56 1f 64 38 0b 10 12 09 8f 89 00 03 01 00 01
// 80 24 00 15 20 56 8a db 85 20 13 c8 5d 61 42 3f c9 43 bc f2 ea e9 3e 31 1c 26 be ed 96 c4 07 6f 19 89 57 d1 02 02 81 2c 00 17 20 6a 35 b5 19 9d 11 f6 fd 68 53 bf 0d 0e dc 4d 40 63 62 14 8a 82 a1 80 06 07 54 84 50 d1 d7 61 22 00 00 08 00 a3 19 4e 2d 4c cf a5 aa 86 44 f5 10 4b c8 b4 63 87 09 d6 ce fe 6f 94 4c df af 00 bd 98 0b ea e6 f0 fc ea 52 a6 91 95 cd aa 0b a0 46 b6 2b 25 e6 87 9d ae 40 da 8d dc dd 99 d9 c9 9a 8a 35 dd ac 41 89 5e 3f 9d d6 59 44 e9 07 c0 9c 8d 80 8f 2a 11 77 82 49 df a0 54 38 02 db fd 77 1c b7 1c 82 56 80 9a 10 c1 e1 2a bc 4a a5 7d bf cb 74 53 e5 db 2a 95 83 bf 75 30 3e d8 fe 18 a9 d0 54 60 1c db 2b 41 ec 81 80 78 2e bb 09 1d 9b 0b d1 32 64 4a 68 17 c9 89 bc e7 53 8b e8 28 c6 6f a8 ca 82 2d f8 27 e5 6b c1 e5 3b ab 2d 92 7c 90 19 af 68 85 a4 0f 59 a7 97 7b 3a 68 da b8 b7 26 f0 23 14 ec 85 3b 8d 39 32 2b 73 55 20 cb 73 aa 22 54 26 b0 dd cf ae 12 da c9 fc 78 b3 c6 18 99 d4 f0 0d 3c ca 60 1d 2c 09 56 68 de 97 d0 54 58 ef 52 a6 92 0e 60 82 48 c2 56 1f 64 38 0b 10 12 09 8f 89 00 03 01 00 01


