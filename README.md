# milter-template

<p>Installation:</p>

```
git clone https://github.com/joaoreis81/milter-template.git
cd milter-template
docker-compose up -d
``` 

<p>Postfix configuration:</p>

```
postconf -e "smtpd_milters = {inet:127.0.0.1:8801, connect_timeout=20s, default_action=accept }"
postconf -e "non_smtpd_milters = {inet:127.0.0.1:8801, connect_timeout=20s, default_action=accept }"
postfix reload
```


