# Spark
from spark.GitHub import SparkInit, SparkIssue, SparkComment


def run():

    # ? CSV Output File
    csv_issue_file = f"github_issues_Uniswap_v3-core.csv"
    csv_comment_file = "github_issues_comments_Uniswap_v3-core.csv"

    # ? Initiate SparkSession
    spark = SparkInit.init()

    # ? Create Issue & Comment DataFrame
    df_issue = SparkIssue.create_dataframe(spark, csv_issue_file)
    df_comment = SparkComment.create_dataframe(spark, csv_comment_file)

    # ? Analysis
    SparkComment.analysis_top_10_commenters(df_comment)

    SparkIssue.analysis_average_resolution(df_issue)

    SparkIssue.sql_analysis_average_resolution(spark, df_issue)

    df_issue_res = SparkIssue.analysis_creation_trend(df_issue)
    # ? Visualize the monthly issue createion trend
    title = f'Monthly Issue Creation Trend of "{csv_issue_file}"'
    SparkIssue.visualize_creation_trend(df_issue_res, title)

    # ? Terminate Spark After run completely
    spark.stop()
