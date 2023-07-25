import openai
import pandas as pd
import streamlit as st


openai.api_key = st.secrets['openai_api_key']

default_prompt = """\
Write an article for Fiveable titled "{article_title}". I will provide you with a list of sub-topics to include.

Here are the topics to include:
{topics}

Use an H2 heading for each topic in the following format: "## [EMOJI] [TOPIC]\\n" and nothing else.

Please write ~1 paragraph for each sub-topic.

Please also write a very brief introduction that reiterates the main topic. Don't add the title in your response.

Write your response in an engaging tone using everyday language and casual expressions.

Avoid libertarian or conservative stances.

When necessary, incorporate relevant visual elements such as emojis and tables to support your explanation. Limit 1-2 emojis per paragraph.

Use first-person narration and occasional interjections to make the reader feel like they're in a personal conversation with you.

Use current affairs, historical facts, or real-world examples to illustrate your points.

Although the tone should be informal, ensure the content remains informative and academically accurate.

Engage the reader with rhetorical questions to provoke thought and underline important points.

Make sure your tone is friendly, warm, and encouraging throughout your response.

Paragraphs should cite specific information, not just generalizations.\
"""

st.title("Listicle Generator")
st.subheader("Generate Fiveable listicle content using ChatGPT")


def generate_topics(df):
    return "- " + "\n- ".join([f"{row['Term']}: {row['Definition']}" for index, row in df.iterrows()])


def process_csv(file):
    st.header("Output")

    df = pd.read_csv(file, skiprows=2)
    st.dataframe(df)

    topics = None

    col1, col2 = st.columns(2)
    with col1:
        categories = df["Category"].unique().astype(str)
        st.markdown("**Generate topics from category:**")
        for value in categories[categories != 'nan']:
            if st.button(value):
                topics = generate_topics(df[df['Category'] == value])
    with col2:
        key_topics = df.iloc[:, 0].astype(str).unique().astype(str)
        st.markdown("**Generate topics from key topic:**")
        for value in key_topics[key_topics != 'nan']:
            if st.button(value):
                topics = generate_topics(df[df.iloc[:, 0] == value])

    return topics

def main():
    # File upload widget
    uploaded_file = st.file_uploader("Upload terms list file", type="csv")

    if 'topics' not in st.session_state:
        st.session_state['topics'] = None

    if uploaded_file is not None:
        # Process the uploaded file
        new_topics = process_csv(uploaded_file)
        st.session_state["topics"] = new_topics if new_topics is not None else st.session_state["topics"]

    topics = st.session_state["topics"]

    if topics is not None:
        st.divider()

        # Text input for the title
        article_title = st.text_input("Title", "")

        topics_count = len(topics.split('\n'))
        st.text_area(f"{topics_count} topics:", topics)

        prompt = st.text_area('Prompt', default_prompt)
        st.caption("Ensure that {article_title} and {topics} is included in your prompt!")

        # Button to submit the list
        if st.button("Generate"):
            # Split the input by new lines and remove leading/trailing spaces
            st.markdown("----")
            res_box = st.empty()

            msg = prompt.format(article_title=article_title, topics=topics)

            req = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                               messages=[
                                                   {"role": "system", "content": msg}
                                               ],
                                               max_tokens=2048,
                                               temperature=1,
                                               stream=True)

            report = []
            result = ""
            for resp in req:
                try:
                    report.append(resp.choices[0].delta.content)
                    result = "".join(report).strip()
                    res_box.markdown(f'{result}')
                except:
                    pass

            st.divider()
            st.text_area("Output", result)


if __name__ == '__main__':
    main()
