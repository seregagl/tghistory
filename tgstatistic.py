#!/usr/bin/python3

import pandas as pd
import plotly
import plotly.graph_objs as go
import datetime
from collections import Counter

class TgStatistic:

    def __init__(self):

        pd.set_option('display.max_columns', 1000)
        pd.set_option('display.max_rows', 1000)

        date_parser = lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S')
        self.df = pd.read_csv('tg/messages.csv', names=['id', 'user', 'date', 'message'], parse_dates=['date'], date_parser=date_parser)

        self.df['day'] = self.df['date'].dt.strftime('%m-%d (%a)')
        self.df['hour'] = self.df['date'].dt.strftime('%H')
        self.df['message_length'] = self.df['message'].str.len()

    def report_messages_by_day(self):
        # total messages by day
        day_count = self.df.groupby('day')['day'].count()
        trace = go.Bar(x = day_count.index.values, y = day_count.values)
        plotly.offline.plot({'data': [trace], 'layout': go.Layout(title="Messages by day")}, filename='by_day.html')

    def report_messages_by_hour(self):
        # total messages by hour
        hour_count = self.df.groupby('hour')['hour'].count()
        trace = go.Bar(x = hour_count.index.values, y = hour_count.values)
        plotly.offline.plot({'data': [trace], 'layout': go.Layout(title="Messages by hour")}, filename='by_hour.html')

    def report_messages_by_user(self):
        # total messages by user
        user_count = self.df.groupby('user')['user'].count()
        trace = go.Pie(labels = user_count.index, values = user_count.values)
        plotly.offline.plot({'data': [trace], 'layout': go.Layout(title="Messages by user")}, filename='by_user.html')

    def report_messages_by_length(self):
        # average user message length
        user_length = self.df.groupby('user')['message_length'].mean()
        trace = go.Pie(labels = user_length.index, values = user_length.values)
        plotly.offline.plot({'data': [trace], 'layout': go.Layout(title="Average messages length")}, filename='by_message_len.html')

    def report_user_messages_sum(self):
        # user message sum
        user_sum = self.df.groupby('user')['message_length'].sum()
        trace = go.Pie(labels = user_sum.index, values = user_sum.values)
        plotly.offline.plot({'data': [trace], 'layout': go.Layout(title="User messages sum")}, filename='by_message_sum.html')

    def report_user_messages_by_day(self):
        # user messages by day
        user_messages1 = self.df.query('user.str.contains("S")').groupby(['day'])['day'].count()
        user_messages2 = self.df.query('user.str.contains("К")').groupby(['day'])['day'].count()
        trace1 = go.Bar(x = user_messages1.index, y = user_messages1.values)
        trace2 = go.Bar(x = user_messages2.index, y = user_messages2.values)
        plotly.offline.plot({'data': [trace1, trace2], 'layout': go.Layout(title="User messages by day", barmode='group')}, filename='user_by_day.html')

    def report_words_count(self):
        all_words = []
        messages = [str(m).split() for m in self.df['message']]

        for message in messages:
            for words in message:
                s = words.strip('.,"!?#()*+-:>«»').lower()
                if len(s) > 0:
                    all_words.append(s)

        # keys = Counter(all_words).keys()  # equals to list(set(words))
        # val = Counter(all_words).values()  # counts the elements' frequency

        c = Counter(all_words)
        print(c.items())
        #all_words = sorted(all_words)


statistic = TgStatistic()
statistic.report_messages_by_day()
#statistic.report_messages_by_hour()
#statistic.report_messages_by_user()
#statistic.report_messages_by_length()
#statistic.report_user_messages_sum()
#statistic.report_user_messages_by_day()
statistic.report_words_count()