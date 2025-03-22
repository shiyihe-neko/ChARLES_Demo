import streamlit as st

st.title('Charles App')

import streamlit as st
import pandas as pd

st.title("Attribute Selection Demo")

# 1. Select Source and Target Datasets
source_file = st.file_uploader("Select Source CSV", type=["csv"])
target_file = st.file_uploader("Select Target CSV", type=["csv"])

# Only proceed if both files are uploaded
if source_file and target_file:
    # Read in the CSV files
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)

    # 2. Check if the attributes are the same
    source_cols = set(source_df.columns)
    target_cols = set(target_df.columns)

    if source_cols == target_cols:
        st.success("The attributes match between source and target datasets.")
    else:
        st.warning("The attributes are NOT the same between source and target datasets!")

    # Prepare a DataFrame for editing:
    # This table will contain all columns from the source dataset.
    # The "Include" column (boolean) lets the user choose which columns to keep.
    df_attributes = pd.DataFrame({
        "Attribute": source_df.columns,
        "Include": [True] * len(source_df.columns)  # Default to True
    })

    st.write("### Select Attributes to Include")
    # 2. Use a scrollable table to choose if we need each attribute
    edited_df = st.data_editor(
        df_attributes,
        num_rows="dynamic",  # Allows the user to scroll
        use_container_width=True
    )

    # 3. Choose condition and transformation (range 0 to 10)
    #TODO currently set range from 0 to 10, change it according to number of attributes
    condition = st.slider("Condition", 0, 10, 3)
    transformation = st.slider("Transformation", 0, 10, 3)

    # 4. Confirm button
    if st.button("Confirm"):
        # Get the list of attributes the user wants to include
        selected_attributes = edited_df[edited_df["Include"] == True]["Attribute"].tolist()

        st.write("### Form Submitted!")
        st.write("**Selected columns:**", selected_attributes)
        st.write("**Condition:**", condition)
        st.write("**Transformation:**", transformation)

        # Here, you could do any additional processing you need
        # (e.g., filter the DataFrame by selected columns, apply transformations, etc.)
