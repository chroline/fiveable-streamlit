import streamlit as st
import pandas as pd


def process_csv(file):
    df = pd.read_csv(file, skiprows=3)
    duplicate_terms = df[df.duplicated(df.columns[1])][df.columns[1]].unique()  # Find duplicates in the 2nd column
    unique_categories = df.iloc[:, 2].unique()  # Get unique values from the 3rd column

    # Remove NaN values
    unique_categories = [value for value in unique_categories if pd.notna(value)]

    st.header("Output")

    st.subheader("List of Categories")
    st.markdown("* " + "\n* ".join(set(unique_categories)))

    # Print duplicates in the 2nd column
    st.subheader("Duplicate Terms")
    if len(duplicate_terms) > 0:
        st.markdown("* " + "\n* ".join(set(duplicate_terms)))
    else:
        st.write("No duplicate terms found.")

    return df


# Main Streamlit app code
def main():
    st.title("Terms List Tool")
    st.subheader("Extract categories and duplicates")

    # File upload widget
    uploaded_file = st.file_uploader("Upload terms list file", type="csv")

    if uploaded_file is not None:
        # Process the uploaded file
        process_csv(uploaded_file)


# Run the Streamlit app
if __name__ == "__main__":
    main()
