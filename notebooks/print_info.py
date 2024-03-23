import pandas as pd


def column_info(df: pd.DataFrame):
    print("Информация о колонках:")
    for column in df.columns:
        unique_count = (
            df[column]
            .apply(lambda x: str(x) if isinstance(x, list) else x)
            .nunique(dropna=False)
        )
        data_type = df[column].dtype
        nan_count = df[column].isna().sum()
        print(
            f"Колонка '{column}': количество уникальных значений = {unique_count}, тип данных = {data_type}, количество NaN = {nan_count}"
        )
    print("Размерность: ", df.shape)


def rare_category_info(df: pd.DataFrame, column: str, rare_threshold: int = 10):
    counts = df[column].value_counts()
    filtered_counts = counts[counts < rare_threshold]
    for value, count in filtered_counts.items():
        print(f"{value}: {count}")
        
        

def unique_categorical_values_info(df: pd.DataFrame):
    categorical_columns = df.select_dtypes(include=['category']).columns
    for column in categorical_columns:
        unique_values = df[column].unique()
        print(f"Уникальные значения в столбце {column}: {list(unique_values)}")


