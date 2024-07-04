import streamlit as st
import pandas as pd

def is_numeric(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def safe_convert_to_numeric(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None

def recommend_sql_type(col_name, series):
    if series.dtype == 'object':
        if series.apply(lambda x: isinstance(x, str)).all():
            max_length = series.str.len().max()
            return f"VARCHAR({max_length})" if max_length <= 255 else "TEXT"
        else:
            return "TEXT"
    elif pd.api.types.is_integer_dtype(series):
        min_val, max_val = series.min(), series.max()
        if min_val >= 0:
            if max_val <= 255:
                return "TINYINT UNSIGNED"
            elif max_val <= 65535:
                return "SMALLINT UNSIGNED"
            elif max_val <= 16777215:
                return "MEDIUMINT UNSIGNED"
            elif max_val <= 4294967295:
                return "INT UNSIGNED"
            else:
                return "BIGINT UNSIGNED"
        else:
            if min_val >= -128 and max_val <= 127:
                return "TINYINT"
            elif min_val >= -32768 and max_val <= 32767:
                return "SMALLINT"
            elif min_val >= -8388608 and max_val <= 8388607:
                return "MEDIUMINT"
            elif min_val >= -2147483648 and max_val <= 2147483647:
                return "INT"
            else:
                return "BIGINT"
    elif pd.api.types.is_float_dtype(series):
        return "DOUBLE"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "DATETIME"
    elif pd.api.types.is_timedelta64_dtype(series):
        return "TIME"
    elif pd.api.types.is_bool_dtype(series):
        return "BOOLEAN"
    elif pd.api.types.is_categorical_dtype(series):
        return "ENUM"
    else:
        return "TEXT"

st.title("Dataset analyzer / SQL data type recommender")

st.write("""
## Instructions
Please ensure your dataset is structured as follows before uploading:

1. **File Format**: CSV or Excel (XLSX, XLS)
2. **Column Headers**: Include column headers in the first row.
3. **Data Types**: Ensure columns contain consistent data types:
   - Numeric (integer or float)
   - Text (string)
   - Date/Time
   - Boolean (True/False)
4. **No Mixed Types**: Avoid mixing different data types within the same column.
5. **Missing Values**: Handle missing values appropriately (e.g., leave cells empty, use NaN, etc.).

Example:

| ID  | Name      | Age | Date of Birth | Active |
|-----|-----------|-----|---------------|--------|
| 1   | John Doe  | 30  | 1993-04-01    | True   |
| 2   | Jane Smith| 25  | 1998-11-22    | False  |
| ... | ...       | ... | ...           | ...    |

""")

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    try:
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        st.stop()
    
    results = []
    
    for col in df.columns:
        series = df[col]
        sql_type = recommend_sql_type(col, series)
        
        if pd.api.types.is_numeric_dtype(series):
            min_val = series.min()
            max_val = series.max()
        else:
            min_val = None
            max_val = None
        
        results.append({
            "Column": col,
            "Min": min_val,
            "Max": max_val,
            "Python Type": series.dtype,
            "Recommended SQL Type": sql_type
        })
    
    result_df = pd.DataFrame(results)
    st.write(result_df)
    
    st.download_button(
        label="Download results as CSV",
        data=result_df.to_csv(index=False).encode('utf-8'),
        file_name="column_analysis.csv",
        mime="text/csv"
    )
else:
    st.write("Please upload a CSV or Excel file to begin analysis.")



