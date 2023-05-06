const net = require('net');
const { SerialPort, ReadlineParser } = require('serialport')

var path = 'com36'
var baudRate = 115200
var serialport = new SerialPort({ path, baudRate })


var pathDevice = "com22"
var baudRateDevice = 115200
var serialportDevice = new SerialPort({ path:pathDevice, baudRate:baudRateDevice })

serialportDevice.on('data',(data) => {
    serialport.write(data)
})

serialport.on('data', (data) => {
    serialportDevice.write(data)
})
