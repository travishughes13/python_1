import smtplib
server = smtplib.SMTP("127.0.0.1", 8025)
server.sendmail("travis.hughes+1@gmail.com","travis.hughes+2@gmail.com","Hey Buddy, you suck")
{}