# -*- coding: utf-8 -*-
import asyncio
import glob
import sys


from aiosmtplib import SMTP

sender = "joao@uxerere.io"
recipients = ["joao+rcpt@citybabyattackedbyrats.io"]


file_path = 'email.eml'
message = file_path
for eml_files in glob.glob("./spams/*"):
    print(eml_files)
    with open(eml_files, 'rb') as f:
        message = f.read()

    async def send_with_sendmail():
        smtp_client = SMTP(hostname="127.0.0.1", port=2525)
        await smtp_client.connect()
        await smtp_client.sendmail(sender, recipients, message)
        await smtp_client.quit()
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(send_with_sendmail())







