from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import smtplib
import email
from pasword1 import pasword, sender, reciver
from email.message import EmailMessage
from email.header import decode_header
import imaplib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import os

# старт работы по получению письма
while True:
    try:
        time.sleep(1)
        imap = imaplib.IMAP4_SSL('imap.mail.ru')
        imap.login(sender, pasword)
        status, mess = imap.select('leonovdubai')
        res, data = imap.uid('search', None, 'UNSEEN')
        raw_mail = int(data[0].split()[-1])
        stat, inf = imap.uid('fetch', str(raw_mail), "(RFC822)")
        get_inf = inf[0][1]
        email_message = email.message_from_bytes(get_inf)
        subject, encoding = decode_header(email_message["Subject"])[0]
        subject = subject.decode(encoding)
        if subject == 'привет123':

            if os.path.exists('test'):
                pass
            else:
                os.mkdir('test')

            option = Options()
            option.add_argument("--headless")
            s = Service(r'D:\pythonProject1\geckodriver.exe')
            driver = webdriver.Firefox(service=s, options=option)
            action = ActionChains(driver)

            with open('news.txt', 'r') as f:
                quantity_of_url = f.read()
            list_of_urls = quantity_of_url.strip().split()
            name = 0
            for url in list_of_urls:
                name = re.findall('//(.*)/', url)[0]
                driver.get(url)
                for i in range(2):
                    time.sleep(2)
                    action.send_keys(Keys.CONTROL + Keys.END).perform()
                    time.sleep(2)
                    action.send_keys(Keys.CONTROL + Keys.HOME).perform()
                driver.get_full_page_screenshot_as_file(f"test\{name}.png")
            driver.quit()

            # отправка всех скринов одним письмом
            # ms = EmailMessage()
            # ms['Subject'] = 'Urls hiblack'
            # ms['From'] = sender
            # ms['To'] = reciver
            # ms.set_content('юрлс')
            # server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            # server.login(sender, pasword)
            # for i in os.listdir('test'):
            #     with open(os.path.join('test', i),'rb') as f:
            #         file1 = f.read()
            #         file_name = f.name
            #         ms.add_attachment(file1, maintype='aplication', subtype='octec-strem', filename=file_name)
            # server.send_message(ms)
            # server.quit()

            # отправка скринов разными письмами
            for i in os.listdir('test'):
                with open(os.path.join('test', i), 'rb') as f:
                    file1 = f.read()
                    file_name = f.name
                ms = EmailMessage()
                ms['Subject'] = 'Urls hiblack'
                ms['From'] = sender
                ms['To'] = reciver
                ms.set_content('юрлс')
                server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
                server.login(sender, pasword)
                ms.add_attachment(file1, maintype='aplication', subtype='octec-strem', filename=file_name)
                server.send_message(ms)
                server.quit()
    except:
        continue



