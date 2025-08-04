# Library
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    avg,
    date_format,
    datediff,
    col,
    lag,
    lit,
    round,
    monotonically_increasing_id,
)
from pyspark.sql import Window
import matplotlib.pyplot as plt


# Schema
from spark.GitHub.SparkSchema import schema_issue


# Utils
from utils.function.FuncSpark import import_spark_csv, schema_nested_parsed


def create_dataframe(spark: SparkSession, csv_file: str) -> DataFrame:

    df = import_spark_csv(spark, csv_file)

    df = schema_nested_parsed(df=df, schemas=schema_issue())

    # Select and alias specific columns with index
    df_res = df.select(
        monotonically_increasing_id().alias("index"),
        col("number").alias("issue_number"),
        "state",
        "comments",
        "comments_url",
        col("user.id").alias("created_by_user_id"),
        col("created_at").alias("created_date"),
        col("closed_by.id").alias("closed_by_user_id"),
        col("closed_at").alias("closed_date"),
    )
    total = df_res.count()

    print(f"\n")
    print(f'🚀 DATAFRAME_LOADED Total "{total}" records')
    df_res.show()
    # df_res.show(n=total, truncate=False)

    return df


def analysis_average_resolution(df: DataFrame) -> DataFrame:

    df_res = (
        df.filter(col("state") == "closed")
        .withColumn("created_at", col("created_at"))
        .withColumn("closed_at", col("closed_at"))
        .withColumn("resolution_days", datediff(col("closed_at"), col("created_at")))
        .withColumn("month", date_format(col("created_at"), "yyyy-MM"))
        .groupBy("month")
        .agg(round(avg("resolution_days"), 2).alias("avg_resolution_days"))
        .orderBy("month")
    )

    total = df_res.count()
    # selected_columns = ["user.id", "body", "created_at"]
    # df_res = df_res.select(*selected_columns)

    print(f"\n✨ Average resolution time by month")
    print(f'Total "{total}" records')
    df_res.show(n=total, truncate=False)

    return df_res


def analysis_creation_trend(df: DataFrame) -> DataFrame:

    window = Window.partitionBy(lit(1)).orderBy("month")
    df_res = (
        df.withColumn("month", date_format(col("created_at"), "yyyy-MM"))
        .groupBy("month")
        .count()
        .withColumn("prev_count", lag("count", 1).over(window))
        .withColumn(
            "percentage_change",
            round(((col("count") - col("prev_count")) / col("prev_count")) * 100, 2),
        )
        .na.fill(0)
        .orderBy("month")
    )

    total = df_res.count()

    print(f"\n✨ Monthly issue creation trend")
    print(f'Total "{total}" records')
    df_res.show(n=total, truncate=False)

    return df_res


def visualize_creation_trend(df: DataFrame, title: str):
    """Visualize monthly trends using matplotlib"""
    # Convert to Pandas for visualization
    pandas_df = df.toPandas()

    # Create figure and axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Bar plot for issue counts
    ax1.bar(pandas_df["month"], pandas_df["count"], color="skyblue")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Issue Count", color="skyblue")
    ax1.tick_params(axis="y", labelcolor="skyblue")

    # Line plot for percentage change
    ax2 = ax1.twinx()
    ax2.plot(pandas_df["month"], pandas_df["percentage_change"], "r-*", markersize=8)
    ax2.set_ylabel("Percentage Change (%)", color="red")
    ax2.tick_params(axis="y", labelcolor="red")
    ax2.axhline(0, color="gray", linestyle="--")

    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def sql_analysis_average_resolution(spark: SparkSession, df: DataFrame) -> DataFrame:
    """Calculate average issue resolution time by month using SQL"""

    df.createOrReplaceTempView("issues")

    sql_query = """
        SELECT
            DATE_FORMAT(created_at, 'yyyy-MM') AS month,
            ROUND(AVG(DATEDIFF(closed_at, created_at)), 2) AS avg_resolution_days
        FROM issues
        WHERE state = 'closed'
        GROUP BY month
        ORDER BY month
    """

    df_res = spark.sql(sql_query)

    total = df_res.count()

    print(f"\n✨ SQL Query : Average resolution time by month")
    print(f'Total "{total}" records')
    df_res.show(n=total, truncate=False)

    return df_res
