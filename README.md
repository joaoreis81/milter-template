# milter-template

<p>Installation:</p>

```
git clone https://github.com/joaoreis81/milter-template.git
cd milter-template
mkdir spams
docker-compose up -d
``` 
Get some .eml (raw email messages) and put it to "spams" directory.

<p>Running the tests:</p>

```
pip3 install iosmtplib
python3 ./smtp_client.py
```
or
```
python3 ./smtp_client.py& python3 ./smtp_client.py& python3 ./smtp_client.py& python3 ./smtp_client.py& python3 ./smtp_client.py& python3 ./smtp_client.py& python3 ./smtp_client.py& python3 ./smtp_client.py& python3 ./smtp_client.py& python3 ./smtp_client.py&   
```

