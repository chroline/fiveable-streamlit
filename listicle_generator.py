import re

import openai
import streamlit as st


class SessionState:
    def __init__(self):
        self.data = []


openai.api_key = st.secrets['openai_api_key']

prompt = """
Write an article for Fiveable titled "{article_title}". I will provide you with a list of sub-topics to include. Please write ~1 paragraph for each sub-topic, and make an H2 heading for each.

Here are the topics to include:
{topics}

Please also write a very brief introduction that reiterates the main topic. Don't add the title in your response.

Write your response in a conversational and engaging tone using everyday language and casual expressions. Engage with the reader directly using the second person. Incorporate ample relevant visual elements such as emojis and tables to support your explanation. Use first-person narration and occasional interjections to make the reader feel like they're in a personal conversation with you. Use current affairs, historical facts, or real-world examples to illustrate your points. Be sure to emphasize key points for easy recall. Although the tone should be informal, ensure the content remains informative and academically accurate. Engage the reader with rhetorical questions to provoke thought and underline important points.

Make sure your tone is friendly, warm, and encouraging throughout your response.

When using ordered or numbered list, make them in Markdown format. Use markdown headings.

Don't prompt the user to respond or launch into a discussion, but feel free to use rhetorical questions.

Paragraphs should cite specific information, not just generalizations.
"""

st.title("Listicle Generator")
st.subheader("Generate Fiveable listicle content using AI!")


def main():
    # Text input for the title
    article_title = st.text_input("Title", "")

    # Text area input for the list
    st.write("Enter a list of topics below, with each item on a new line:")
    topics = st.text_area("Topics", "")

    # Button to submit the list
    if st.button("Submit"):
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
