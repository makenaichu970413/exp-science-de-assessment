# Library
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, desc, monotonically_increasing_id

# Schema
from spark.GitHub.SparkSchema import schema_comment


# Utils
from utils.function.FuncSpark import import_spark_csv, schema_nested_parsed


def create_dataframe(spark: SparkSession, csv_file: str) -> DataFrame:

    df = import_spark_csv(spark, csv_file)

    df = schema_nested_parsed(df=df, schemas=schema_comment())

    # Select and alias specific columns with index
    df_res = df.select(
        monotonically_increasing_id().alias("index"),
        col("user.id").alias("user_id"),
        "url",
        col("body").alias("body"),
        col("created_at").alias("created_date"),
    )
    total = df_res.count()

    print(f"\n")
    print(f'🚀 DATAFRAME_LOADED Total "{total}" records')
    df_res.show()
    # df_res.show(n=total, truncate=True)

    return df


def analysis_top_10_commenters(df: DataFrame) -> DataFrame:

    df_res = df.groupBy("user.id").count().orderBy(desc("count")).limit(10)

    total = df_res.count()

    print(f"\n✨ Top 10 commenters")
    print(f'Total "{total}" records')
    df_res.show(n=total, truncate=False)

    return df_res
