# import streamlit as st
# import pandas as pd
# import numpy as np
# from datetime import datetime

# def recommend_sql_type(col_name, min_val, max_val, dtype):
#     if pd.api.types.is_string_dtype(dtype):
#         max_length = max(len(str(min_val)), len(str(max_val)))
#         if max_length <= 255:
#             return f"VARCHAR({max_length})"
#         else:
#             return "TEXT"
#     elif pd.api.types.is_integer_dtype(dtype):
#         if min_val >= 0:
#             if max_val <= 255:
#                 return "TINYINT UNSIGNED"
#             elif max_val <= 65535:
#                 return "SMALLINT UNSIGNED"
#             elif max_val <= 16777215:
#                 return "MEDIUMINT UNSIGNED"
#             elif max_val <= 4294967295:
#                 return "INT UNSIGNED"
#             else:
#                 return "BIGINT UNSIGNED"
#         else:
#             if min_val >= -128 and max_val <= 127:
#                 return "TINYINT"
#             elif min_val >= -32768 and max_val <= 32767:
#                 return "SMALLINT"
#             elif min_val >= -8388608 and max_val <= 8388607:
#                 return "MEDIUMINT"
#             elif min_val >= -2147483648 and max_val <= 2147483647:
#                 return "INT"
#             else:
#                 return "BIGINT"
#     elif pd.api.types.is_float_dtype(dtype):
#         if -3.4e38 <= min_val <= max_val <= 3.4e38:
#             return "FLOAT"
#         else:
#             return "DOUBLE"
#     elif pd.api.types.is_datetime64_any_dtype(dtype):
#         return "DATETIME"
#     elif pd.api.types.is_timedelta64_dtype(dtype):
#         return "TIME"
#     elif pd.api.types.is_bool_dtype(dtype):
#         return "BOOLEAN"
#     elif pd.api.types.is_categorical_dtype(dtype):
#         return "ENUM"
#     else:
#         return "TEXT"

# def get_decimal_places(value):
#     return abs(decimal.Decimal(str(value)).as_tuple().exponent)

# st.title("Universal Dataset Analyzer and SQL Type Recommender")

# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
    
#     results = []
    
#     for col in df.columns:
#         min_val = df[col].min()
#         max_val = df[col].max()
#         dtype = df[col].dtype
#         sql_type = recommend_sql_type(col, min_val, max_val, dtype)
        
#         # Additional logic for DECIMAL type
#         if sql_type in ["FLOAT", "DOUBLE"]:
#             max_decimal_places = max(get_decimal_places(min_val), get_decimal_places(max_val))
#             max_integer_digits = max(len(str(int(abs(min_val)))), len(str(int(abs(max_val)))))
#             total_digits = max_integer_digits + max_decimal_places
#             if total_digits <= 65:
#                 sql_type = f"DECIMAL({total_digits},{max_decimal_places})"
        
#         results.append({
#             "Column": col,
#             "Min": min_val,
#             "Max": max_val,
#             "Python Type": dtype,
#             "Recommended SQL Type": sql_type
#         })
    
#     result_df = pd.DataFrame(results)
#     st.write(result_df)
    
#     st.download_button(
#         label="Download results as CSV",
#         data=result_df.to_csv(index=False).encode('utf-8'),
#         file_name="column_analysis.csv",
#         mime="text/csv"
#     )
# else:
#     st.write("Please upload a CSV file to begin analysis.")

TypeError: '<=' not supported between instances of 'float' and 'str'

