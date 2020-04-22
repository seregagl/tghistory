#!/usr/bin/python3

import bs4
import csv
import glob, os

class TgHistoryParser:

    def __init__(self, file_mask, output_file_name):
        self.writer = None
        self.output_file = None
        self.output_file_name = output_file_name

        for file in self.find_files(file_mask):
            html = self.load_messages(file)
            self.parse_html(html)

    def find_files(self, file_mask):
        files = []
        for file in glob.glob(file_mask):
            files.append(file)

        return files

    def load_messages(self, filename):
        f = open(filename, 'r')
        html = f.read()
        f.close()
        return html

    def parse_html(self, data):
        soup = bs4.BeautifulSoup(data, 'html.parser')
        result = soup.select("div.message.default")
        previous_name = None

        for tag in result:
            m = {
                'id' : tag.attrs['id'],
                'name' : tag.select('.body:not(.forwarded) > .from_name'),
                'date' : tag.select_one('div.date.details').attrs['title'],
                'message' : tag.select('div.text'),
            }

            if 'joined' in tag.attrs['class']:
                m['name'] = previous_name
            else:
                previous_name = m['name']

            self.__save_message(m)

    def __save_message(self, message):
        if self.output_file is None:
            self.output_file = open(self.output_file_name, 'a')
            self.writer = csv.DictWriter(self.output_file, message.keys())
            # self.writer.writeheader()

        message = self.__format_message(message)
        self.writer.writerow(message)

    def __format_message(self, message):
        for key in message:
            if type(message[key]) is bs4.ResultSet:
                message[key] = [m.get_text(strip=True, separator='\r\n') for m in message[key]]

            message[key] = ' '.join(message[key]) if type(message[key]) is list else str(message[key])

        # remove message text for security reasons
        # message['message'] = '*' * len(message['message'])

        return message

    def __del__(self):
        if self.output_file is not None:
            self.output_file.close()

parser = TgHistoryParser('tg/*.html', 'tg/messages.csv')