const net = require('net');
const server = net.createServer((c) => {
  // 'connection' listener.
  console.log('client connected:' + c.remoteAddress);
  const client = net.createConnection({ port: 5900 }, () => {
    // 'connect' listener.
    console.log('connected to server!');
    // client.write('world!\r\n');
  });
  var initServer = false;
  client.on('data', (data) => {
    try {
      console.log("server", new String(data));
    } catch (error) {
    }
    if (!initServer) {
      initServer = true;
      return;
    }
    c.write(data);

  });
  client.on('end', () => {
    console.log('disconnected from server');
  });

  c.on('data', (e) => {
    console.log(e);
    try {
      console.log("client", new String(e));
    } catch (error) {
    }
    client.write(e);
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

