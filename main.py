import os.path
import ssl
import smtplib
import datetime
import json
import argparse
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class Config:
    def __init__(self, json_config) -> None:
        js_dict = json.loads(json_config)
        self.ftp_user = js_dict["ftp_user"]
        self.ftp_pw = js_dict["ftp_pw"]
        self.ftp_port = js_dict["ftp_port"]
        self.ftp_root = js_dict["ftp_root"]
        self.mail_user = js_dict["mail_user"]
        self.mail_pw = js_dict["mail_pw"]
        self.mail_server = js_dict["mail_server"]
        self.mail_recipient = js_dict["mail_recipient"]
        super().__init__()


class MyHandler(FTPHandler):
    def on_file_received(self, file):
        print('==> File received: {0}'.format(file))
        self.send_email(file)
        super().on_file_received(file)

    def send_email(self, image_filename):
        msg = self.create_mime_message(image_filename)
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.set_default_verify_paths()
        mail_server = smtplib.SMTP_SSL(self.cfg.mail_server, context=ctx)
        mail_server.login(self.cfg.mail_user, self.cfg.mail_pw)
        mail_server.sendmail(self.cfg.mail_user, self.cfg.mail_recipient, msg)
        mail_server.quit()

    def create_mime_message(self, image_filename):
        message = MIMEMultipart()
        message["From"] = self.cfg.mail_user
        message["To"] = self.cfg.mail_recipient
        message["Subject"] = "Security camera activation {0}".format(datetime.datetime.today())
        body = "Security camera activation message"
        message.attach(MIMEText(body, "plain"))
        with open(image_filename, "rb") as attachment:
            part = MIMEBase("image", "jpeg")
            part.set_payload(attachment.read())
        #
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment; filename={0}".format(os.path.basename(image_filename))
        )
        message.attach(part)
        text = message.as_string()
        return text


def parse_config_file():
    """
    Parse the config file for runtime params
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('config', action="store", help="Path to the configuration file")
    res = parser.parse_args()

    with open(res.config, 'r') as f:
        file_string = f.read()
    cfg = Config(file_string)
    return cfg


def setup_ftp_server(cfg):
    """
    Configure the ftp server
    """
    authorizer = DummyAuthorizer()
    # authorizer.add_user(FTP_USER, FTP_PW, DEFAULT_ROOT, perm='elradfmwMT')
    authorizer.add_user(cfg.ftp_user, cfg.ftp_pw, cfg.ftp_root, perm='lrw')
    handler = MyHandler
    handler.cfg = cfg
    handler.authorizer = authorizer
    handler.banner = "Camera image uploader"
    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', cfg.ftp_port)
    server = FTPServer(address, handler)
    # set a limit for connections - keep this small for a smaller attack surface
    server.max_cons = 5
    server.max_cons_per_ip = 5
    return server


def run_main():
    """ Main """
    cfg = parse_config_file()
    server = setup_ftp_server(cfg)
    print('Starting server, use SIGINT to stop')
    server.serve_forever()


if __name__ == '__main__':
    run_main()