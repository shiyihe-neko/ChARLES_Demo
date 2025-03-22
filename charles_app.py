import streamlit as st
import pandas as pd
from PIL import Image

st.title("Charles App")

# ---------------------------
# Stage: File Upload (outside forms)
# ---------------------------
source_file = st.file_uploader("Select Source CSV", type=["csv"])
target_file = st.file_uploader("Select Target CSV", type=["csv"])

if source_file and target_file:
    # Read the CSV files
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)

    # Check if the attributes are the same
    source_cols = set(source_df.columns)
    target_cols = set(target_df.columns)
    if source_cols == target_cols:
        st.success("The attributes match between source and target datasets.")
    else:
        st.warning("The attributes are NOT the same between source and target datasets!")

    # ---------------------------
    # Stage 1: Attribute Selection
    # ---------------------------
    # Create a dataframe for attribute selection (all columns)
    df_attributes = pd.DataFrame({
        "Attribute": source_df.columns,
        "Include": [True] * len(source_df.columns)
    })

    st.write("### Stage 1: Select Attributes to Include")
    with st.form(key="stage1"):
        edited_df = st.data_editor(
            df_attributes,
            num_rows="dynamic",
            use_container_width=True
        )
        condition = st.slider("Condition", 0, 10, 3)
        transformation = st.slider("Transformation", 0, 10, 3)
        submitted_stage1 = st.form_submit_button("Confirm")
        if submitted_stage1:
            st.session_state.confirmed = True
            st.session_state.selected_attributes = edited_df[edited_df["Include"] == True]["Attribute"].tolist()
            st.session_state.condition = condition
            st.session_state.transformation = transformation

            # Prepare dataframes for numeric and non-numeric attributes
            numeric_cols = source_df.select_dtypes(include=["number"]).columns.tolist()
            non_numeric_cols = source_df.select_dtypes(exclude=["number"]).columns.tolist()
            st.session_state.numeric_df = pd.DataFrame({
                "Attribute": numeric_cols,
                "Include": [True] * len(numeric_cols)
            })
            st.session_state.non_numeric_df = pd.DataFrame({
                "Attribute": non_numeric_cols,
                "Include": [True] * len(non_numeric_cols)
            })

    # ---------------------------
    # Stage 2: Attribute Categorization
    # ---------------------------
    if st.session_state.get("confirmed", False):
        st.write("### Stage 2: Categorize Attributes")
        with st.form(key="stage2"):
            edited_numeric_df = st.data_editor(
                st.session_state.numeric_df,
                use_container_width=True
            )
            edited_non_numeric_df = st.data_editor(
                st.session_state.non_numeric_df,
                use_container_width=True
            )
            weight_accuracy = st.slider("Weight of Accuracy (α)", 0.0, 1.0, 0.5)
            submitted_stage2 = st.form_submit_button("Compare")
            if submitted_stage2:
                st.session_state.compared = True
                st.session_state.selected_numeric_attrs = edited_numeric_df[edited_numeric_df["Include"] == True]["Attribute"].tolist()
                st.session_state.selected_non_numeric_attrs = edited_non_numeric_df[edited_non_numeric_df["Include"] == True]["Attribute"].tolist()
                st.session_state.weight_accuracy = weight_accuracy

    # ---------------------------
    # Stage 3: Transformation Results
    # ---------------------------
    if st.session_state.get("compared", False):
        st.write("### Stage 3: Transformation Results")
        st.write("**Selected columns:**", st.session_state.selected_attributes)
        st.write("**Condition:**", st.session_state.condition)
        st.write("**Transformation:**", st.session_state.transformation)
        st.write("**Transformation Attributes (Numeric):**", st.session_state.selected_numeric_attrs)
        st.write("**Condition Attributes (Non-Numeric):**", st.session_state.selected_non_numeric_attrs)
        st.write("**Weight of Accuracy (α):**", st.session_state.weight_accuracy)

        # Example transformation results (hard-coded)
        data = {
            "Summary": [
                "Gender = M -> Current Annual Salary (0.9)",
                "Gender = F -> Current Annual Salary (1.1)",
                "Gender = M -> 2016 Gross Pay (1.05)",
                "Department = HR -> 2016 Overtime Pay (0.8)",
                "Employee Position Title = Firefighter -> Current Annual Salary (1.2)",
                "Employee Position Title = Police -> 2016 Gross Pay (1.1)",
                "Department = IT -> Current Annual Salary (0.95)",
                "Gender = F -> 2016 Overtime Pay (1.0)",
                "Department = Finance -> Current Annual Salary (1.05)",
                "Gender = M -> 2016 Gross Pay (0.9)"
            ],
            "Status": ["OK"] * 10,
            "Accuracy": [95.7, 93.2, 94.5, 92.6, 95.1, 96.3, 94.9, 95.0, 93.8, 94.0],
            "Improvement": [72.0, 71.5, 73.1, 70.2, 75.6, 76.3, 74.5, 71.9, 73.0, 70.7]
        }
        df_table = pd.DataFrame(data)

        # Create a blue square as a placeholder transformation image
        blue_square = Image.new("RGB", (200, 200), color=(0, 0, 255))

        top_n = st.number_input("Show the top X summaries", min_value=1, max_value=len(df_table), value=5)

        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.write("### Summaries")
            # Display the top N rows
            for i, row in df_table.head(top_n).iterrows():
                st.write(
                    f"**{i+1}. Summary:** {row['Summary']} | "
                    f"**Status:** {row['Status']} | "
                    f"**Accuracy:** {row['Accuracy']}% | "
                    f"**Improvement:** {row['Improvement']}%"
                )
                # Each row has a "Details" button
                if st.button(f"Details_{i}"):
                    st.session_state.selected_row = i

        with col_right:
            if "selected_row" in st.session_state:
                selected_idx = st.session_state["selected_row"]
                st.write(f"### Details for Row {selected_idx + 1}")
                st.image(blue_square, caption="Transformation Visualization")
