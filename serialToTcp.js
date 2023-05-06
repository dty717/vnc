const net = require('net');
const { SerialPort, ReadlineParser } = require('serialport')

var usingServer = true

if(usingServer){
    // var path = '/dev/ttyUSB0'
    var path = '/dev/serial0'
    var baudRate = 9600
}else{
    var path = 'com37'
    var baudRate = 9600
}

var serialport = new SerialPort({ path, baudRate })
var parser = new ReadlineParser()
if (usingServer) {
    // serialport.pipe(parser)
    var clients = [];
    serialport.on('data', (data) => {
        for (var client of clients) {
            client.write(data)
        }
    })
    function deleteItem(client) {
        var _indexClient = clients.indexOf(client)
        if (_indexClient != -1) {
            clients.splice(_indexClient, 1);
        }
    }
    const server = net.createServer((c) => {
        console.log('client connected:' + c.remoteAddress);
        clients.push(c);
        c.on('data', (e) => {
            try {
                serialport.write(e)
                console.log(e);
            } catch (error) {
                console.log(e);
            }
        });
        c.on('end', () => {
            deleteItem(c);
            console.log('client disconnected');
        });
        c.on('error', () => {
            deleteItem(c);
            console.log('client error');
        });
    });
    server.on('error', (err) => {
        throw err;
    });
    server.listen(9999, () => {
        console.log('server bound');
    });
} else {
    var client = net.createConnection({ host: "127.0.0.1", port: 9999 }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // client.write('world!\r\n');
    });

    serialport.on('data', (data) => {
        client.write(data);
    })
    client.on('data', (e) => {
        try {
            serialport.write(e)
            console.log(e);
        } catch (error) {
            console.log(e);
        }
    });
    client.on('end', () => {
        console.log('disconnected from server');
    });
}
