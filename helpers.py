from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas
import emoji


def filter_data(data_frame):
    data_frame = data_frame[data_frame['user'] != 'group_notification']
    data_frame = data_frame[data_frame['message'] != "<Media omitted>\n"]
    data_frame = data_frame[data_frame['message'] !=
                            "This message was deleted\n"]
    data_frame = data_frame[data_frame['message'] != "You were added\n"]
    data_frame = data_frame[data_frame['message'] != "🤣"]
    return data_frame


def calculate_number_of_words(data_frame):
    total_words = []
    for message in data_frame:
        total_words.extend(message.split(" "))
    return len(total_words)


def fetch_num_of_messages(actions, data_frame):
    data_frame = filter_data(data_frame)
    if actions != "Overall Analysis":
        data_frame = data_frame[data_frame['user'] == actions]
    return data_frame.shape[0]


def fetch_num_of_words(actions, data_frame):
    data_frame = filter_data(data_frame)
    if actions != "Overall Analysis":
        data_frame = data_frame[data_frame['user'] == actions]
    return calculate_number_of_words(data_frame['message'])


def fetch_num_of_media(actions, data_frame):
    data_frame = filter_data(data_frame)
    if actions != "Overall Analysis":
        data_frame = data_frame[data_frame['user'] == actions]
    return data_frame[data_frame['message'] == '<Media omitted>\n'].shape[0]


def fetch_num_of_links(actions, data_frame):
    data_frame = filter_data(data_frame)
    if actions != "Overall Analysis":
        data_frame = data_frame[data_frame['user'] == actions]
    total_links = []

    extractor = URLExtract()
    for message in data_frame['message']:
        total_links.extend(extractor.find_urls(message))
    return len(total_links)


def fetch_most_busy_users(data_frame):
    data_frame = filter_data(data_frame)
    top_five_busy_user = data_frame['user'].value_counts().head()
    all_users_chat_percentage = (round(
        data_frame['user'].value_counts() / data_frame.shape[0] * 100, 2)
        .reset_index().rename(columns={'count': 'percentage'}))
    return top_five_busy_user, all_users_chat_percentage


def create_chat_word_cloud(actions, data_frame):
    data_frame = filter_data(data_frame)
    if actions != "Overall Analysis":
        data_frame = data_frame[data_frame['user'] == actions]
    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    data_frame_wc = wc.generate(data_frame['message'].str.cat(sep=" "))
    return data_frame_wc


def most_frequent_words(actions, data_frame):
    extractor = URLExtract()
    data_frame = filter_data(data_frame)
    f = open("stop_words_hinglish.txt", "r")
    stop_words = f.read()
    all_chat_words = []
    if actions != "Overall Analysis":
        data_frame = data_frame[data_frame['user'] == actions]
    for message in data_frame['message']:
        if extractor.find_urls(message):
            continue
        for word in message.lower().split():
            if word not in stop_words:
                all_chat_words.append(word)
    new_data_frame = pandas.DataFrame(Counter(all_chat_words).most_common(20))
    new_data_frame.rename(columns={0: 'Most Frequent Words',
                                   1: 'No of Frequent Words'}, inplace=True)
    pandas.set_option('colheader_justify', 'center')
    new_data_frame.head()
    new_data_frame.index = range(1, len(new_data_frame) + 1)
    return new_data_frame


def get_emojis(actions, data_frame):
    emojis = []
    if actions != "Overall Analysis":
        data_frame = data_frame[data_frame['user'] == actions]
    for message in data_frame['message']:
        emojis.extend([e for e in message if e in emoji.EMOJI_DATA])
    emoji_data_frame = pandas.DataFrame(
        Counter(emojis).most_common(len(Counter(emojis))))
    emoji_data_frame.rename(columns={0: 'Frequent Emoji',
                                     1: 'No of Frequent Emoji'}, inplace=True)
    emoji_data_frame.index = range(1, len(emoji_data_frame) + 1)
    return emoji_data_frame
