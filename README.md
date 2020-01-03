# milter-template

<p>Installation:</p>
git clone https://github.com/joaoreis81/milter-template.git<br>
cd milter-template<br>
docker-compose up -d<br>
<br>
<p>Postfix configuration:</p>

postconf -e "smtpd_milters = {inet:127.0.0.1:8801, connect_timeout=20s, default_action=accept }"<br>
postconf -e "non_smtpd_milters = {inet:127.0.0.1:8801, connect_timeout=20s, default_action=accept }"<br>
postfix reload


