import streamlit as st
import pandas as pd

# 1. 设置为宽屏，并通过自定义 CSS 限制最大宽度，且取消居中效果（使内容靠左）
st.set_page_config(layout="wide")
st.markdown("""
<style>
/* 限制主内容区最大宽度，并靠左显示 */
.main .block-container {
    max-width: 800px;  
    margin: 0;  /* 左上对齐 */
}
</style>
""", unsafe_allow_html=True)

# 2. 创建四个象限：上行分为左、右两个象限，下行同理
top_left, top_right = st.columns(2)
bottom_left, bottom_right = st.columns(2)

with top_left:
    st.title("Charles App")
    
    # 第一行：并排放置两个上传框
    col_file_left, col_file_right = st.columns(2)
    with col_file_left:
        source_file = st.file_uploader("Select Source CSV", type=["csv"])
    with col_file_right:
        target_file = st.file_uploader("Select Target CSV", type=["csv"])
    
    # 当两个文件都上传后，进行后续处理
    if source_file and target_file:
        source_df = pd.read_csv(source_file)
        target_df = pd.read_csv(target_file)
        total_columns = len(source_df.columns)

        # 计算 source_df 中数值型列的数量
        # 注：'number' 会匹配 int、float 等常见数值类型
        numeric_columns = len(source_df.select_dtypes(include=["number"]).columns)
        if set(source_df.columns) == set(target_df.columns):
            # 找到值发生变化的列
            changed_attributes = [
                col for col in source_df.columns
                if not source_df[col].equals(target_df[col])
            ]

            if changed_attributes:
                st.markdown("### 选择需要用到的属性（仅显示值发生变化的属性）")

                # 1. 构造 DataFrame，其中「Include」列用于勾选
                df_changed = pd.DataFrame({
                    "Attribute": changed_attributes,
                    "Include": [False] * len(changed_attributes)  # 默认全部勾选
                })

                # 2. 用 data_editor 展示并让用户勾选
                edited_changed_df = st.data_editor(
                    df_changed,
                    num_rows="dynamic",         # 如果列很多，可开启滚动
                    use_container_width=True    # 自适应宽度
                )

                # 3. 读取勾选结果
                selected_attributes = edited_changed_df[
                    edited_changed_df["Include"] == True
                ]["Attribute"].tolist()

                st.write("**已选属性：**", selected_attributes)

            else:
                st.info("两个 CSV 文件的所有列值均未发生变化。")
        else:
            st.error("上传的 CSV 文件列不一致，请检查后重试。")

        condition = st.slider("Condition", min_value=0, max_value=total_columns, value=3)
        transformation = st.slider("Transformation", min_value=0, max_value=numeric_columns, value=3)


        if st.button("Confirm"):
            selected_cols = edited_changed_df[edited_changed_df["Include"] == True]["Attribute"].tolist()
            st.write("### Form Submitted!")
            st.write("**Selected columns:**", selected_cols)
            st.write("**Condition:**", condition)
            st.write("**Transformation:**", transformation)
            
with top_right:
    # 上右象限预留空白或其他内容
    st.empty()

with bottom_left:
    # 下左象限预留空白或其他内容
    st.empty()

with bottom_right:
    # 下右象限预留空白或其他内容
    st.empty()
