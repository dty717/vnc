const net = require('net');
const { SerialPort ,ReadlineParser} = require('serialport')

var path = '/dev/serial0'
var baudRate = 9600
var serialport = new SerialPort({ path, baudRate})
var parser = new ReadlineParser()
serialport.pipe(parser)
parser.on('data', (data)=>{
    for( var client of clients){
        client.write(data+"\n")
    }
})

var clients = [];
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
            console.log(new String(e));
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
