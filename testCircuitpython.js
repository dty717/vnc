const net = require('net');
const { SerialPort, ReadlineParser } = require('serialport')

var path = 'com23'

var baudRate = 9600
var serialport = new SerialPort({ path, baudRate })
var parser = new ReadlineParser()
serialport.pipe(parser)

var holdOn = false
var holdOnRecLen = 0
var holdOnRecLenLast = 0
var holdOnRecStr = ''

var isSending = false

var pathDevice = "com22"
var baudRateDevice = 9600
var serialportDevice = new SerialPort({ path:pathDevice, baudRate:baudRateDevice })

serialportDevice.on('data',(data) => {
    // holdOnRecStr
    if (holdOnRecLen > 0) {
        holdOnRecLen--;
        // holdOnRecStr 
        for (let dataIndex = 0; dataIndex < data.length; dataIndex++) {
            const element = data[dataIndex];
            holdOnRecStr += element + ","
        }
    }

    if (holdOnRecLen <= 0) {
        holdOnRecLen = 0
        if(holdOnRecStr){
            holdOnRecStr = "\r\n"+holdOnRecStr.substring(0, holdOnRecStr.length - 1) + "]))\r\n"
            serialport.write(holdOnRecStr)
            console.log(holdOnRecStr)
            holdOnRecStr = ""
        }
        holdOn = false
    }
})


parser.on('data', (data) => {
    if (data == holdOnRecLenLast) {
        isSending = false
    }
    if(data == ">>> list(usb_cdc.data.read(100))\r" ||(data == "[]\r")){
        if(data == "[]\r"){
            isSending = false
        }
        return;
    }
    console.log("\t\t\t\t"+data)
    var dataMatch = data.match(/^\[[\d,\s]+\]/)
    if(dataMatch){
        holdOn = true
        recList = eval(dataMatch[0])
        serialportDevice.write(Buffer.from(recList))
        holdOnRecStr = 'usb_cdc.data.write(bytes(['
        holdOnRecLen = recList[5] * 2 + 3 + 2
        holdOnRecLenLast = holdOnRecLen
    }
})

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

serialport.write([0x03])
serialport.write("\r\n")
serialport.write("import usb_cdc\r\n")
serialport.write("usb_cdc.data.timeout = 0.1\r\n")


async function runTask(){
    while(true) {
        await sleep(0.1)
        if(holdOn){
            continue
        }
        if(isSending){
            continue
        }
        isSending = true
        serialport.write("list(usb_cdc.data.read(100))\r\n")
    }
    console.log("runTask finished")
}

runTask()


// def modbus(buf):
    // recBuf = usb_cdc.data.read(8)
    // time.sleep(0.2)
    // usb_cdc.data.write(bytes(buf))
    // print(list(recBuf))




// var usingServer = false

// if(usingServer){
//     var path = '/dev/ttyUSB0'
// }else{
//     var path = 'com23'
// }

// var baudRate = 9600
// var serialport = new SerialPort({ path, baudRate })
// if (usingServer) {
//     // serialport.pipe(parser)
//     var clients = [];
//     serialport.on('data', (data) => {
//         for (var client of clients) {
//             client.write(data)
//         }
//     })
//     function deleteItem(client) {
//         var _indexClient = clients.indexOf(client)
//         if (_indexClient != -1) {
//             clients.splice(_indexClient, 1);
//         }
//     }
//     const server = net.createServer((c) => {
//         console.log('client connected:' + c.remoteAddress);
//         clients.push(c);
//         c.on('data', (e) => {
//             try {
//                 serialport.write(e)
//                 console.log(e);
//             } catch (error) {
//                 console.log(e);
//             }
//         });
//         c.on('end', () => {
//             deleteItem(c);
//             console.log('client disconnected');
//         });
//         c.on('error', () => {
//             deleteItem(c);
//             console.log('client error');
//         });
//     });
//     server.on('error', (err) => {
//         throw err;
//     });
//     server.listen(9999, () => {
//         console.log('server bound');
//     });
// } else {
//     // var client = net.createConnection({ host: "127.0.0.1", port: 9999 }, () => {
//     //     // 'connect' listener.
//     //     console.log('connected to server!');
//     //     // client.write('world!\r\n');
//     // });

//     serialport.on('data', (data) => {
//         // client.write(data);
//         if (data.compare(strToBuf("03 04 00 64 00 0A 30 30")) == 0) {
//             // console.log("Buffer 03")
//             serialport.write(strToBuf("03 04 14 CD 32 00 01 AA AA 65 F5 01 B9 A0 31 00 03 63 7F 00 00 00 00 5F 3F"))
//             serialport.flush()
//             // setTimeout(() => {
//             // }, 100);
//         }
//         console.log(data)

//     })
//     // 02 04 14 cd 32 00 01 aa aa 65 f5 00 00 a0 20 00 03 22 1f 00 00 00 00 58 77
//     // 02 04 14 cd 32 00 01 aa aa 65 f5 00 00 a0 20 00 03 22 1f 00 00 00 00 58 77
//     // client.on('data', (e) => {
//     //     try {
//     //         serialport.write(e)
//     //         console.log(e);
//     //     } catch (error) {
//     //         console.log(e);
//     //     }
//     // });
//     // client.on('end', () => {
//     //     console.log('disconnected from server');
//     // });
// }
function strToBuf(strBuf){
    return Buffer.from(strBuf.trim().split(' ').map(e=>parseInt('0x'+e)))
}