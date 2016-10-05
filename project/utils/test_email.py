import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

to_addr = 'to_email@gmail.com'
subject = 'Salam Test'
body = 'CHetori?'
from_addr = "email@gmail.com"

msg = MIMEMultipart()

msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)  # todo the mail server address
server.starttls()
server.login(from_addr, "something")
text = msg.as_string()
server.sendmail(from_addr, to_addr, text)
server.quit()