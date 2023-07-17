import re
import pandas as pd


def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user_message": messages, "message_date": dates})
    # user_date -> date                                              '18/10/21, 10:58 - '
    df["message_date"] = pd.to_datetime(df["message_date"], format="%d/%m/%y, %H:%M - ")

    df.rename(columns={"message_date": "dates"}, inplace=True)

    users = []

    messages = []
    for message in df["user_message"]:
        entry = re.split("([\w\W]+?):\s", message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("Group_notification")
            messages.append(entry[0])

    df["user"] = users
    df["messages"] = messages
    df.drop(columns=["user_message"], inplace=True)

    df["only_date"] = df["dates"].dt.date
    df["year"] = df["dates"].dt.year
    df["month_num"] = df["dates"].dt.month
    df["month"] = df["dates"].dt.month_name()
    df["day"] = df["dates"].dt.day
    df["day_name"] = df["dates"].dt.day_name()
    df["hour"] = df["dates"].dt.hour
    df["minutes"] = df["dates"].dt.minute

    period = []

    for hour in df[["day_name", "hour"]]["hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 00:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    period = sorted(period)
    print(period)

    df["period"] = period
    return df
