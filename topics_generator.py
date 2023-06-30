import streamlit as st
import pandas as pd


def generate_topics(df):
    return "- "+"\n- ".join([f"{row['Term']}: {row['Definition']}" for index, row in df.iterrows()])

def process_csv(file):
    st.header("Output")

    df = pd.read_csv(file, skiprows=2)
    st.dataframe(df.sort_values(by='Key Topic'))

    topics = ""

    # Create two columns
    col1, col2 = st.columns(2)

    # Add content to the first column
    with col1:
        categories = df["Category"].unique()
        st.markdown("**Generate topics from category:**")
        for value in categories:
            if st.button(value):
                topics = generate_topics(df[df['Category'] == value])

    # Add content to the second column
    with col2:
        key_topics = df["Key Topic"].astype(str).unique()
        st.markdown("**Generate topics from key topic:**")
        for value in key_topics:
            if st.button(value):
                topics = generate_topics(df[df['Key Topic'].astype(str) == value])

    st.text_area("Topics:", topics)


# Main Streamlit app code
def main():
    st.title("Topics Generator")
    st.subheader("Generate a list of topics from a terms list.")

    # File upload widget
    uploaded_file = st.file_uploader("Upload terms list file", type="csv")

    if uploaded_file is not None:
        # Process the uploaded file
        process_csv(uploaded_file)


# Run the Streamlit app
if __name__ == "__main__":
    main()
