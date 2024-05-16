import streamlit as st
import preprocessing
import helpers
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a whatsapp chat file.")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    file_data = bytes_data.decode('utf-8')
    processed_data = preprocessing.data_pre_processor(file_data)
    st.dataframe(processed_data)

    # get the unique user
    users = processed_data['user'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0, "Overall Analysis")
    selected_user = (st.sidebar.
                     selectbox('Analyzed the chat by according to...', users))

    if st.sidebar.button("Show Analyzed Data"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(helpers.fetch_num_of_messages(selected_user,
                                                   processed_data))
        with col2:
            st.header('Total Words')
            st.title(helpers.fetch_num_of_words(selected_user,
                                                processed_data))
        with col3:
            st.header("Shared Media")
            st.title(helpers.fetch_num_of_media(selected_user,
                                                processed_data))
        with col4:
            st.header("Shared Links")
            st.title(helpers.fetch_num_of_links(selected_user,
                                                processed_data))

        # Finding busy users
        if selected_user == "Overall Analysis":
            st.title("Most Busy Users")
            top_five_busy_user, user_chat_percentage = (helpers.
                                                        fetch_most_busy_users(
                                                            processed_data))
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(top_five_busy_user.index,
                       top_five_busy_user.values,
                       color='orangered')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(user_chat_percentage)
        # Word Cloud
        st.title("Chat Word Cloud")
        data_frame_word_cloud = helpers.create_chat_word_cloud(selected_user,
                                                               processed_data)
        fig, ax = plt.subplots()
        ax.imshow(data_frame_word_cloud)
        st.pyplot(fig)

        # Most Frequent Common words
        st.title("Most Frequent Words")
        most_freq = helpers.most_frequent_words(selected_user, processed_data)
        fig, ax = plt.subplots()
        ax.bar(most_freq['Most Frequent Words'],
               most_freq['No of Frequent Words'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title("Fetch All Emoji")
        emojis = helpers.get_emojis(selected_user, processed_data)
        st.dataframe(emojis)
hide_stream_lit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_stream_lit_style, unsafe_allow_html=True)
