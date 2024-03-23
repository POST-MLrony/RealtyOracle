import pandas as pd


def column_info(df: pd.DataFrame) -> None:
    """Печатает информацию о колонках DataFrame.

    Args:
        df (pd.DataFrame): DataFrame, для которого нужно вывести информацию о колонках.

    Returns:
        None

    Description:
        Эта функция выводит информацию о каждой колонке DataFrame, включая количество уникальных значений,
        тип данных и количество пропущенных значений (NaN).

    """
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


def rare_category_info(df: pd.DataFrame, column: str, rare_threshold: int = 10) -> None:
    """Печатает информацию о редких категориях в указанном столбце DataFrame.

    Args:
        df (pd.DataFrame): DataFrame, для которого нужно найти редкие категории.
        column (str): Название столбца, в котором нужно найти редкие категории.
        rare_threshold (int, optional): Пороговое значение для определения редких категорий.
            Категории, встречающиеся реже, чем указанное значение, будут считаться редкими.
            По умолчанию установлено значение 10.

    Returns:
        None

    Description:
        Эта функция выводит информацию о редких категориях в указанном столбце DataFrame.
        Категории, встречающиеся реже, чем пороговое значение, будут распечатаны с их частотой встречаемости.

    """
    counts = df[column].value_counts()
    filtered_counts = counts[counts < rare_threshold]
    for value, count in filtered_counts.items():
        print(f"{value}: {count}")


def unique_categorical_values_info(df: pd.DataFrame) -> None:
    """Печатает уникальные категориальные значения для всех столбцов DataFrame.

    Args:
        df (pd.DataFrame): DataFrame, для которого нужно вывести уникальные категориальные значения.

    Returns:
        None

    Description:
        Эта функция выводит уникальные категориальные значения для всех столбцов DataFrame,
        которые имеют тип данных 'category'.

    """
    categorical_columns = df.select_dtypes(include=["category"]).columns
    for column in categorical_columns:
        unique_values = df[column].unique()
        print(f"Уникальные значения в столбце {column}: {list(unique_values)}")
