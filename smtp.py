
# SMTP configuration for sending email from the server (to the sys admin).

def send_email_server(subject, body):
    import smtplib

    FROM = "cryptopredicted@gmail.com"
    TO =  ["ilja@nevolin.be"] # recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
       # server_ssl.ehlo() # optional, called by login()
        server_ssl.login("cryptopredicted@gmail.com", "tteesstteerr112233++++")  
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        print('successfully sent the mail')
    except Exception as ex:
        print(ex)
        print("failed to send mail")


# import smtplib
# server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
# server_ssl.ehlo() # optional, called by login()
# o = server_ssl.login("cryptopredicted@gmail.com", "tteesstteerr112233++++")
# print(o)
# print("test")