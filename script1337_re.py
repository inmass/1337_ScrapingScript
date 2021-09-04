from bs4 import BeautifulSoup
from time import time, sleep
import cloudscraper as requests
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

active = True
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "SENDER EMAIL"
password = "SMTP_PASSWORD"
receivers = ["RECEIVERS"]
body = 'https://candidature.1337.ma/piscines'

while active:
    try:
        sleep(60 - time() % 60)
        #log in
        print('logging in')
        client = requests.create_scraper()
        src = client.get('https://candidature.1337.ma/users/sign_in')
        soup = BeautifulSoup(src.text, "html.parser")
        csrf_input = soup.findAll("input", {"name":"authenticity_token"})
        csrf = csrf_input[0].attrs['value']

        r = client.post(
            'https://candidature.1337.ma/users/sign_in', 
            data = {
                "user[password]":"ACCOUT_PASSWORD",
                "user[email]":"ACCOUNT_EMAIL",
                "authenticity_token":csrf
            },
            headers = dict(Referer='https://candidature.1337.ma/users/sign_in')
        )

        print('logged in!')

    
        while active:
            sleep(60 - time() % 60)
            # thing to run
            src = client.get('https://candidature.1337.ma/piscines')
            soup = BeautifulSoup(src.text, "html.parser")

            if 'Lundi' in str(soup) or 'lundi' in str(soup) or 'Khouribga' in str(soup) or 'Ben Guerir' in str(soup) or 'places' in str(soup) or 'Juin' in str(soup) or 'juin' in str(soup) or 'août' in str(soup) or 'Août' in str(soup) or 'septembre' in str(soup) or 'Septembre' in str(soup):
                
                print('FINALLY!')
                #sending email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    for receiver_email in receivers:
                        message = MIMEMultipart()
                        message['From'] = sender_email
                        message['To'] = receiver_email
                        message['Subject'] = "!!![1337 POOL IS HERE]!!!"
                        message.attach(MIMEText(body,'plain'))
                        server.send_message(message)
                active = False

            elif "Aucune piscine n'est actuellement disponible" in str(soup):

                print('Not yet :(')
                active = True

            else:

                try:
                    print('Logged out.')

                    client = requests.create_scraper()
                    src = client.get('https://candidature.1337.ma/users/sign_in')
                    soup = BeautifulSoup(src.text, "html.parser")
                    csrf_input = soup.findAll("input", {"name":"authenticity_token"})
                    csrf = csrf_input[0].attrs['value']

                    #logging in to the console again
                    r = client.post(
                        'https://candidature.1337.ma/users/sign_in', 
                        data = {
                            "user[password]":"ACCOUT_PASSWORD",
                            "user[email]":"ACCOUNT_EMAIL",
                            "authenticity_token":csrf
                        },
                        headers = dict(Referer='https://candidature.1337.ma/users/sign_in')
                    )
                    print('logged in!')
                    print('WATCHING')

                except:
                    active = True

    except KeyboardInterrupt:
        active = False

    except:
        active = True