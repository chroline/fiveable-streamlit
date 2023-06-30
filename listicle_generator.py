import re

import openai
import streamlit as st


class SessionState:
    def __init__(self):
        self.data = []


openai.api_key = st.secrets['openai_api_key']

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251" 
    "]+"
)

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
        items = [item.strip() for item in topics.split("\n")]
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

                lines = result.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('#'):
                        heading_without_emojis = EMOJI_PATTERN.sub('', line)
                        lines[i] = heading_without_emojis.strip()

                result = '\n'.join(lines)

                res_box.markdown(f'{result}')
            except:
                pass

        st.divider()
        st.text_area("Output", result)



if __name__ == '__main__':
    main()
