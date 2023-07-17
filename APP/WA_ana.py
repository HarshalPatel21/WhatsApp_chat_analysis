import streamlit as st
import pandas as pd
import seaborn as sns
import preprocess
import helper
import matplotlib.pyplot as plt

st.sidebar.title("WA Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose File")
if uploaded_file is not None:
    # data will be in bytes
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("UTF-8")

    # this will get us our DataFrame
    df = preprocess.preprocess(data)

    st.title("Chat")
    st.dataframe(df)

    # fetch unique user
    user_list = df["user"].unique().tolist()
    user_list.remove("Group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysi fro", user_list)
    if st.sidebar.button("Show analysy"):
        # Stats Area

        st.title("Top Statistics")
        num_messages, words, media, links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media")
            st.title(media)

        with col4:
            st.header("Links Shared")
            st.title(links)

        # Monthly Timeline

        st.title("montly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["messages"], color="purple")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # Daily Timeline

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline["only_date"], daily_timeline["messages"], color="lime")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # Activity Weekly
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="Orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        st.title("Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Finding the Activity
        if selected_user == "Overall":
            st.title("Most Busy User")
            x, new_df = helper.most_busy(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # word cloud
        # df_wc = helper.create_wordcloud(selected_user, df)
        # fig, ax = plt.subplot()
        # ax.imshow(df_wc)
        # st.pyplot(fig)

        # most common
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(most_common_df[0], most_common_df[1])
        plt.xticks(rotation="vertical")

        st.title("Most Common Words")
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)

        short_emoji_df = emoji_df.head(10)
        # ax.pie(short_emoji_df[1], labels=emoji_df[0],head(), autopct="%0.3f")
        #  ^^^^^^ this was showing error
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(short_emoji_df[1], labels=short_emoji_df[0], autopct="%0.3f")
            st.pyplot(fig)
