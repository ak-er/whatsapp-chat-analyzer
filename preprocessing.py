import re
import pandas

# f = open('chats/cyber-group.txt', 'r', encoding='utf-8')
# data = f.read()


def data_pre_processor(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)

    # pandas data frame
    pd_data_frame = pandas.DataFrame.from_dict(
        {'users_messages': messages, 'messages_dates': dates}, orient='index')
    pd_data_frame = pd_data_frame.transpose()

    pd_data_frame['messages_dates'] = pandas.to_datetime(
        pd_data_frame['messages_dates'], format='%d/%m/%Y, %H:%M - ')

    pd_data_frame.rename(columns={'messages_dates': 'date'}, inplace=True)
    pd_data_frame.head()

    # separae users and messages
    users = []
    messages = []
    for message in pd_data_frame['users_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    pd_data_frame['user'] = users
    pd_data_frame['message'] = messages
    pd_data_frame.drop(columns=['users_messages'], inplace=True)
    pd_data_frame.head()

    pd_data_frame['year'] = pd_data_frame['date'].dt.year.fillna(0).astype(int)
    pd_data_frame['month'] = pd_data_frame['date'].dt.month_name()
    pd_data_frame['day'] = pd_data_frame['date'].dt.day.fillna(0).astype(int)
    pd_data_frame['hour'] = pd_data_frame['date'].dt.hour.fillna(0).astype(int)
    pd_data_frame['minute'] = (pd_data_frame['date'].dt.minute.fillna(0)
                               .astype(int))
    pd_data_frame.head()
    return pd_data_frame
