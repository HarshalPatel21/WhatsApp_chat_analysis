from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    num_messages = df.shape[0]
    words = []

    for m in df["messages"]:
        words.extend(m.split())

    # Media msgs
    num_media = df[df["messages"] == "<Media omitted>\n"].shape[0]

    # For Links

    links = []
    for m in df["messages"]:
        links.extend(extract.find_urls(m))

    return num_messages, len(words), num_media, len(links)


def most_busy(df):
    x = df["user"].value_counts().head()
    df = (
        round((df["user"].value_counts() / df.shape[0]) * 100, 3)
        .reset_index()
        .rename(columns={"index": "Name", "user": "Percent"})
    )
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=100, background_color="white")
    df_wc = wc.generate(df["messages"].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != "Group_notification"]
    temp = df[df["messages"] != "<Media omitted>\n"]

    words = []

    for m in temp["messages"]:
        for word in m.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(30))


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for m in df["messages"]:
        emojis.extend([e for e in m if e in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline = (
        df.groupby(["year", "month_num", "month"]).count()["messages"].reset_index()
    )

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))

    timeline["time"] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df.groupby(["only_date"]).count()["messages"].reset_index()


def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["day_name"].value_counts()


def monthly_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["month"].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    user_heatmap = df.pivot_table(
        index="day_name", columns="period", values="messages", aggfunc="count"
    ).fillna(0)

    return user_heatmap
