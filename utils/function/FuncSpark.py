# Library
from typing import Any
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    StructType,
    StringType,
    ArrayType,
    IntegerType,
    BooleanType,
    TimestampType,
)
from pyspark.sql.functions import from_json, col

# Convert Python-style string representations to JSON strings for complex columns
import json
from ast import literal_eval
from pyspark.sql.functions import udf


# Utils
from utils.constant import FOLDER_OUTPUT


def import_spark_csv(spark: SparkSession, csv_file: str) -> DataFrame:

    # csv_file = f"github_issues_Uniswap_v3-core.csv"
    csv_path = f"{FOLDER_OUTPUT}/{csv_file}"

    # Contributors table
    # Read the CSV as strings for nested columns
    # parse the records correctly from CSV
    df = (
        spark.read.option("header", "true")
        .option("multiLine", "true")  # Multi-line records
        .option("quote", '"')  # Fields containing newlines (\n)
        .option("escape", '"')  # Quoted fields with escaped quotes ("")
        .csv(csv_path)
    )

    total = df.count()
    print(f"\n")
    print(f'🚀  DATAFRAME_LOADED "{total}" records from "{csv_path}"')

    return df


def convert_python_repr_to_json(s):

    # Added a UDF to convert Python-style string representations to valid JSON strings
    if s is None or s == "":
        return None
    try:
        # If it's already valid JSON, return it
        json.loads(s)
        return s
    except json.JSONDecodeError:
        try:
            obj = literal_eval(s)
            return json.dumps(obj)
        except:
            # If we can't convert, return the original string
            return s


def schema_nested_parsed(df: DataFrame, schemas: dict[str, Any]) -> DataFrame:
    # Define schemas for nested columns

    complex_columns = {
        k: v for k, v in schemas.items() if isinstance(v, (StructType, ArrayType))
    }
    simple_columns = {
        k: v for k, v in schemas.items() if not isinstance(v, (StructType, ArrayType))
    }

    # Cast simple columns to correct types
    for column_name, schema in simple_columns.items():
        if isinstance(schema, StringType):
            df = df.withColumn(column_name, col(column_name).cast(StringType()))
        elif isinstance(schema, IntegerType):
            df = df.withColumn(column_name, col(column_name).cast(IntegerType()))
        elif isinstance(schema, BooleanType):
            df = df.withColumn(column_name, col(column_name).cast(BooleanType()))
        elif isinstance(schema, TimestampType):
            df = df.withColumn(column_name, col(column_name).cast(TimestampType()))

    # Debug: show the first row of the column
    # if "user" in complex_columns:
    #     print("\n🐛 DEBUG: First row of 'user' column before parsing:")
    #     df.select("user").show(1, truncate=False)

    convert_python_repr_to_json_udf = udf(convert_python_repr_to_json, StringType())

    for column_name, schema in complex_columns.items():
        # Convert the column from Python string representation to JSON string
        df = df.withColumn(
            column_name, convert_python_repr_to_json_udf(col(column_name))
        )

        # Now parse the JSON
        df = df.withColumn(
            column_name,
            from_json(col(column_name), schema, {"allowSingleQuotes": "true"}),
        )

    print(f"\n")
    print(f"📜  DATAFRAME_SCHEMA")
    df.printSchema()

    return df
