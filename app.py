

# import streamlit as st
# import requests
# import pandas as pd
# import time
# from textblob import TextBlob
# from io import BytesIO

# # =========================================================
# # PAGE CONFIG
# # =========================================================

# st.set_page_config(
#     page_title="Reddit Social Listening",
#     layout="wide"
# )

# st.title("📊 Reddit Social Listening Tool")

# # =========================================================
# # SESSION STATE
# # =========================================================

# if "excel_data" not in st.session_state:
#     st.session_state.excel_data = None

# if "df" not in st.session_state:
#     st.session_state.df = None

# if "keyword" not in st.session_state:
#     st.session_state.keyword = None

# # =========================================================
# # USER INPUT
# # =========================================================

# keyword = st.text_input(
#     "Enter Reddit Search Keyword",
#     placeholder="Example: Karnataka IT department"
# )

# limit = st.slider(
#     "Number of Posts to Fetch",
#     min_value=5,
#     max_value=150,
#     value=20
# )

# sort_option = st.selectbox(
#     "Select Reddit Sort Type",
#     [
#         "relevance",
#         "hot",
#         "top",
#         "new",
#         "comments",
#         "rising"
#     ]
# )

# min_relevance = st.slider(
#     "Minimum Relevance Score",
#     min_value=1,
#     max_value=15,
#     value=5
# )

# # =========================================================
# # SENTIMENT FUNCTION
# # =========================================================

# def get_sentiment(text):

#     try:

#         polarity = TextBlob(str(text)).sentiment.polarity

#         if polarity > 0:
#             return "Positive"

#         elif polarity < 0:
#             return "Negative"

#         else:
#             return "Neutral"

#     except:

#         return "Neutral"

# # =========================================================
# # RELEVANCE FUNCTION
# # =========================================================

# def calculate_relevance(title, post_text, subreddit, keyword):

#     score = 0
#     match_count = 0

#     keyword_parts = keyword.lower().split()

#     title = str(title).lower()
#     post_text = str(post_text).lower()
#     subreddit = str(subreddit).lower()

#     full_text = title + " " + post_text + " " + subreddit

#     for word in keyword_parts:

#         if word in full_text:

#             match_count += 1

#             if word in title:
#                 score += 5

#             if word in post_text:
#                 score += 3

#             if word in subreddit:
#                 score += 2

#     return score, match_count

# # =========================================================
# # FETCH BUTTON
# # =========================================================

# if st.button("Fetch Reddit Data"):

#     if not keyword:

#         st.warning("Please enter keyword")
#         st.stop()

#     # =========================================================
#     # SETTINGS
#     # =========================================================

#     HEADERS = {
#         "User-Agent": "KarnatakaSocialListener/1.0"
#     }

#     SEARCH_URL = (
#         f"https://www.reddit.com/search.json?"
#         f"q={keyword}"
#         f"&sort={sort_option}"
#         f"&limit={limit}"
#     )

#     # =========================================================
#     # FETCH DATA
#     # =========================================================

#     with st.spinner("Fetching Reddit Posts and Comments..."):

#         # response = requests.get(
#         #     SEARCH_URL,
#         #     headers=HEADERS
#         # )

#         # data = response.json()
#         response = requests.get(
#             SEARCH_URL,
#             headers=HEADERS,
#             timeout=20
#         )
        
#         # DEBUG STATUS
#         st.write("Search API Status:", response.status_code)
        
#         # CHECK RESPONSE
#         if response.status_code != 200:
        
#             st.error(f"Reddit API Error: {response.status_code}")
        
#             st.text(response.text[:500])
        
#             st.stop()
        
#         # SAFE JSON PARSE
#         try:
#             data = response.json()
        
#         except Exception as e:
        
#             st.error("Failed to decode Reddit response")
        
#             st.text(response.text[:1000])
        
#             st.stop()

#         posts = data["data"]["children"]

#         st.success(f"Total Posts Pulled From Reddit: {len(posts)}")

#         # =========================================================
#         # STORE DATA
#         # =========================================================

#         all_data = []

#         progress_bar = st.progress(0)

#         # =========================================================
#         # LOOP POSTS
#         # =========================================================

#         for idx, post in enumerate(posts):

#             try:

#                 p = post["data"]

#                 # =========================================================
#                 # POST DETAILS
#                 # =========================================================

#                 post_id = p.get("id")
#                 title = p.get("title")
#                 subreddit = p.get("subreddit")
#                 author = p.get("author")
#                 upvotes = p.get("score")
#                 total_comments = p.get("num_comments")
#                 post_text = p.get("selftext")
#                 created_utc = p.get("created_utc")

#                 post_url = "https://reddit.com" + p.get("permalink")

#                 # =========================================================
#                 # RELEVANCE
#                 # =========================================================

#                 relevance_score, match_count = calculate_relevance(
#                     title,
#                     post_text,
#                     subreddit,
#                     keyword
#                 )

#                 if relevance_score < min_relevance:
#                     continue

#                 # =========================================================
#                 # COMMENTS API
#                 # =========================================================

#                 comments_url = (
#                     f"https://www.reddit.com/comments/{post_id}.json"
#                 )

#                 comments_response = requests.get(
#                     comments_url,
#                     headers=HEADERS
#                 )

#                 comments_data = comments_response.json()

#                 comments = comments_data[1]["data"]["children"]

#                 # =========================================================
#                 # NO COMMENTS
#                 # =========================================================

#                 if len(comments) == 0:

#                     all_data.append({

#                         "keyword": keyword,
#                         "relevance_score": relevance_score,
#                         "match_count": match_count,

#                         "post_id": post_id,
#                         "title": title,
#                         "subreddit": subreddit,
#                         "post_author": author,
#                         "post_upvotes": upvotes,
#                         "total_comments": total_comments,
#                         "post_text": post_text,
#                         "post_url": post_url,
#                         "post_created_utc": created_utc,

#                         "comment_author": None,
#                         "comment": None,
#                         "comment_score": None,
#                         "comment_created_utc": None,

#                         "sentiment": "Neutral"
#                     })

#                 # =========================================================
#                 # LOOP COMMENTS
#                 # =========================================================

#                 for c in comments:

#                     if c["kind"] == "t1":

#                         comment = c["data"]

#                         comment_author = comment.get("author")
#                         comment_body = comment.get("body")
#                         comment_score = comment.get("score")
#                         comment_created = comment.get("created_utc")

#                         sentiment = get_sentiment(comment_body)

#                         all_data.append({

#                             "keyword": keyword,

#                             "relevance_score": relevance_score,
#                             "match_count": match_count,

#                             "post_id": post_id,
#                             "title": title,
#                             "subreddit": subreddit,
#                             "post_author": author,
#                             "post_upvotes": upvotes,
#                             "total_comments": total_comments,
#                             "post_text": post_text,
#                             "post_url": post_url,
#                             "post_created_utc": created_utc,

#                             "comment_author": comment_author,
#                             "comment": comment_body,
#                             "comment_score": comment_score,
#                             "comment_created_utc": comment_created,

#                             "sentiment": sentiment
#                         })

#                 progress_bar.progress((idx + 1) / len(posts))

#                 time.sleep(2)

#             except Exception as e:

#                 st.error(f"Error processing post: {e}")

#         # =========================================================
#         # CREATE DATAFRAME
#         # =========================================================

#         df = pd.DataFrame(all_data)

#         # =========================================================
#         # EMPTY CHECK
#         # =========================================================

#         if len(df) == 0:

#             st.warning("No highly relevant posts found")
#             st.stop()

#         # =========================================================
#         # STORE SESSION STATE
#         # =========================================================

#         st.session_state.df = df
#         st.session_state.keyword = keyword

#         # =========================================================
#         # TOP POSTS
#         # =========================================================

#         top_posts = (
#             df[
#                 [
#                     "title",
#                     "subreddit",
#                     "relevance_score",
#                     "post_upvotes",
#                     "total_comments",
#                     "post_url"
#                 ]
#             ]
#             .drop_duplicates()
#             .sort_values(
#                 by=[
#                     "relevance_score",
#                     "total_comments"
#                 ],
#                 ascending=False
#             )
#             .head(10)
#         )

#         # =========================================================
#         # POSITIVE COMMENTS
#         # =========================================================

#         positive_comments = (
#             df[
#                 df["sentiment"] == "Positive"
#             ]
#             .sort_values(
#                 by="comment_score",
#                 ascending=False
#             )
#             .head(10)
#         )

#         # =========================================================
#         # NEGATIVE COMMENTS
#         # =========================================================

#         negative_comments = (
#             df[
#                 df["sentiment"] == "Negative"
#             ]
#             .sort_values(
#                 by="comment_score",
#                 ascending=False
#             )
#             .head(10)
#         )

#         # =========================================================
#         # SENTIMENT SUMMARY
#         # =========================================================

#         sentiment_summary = (
#             df["sentiment"]
#             .value_counts()
#             .reset_index()
#         )

#         sentiment_summary.columns = [
#             "Sentiment",
#             "Count"
#         ]

#         # =========================================================
#         # EXCEL EXPORT
#         # =========================================================

#         output = BytesIO()

#         with pd.ExcelWriter(output, engine="openpyxl") as writer:

#             df.to_excel(
#                 writer,
#                 sheet_name="Raw_Data",
#                 index=False
#             )

#             top_posts.to_excel(
#                 writer,
#                 sheet_name="Top_Posts",
#                 index=False
#             )

#             positive_comments.to_excel(
#                 writer,
#                 sheet_name="Positive_Comments",
#                 index=False
#             )

#             negative_comments.to_excel(
#                 writer,
#                 sheet_name="Negative_Comments",
#                 index=False
#             )

#             sentiment_summary.to_excel(
#                 writer,
#                 sheet_name="Sentiment_Summary",
#                 index=False
#             )

#         st.session_state.excel_data = output.getvalue()

# # =========================================================
# # DISPLAY DATA
# # =========================================================

# if st.session_state.df is not None:

#     df = st.session_state.df

#     # =========================================================
#     # ANALYTICS
#     # =========================================================

#     st.header("📈 Analytics")

#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric("Total Rows", len(df))

#     col2.metric(
#         "Positive Comments",
#         len(df[df["sentiment"] == "Positive"])
#     )

#     col3.metric(
#         "Negative Comments",
#         len(df[df["sentiment"] == "Negative"])
#     )

#     col4.metric(
#         "Neutral Comments",
#         len(df[df["sentiment"] == "Neutral"])
#     )

#     # =========================================================
#     # TOP POSTS
#     # =========================================================

#     st.header("🔥 Top Relevant Posts")

#     top_posts = (
#         df[
#             [
#                 "title",
#                 "subreddit",
#                 "relevance_score",
#                 "post_upvotes",
#                 "total_comments",
#                 "post_url"
#             ]
#         ]
#         .drop_duplicates()
#         .sort_values(
#             by=[
#                 "relevance_score",
#                 "total_comments"
#             ],
#             ascending=False
#         )
#         .head(10)
#     )

#     st.dataframe(top_posts, use_container_width=True)

#     # =========================================================
#     # SENTIMENT SUMMARY
#     # =========================================================

#     st.header("😊 Sentiment Distribution")

#     sentiment_summary = (
#         df["sentiment"]
#         .value_counts()
#         .reset_index()
#     )

#     sentiment_summary.columns = [
#         "Sentiment",
#         "Count"
#     ]

#     st.dataframe(sentiment_summary)

#     # =========================================================
#     # POSITIVE COMMENTS
#     # =========================================================

#     st.header("✅ Top 10 Positive Comments")

#     positive_comments = (
#         df[
#             df["sentiment"] == "Positive"
#         ]
#         .sort_values(
#             by="comment_score",
#             ascending=False
#         )
#         .head(10)
#     )

#     st.dataframe(
#         positive_comments[
#             [
#                 "title",
#                 "comment",
#                 "comment_score",
#                 "comment_author",
#                 "relevance_score",
#                 "post_url"
#             ]
#         ],
#         use_container_width=True
#     )

#     # =========================================================
#     # NEGATIVE COMMENTS
#     # =========================================================

#     st.header("❌ Top 10 Negative Comments")

#     negative_comments = (
#         df[
#             df["sentiment"] == "Negative"
#         ]
#         .sort_values(
#             by="comment_score",
#             ascending=False
#         )
#         .head(10)
#     )

#     st.dataframe(
#         negative_comments[
#             [
#                 "title",
#                 "comment",
#                 "comment_score",
#                 "comment_author",
#                 "relevance_score",
#                 "post_url"
#             ]
#         ],
#         use_container_width=True
#     )

#     # =========================================================
#     # RAW DATA
#     # =========================================================

#     st.header("📋 Complete Extracted Data")

#     st.dataframe(df, use_container_width=True)

# # =========================================================
# # DOWNLOAD BUTTON
# # =========================================================

# if st.session_state.excel_data is not None:

#     st.download_button(
#         label="📥 Download Excel Report",
#         data=st.session_state.excel_data,
#         file_name=f"reddit_social_listening_{st.session_state.keyword.replace(' ', '_')}.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )

#     st.success("Excel Report Ready")













import streamlit as st
import requests
import pandas as pd
import time
from textblob import TextBlob
from io import BytesIO

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Reddit Social Listening",
    layout="wide"
)

st.title("📊 Reddit Social Listening Tool")

# =========================================================
# SESSION STATE
# =========================================================

if "excel_data" not in st.session_state:
    st.session_state.excel_data = None

if "df" not in st.session_state:
    st.session_state.df = None

if "keyword" not in st.session_state:
    st.session_state.keyword = None

# =========================================================
# USER INPUT
# =========================================================

keyword = st.text_input(
    "Enter Reddit Search Keyword",
    placeholder="Example: Karnataka IT department"
)

limit = st.slider(
    "Number of Posts to Fetch",
    min_value=5,
    max_value=150,
    value=20
)

sort_option = st.selectbox(
    "Select Reddit Sort Type",
    [
        "relevance",
        "hot",
        "top",
        "new",
        "comments",
        "rising"
    ]
)

min_relevance = st.slider(
    "Minimum Relevance Score",
    min_value=1,
    max_value=15,
    value=5
)

# =========================================================
# SENTIMENT FUNCTION
# =========================================================

def get_sentiment(text):

    try:

        polarity = TextBlob(str(text)).sentiment.polarity

        if polarity > 0:
            return "Positive"

        elif polarity < 0:
            return "Negative"

        else:
            return "Neutral"

    except:

        return "Neutral"

# =========================================================
# RELEVANCE FUNCTION
# =========================================================

def calculate_relevance(title, post_text, subreddit, keyword):

    score = 0
    match_count = 0

    keyword_parts = keyword.lower().split()

    title = str(title).lower()
    post_text = str(post_text).lower()
    subreddit = str(subreddit).lower()

    full_text = title + " " + post_text + " " + subreddit

    for word in keyword_parts:

        if word in full_text:

            match_count += 1

            if word in title:
                score += 5

            if word in post_text:
                score += 3

            if word in subreddit:
                score += 2

    return score, match_count

# =========================================================
# FETCH BUTTON
# =========================================================

if st.button("Fetch Reddit Data"):

    if not keyword:

        st.warning("Please enter keyword")
        st.stop()

    # =========================================================
    # SETTINGS
    # =========================================================

    HEADERS = {
        "User-Agent": "KarnatakaSocialListener/1.0"
    }

    SEARCH_URL = (
        f"https://www.reddit.com/search.json?"
        f"q={keyword}"
        f"&sort={sort_option}"
        f"&limit={limit}"
    )

    # =========================================================
    # FETCH DATA
    # =========================================================

    with st.spinner("Fetching Reddit Posts and Comments..."):

        response = requests.get(
            SEARCH_URL,
            headers=HEADERS
        )

        data = response.json()

        posts = data["data"]["children"]

        st.success(f"Total Posts Pulled From Reddit: {len(posts)}")

        # =========================================================
        # STORE DATA
        # =========================================================

        all_data = []

        progress_bar = st.progress(0)

        # =========================================================
        # LOOP POSTS
        # =========================================================

        for idx, post in enumerate(posts):

            try:

                p = post["data"]

                # =========================================================
                # POST DETAILS
                # =========================================================

                post_id = p.get("id")
                title = p.get("title")
                subreddit = p.get("subreddit")
                author = p.get("author")
                upvotes = p.get("score")
                total_comments = p.get("num_comments")
                post_text = p.get("selftext")
                created_utc = p.get("created_utc")

                post_url = "https://reddit.com" + p.get("permalink")

                # =========================================================
                # RELEVANCE
                # =========================================================

                relevance_score, match_count = calculate_relevance(
                    title,
                    post_text,
                    subreddit,
                    keyword
                )

                if relevance_score < min_relevance:
                    continue

                # =========================================================
                # COMMENTS API
                # =========================================================

                comments_url = (
                    f"https://www.reddit.com/comments/{post_id}.json"
                )

                comments_response = requests.get(
                    comments_url,
                    headers=HEADERS
                )

                comments_data = comments_response.json()

                comments = comments_data[1]["data"]["children"]

                # =========================================================
                # NO COMMENTS
                # =========================================================

                if len(comments) == 0:

                    all_data.append({

                        "keyword": keyword,
                        "relevance_score": relevance_score,
                        "match_count": match_count,

                        "post_id": post_id,
                        "title": title,
                        "subreddit": subreddit,
                        "post_author": author,
                        "post_upvotes": upvotes,
                        "total_comments": total_comments,
                        "post_text": post_text,
                        "post_url": post_url,
                        "post_created_utc": created_utc,

                        "comment_author": None,
                        "comment": None,
                        "comment_score": None,
                        "comment_created_utc": None,

                        "sentiment": "Neutral"
                    })

                # =========================================================
                # LOOP COMMENTS
                # =========================================================

                for c in comments:

                    if c["kind"] == "t1":

                        comment = c["data"]

                        comment_author = comment.get("author")
                        comment_body = comment.get("body")
                        comment_score = comment.get("score")
                        comment_created = comment.get("created_utc")

                        sentiment = get_sentiment(comment_body)

                        all_data.append({

                            "keyword": keyword,

                            "relevance_score": relevance_score,
                            "match_count": match_count,

                            "post_id": post_id,
                            "title": title,
                            "subreddit": subreddit,
                            "post_author": author,
                            "post_upvotes": upvotes,
                            "total_comments": total_comments,
                            "post_text": post_text,
                            "post_url": post_url,
                            "post_created_utc": created_utc,

                            "comment_author": comment_author,
                            "comment": comment_body,
                            "comment_score": comment_score,
                            "comment_created_utc": comment_created,

                            "sentiment": sentiment
                        })

                progress_bar.progress((idx + 1) / len(posts))

                time.sleep(2)

            except Exception as e:

                st.error(f"Error processing post: {e}")

        # =========================================================
        # CREATE DATAFRAME
        # =========================================================

        df = pd.DataFrame(all_data)

        # =========================================================
        # EMPTY CHECK
        # =========================================================

        if len(df) == 0:

            st.warning("No highly relevant posts found")
            st.stop()

        # =========================================================
        # STORE SESSION STATE
        # =========================================================

        st.session_state.df = df
        st.session_state.keyword = keyword

        # =========================================================
        # TOP POSTS
        # =========================================================

        top_posts = (
            df[
                [
                    "title",
                    "subreddit",
                    "relevance_score",
                    "post_upvotes",
                    "total_comments",
                    "post_url"
                ]
            ]
            .drop_duplicates()
            .sort_values(
                by=[
                    "relevance_score",
                    "total_comments"
                ],
                ascending=False
            )
            .head(10)
        )

        # =========================================================
        # POSITIVE COMMENTS
        # =========================================================

        positive_comments = (
            df[
                df["sentiment"] == "Positive"
            ]
            .sort_values(
                by="comment_score",
                ascending=False
            )
            .head(10)
        )

        # =========================================================
        # NEGATIVE COMMENTS
        # =========================================================

        negative_comments = (
            df[
                df["sentiment"] == "Negative"
            ]
            .sort_values(
                by="comment_score",
                ascending=False
            )
            .head(10)
        )

        # =========================================================
        # SENTIMENT SUMMARY
        # =========================================================

        sentiment_summary = (
            df["sentiment"]
            .value_counts()
            .reset_index()
        )

        sentiment_summary.columns = [
            "Sentiment",
            "Count"
        ]

        # =========================================================
        # EXCEL EXPORT
        # =========================================================

        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:

            df.to_excel(
                writer,
                sheet_name="Raw_Data",
                index=False
            )

            top_posts.to_excel(
                writer,
                sheet_name="Top_Posts",
                index=False
            )

            positive_comments.to_excel(
                writer,
                sheet_name="Positive_Comments",
                index=False
            )

            negative_comments.to_excel(
                writer,
                sheet_name="Negative_Comments",
                index=False
            )

            sentiment_summary.to_excel(
                writer,
                sheet_name="Sentiment_Summary",
                index=False
            )

        st.session_state.excel_data = output.getvalue()

# =========================================================
# DISPLAY DATA
# =========================================================

if st.session_state.df is not None:

    df = st.session_state.df

    # =========================================================
    # ANALYTICS
    # =========================================================

    st.header("📈 Analytics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Rows", len(df))

    col2.metric(
        "Positive Comments",
        len(df[df["sentiment"] == "Positive"])
    )

    col3.metric(
        "Negative Comments",
        len(df[df["sentiment"] == "Negative"])
    )

    col4.metric(
        "Neutral Comments",
        len(df[df["sentiment"] == "Neutral"])
    )

    # =========================================================
    # TOP POSTS
    # =========================================================

    st.header("🔥 Top Relevant Posts")

    top_posts = (
        df[
            [
                "title",
                "subreddit",
                "relevance_score",
                "post_upvotes",
                "total_comments",
                "post_url"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            by=[
                "relevance_score",
                "total_comments"
            ],
            ascending=False
        )
        .head(10)
    )

    st.dataframe(top_posts, use_container_width=True)

    # =========================================================
    # SENTIMENT SUMMARY
    # =========================================================

    st.header("😊 Sentiment Distribution")

    sentiment_summary = (
        df["sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment_summary.columns = [
        "Sentiment",
        "Count"
    ]

    st.dataframe(sentiment_summary)

    # =========================================================
    # POSITIVE COMMENTS
    # =========================================================

    st.header("✅ Top 10 Positive Comments")

    positive_comments = (
        df[
            df["sentiment"] == "Positive"
        ]
        .sort_values(
            by="comment_score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        positive_comments[
            [
                "title",
                "comment",
                "comment_score",
                "comment_author",
                "relevance_score",
                "post_url"
            ]
        ],
        use_container_width=True
    )

    # =========================================================
    # NEGATIVE COMMENTS
    # =========================================================

    st.header("❌ Top 10 Negative Comments")

    negative_comments = (
        df[
            df["sentiment"] == "Negative"
        ]
        .sort_values(
            by="comment_score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        negative_comments[
            [
                "title",
                "comment",
                "comment_score",
                "comment_author",
                "relevance_score",
                "post_url"
            ]
        ],
        use_container_width=True
    )

    # =========================================================
    # RAW DATA
    # =========================================================

    st.header("📋 Complete Extracted Data")

    st.dataframe(df, use_container_width=True)

# =========================================================
# DOWNLOAD BUTTON
# =========================================================

if st.session_state.excel_data is not None:

    st.download_button(
        label="📥 Download Excel Report",
        data=st.session_state.excel_data,
        file_name=f"reddit_social_listening_{st.session_state.keyword.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success("Excel Report Ready")
