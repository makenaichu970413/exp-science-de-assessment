# Library
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip
import getpass
import os
import sys

# Utils
from utils.constant import FOLDER_SPARK_TEMP, HADOOP_HOME, JAVA_HOME


def init() -> SparkSession:

    os.environ["HADOOP_USER_NAME"] = getpass.getuser()
    os.environ["HADOOP_SECURITY_AUTHENTICATION"] = "simple"
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    print(f"Using JAVA_HOME: {JAVA_HOME}")
    print(f"Using HADOOP_HOME: {HADOOP_HOME}")

    app_name = "GitHubAnalysis"
    # Configuration
    spark_builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.cleaner.referenceTracking.cleanCheckpoints", "true")
        .config("spark.local.dir", FOLDER_SPARK_TEMP)
    )

    spark = configure_spark_with_delta_pip(spark_builder).getOrCreate()

    print(f"SPARK_VERSION: {spark.version}")

    return spark
