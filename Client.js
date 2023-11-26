var net = require('net');

var client = new net.Socket();
client.connect(65432, '127.0.0.1', function() {
    console.log('Connected');
    client.write('Article, True,, 2023-11-15, 5');
});

client.on('data', function(data) {
    console.log('Received: ' + data.toString());  // Convert the received data to a string
    client.destroy(); // kill client after server's response
});