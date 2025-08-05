# GitHub Data Scraper and Analyzer

## Overview

This project scrapes GitHub issues and comments, then performs Spark analysis on the collected data. The system provides a menu-driven interface for easy operation.

## Output Reports

- **Scraping Report**: [Detailed statistics and logs](document/de_expsc_assessment_scrape_result.md) from the GitHub data collection process
- **Analysis Report**: [Comprehensive results](document/de_expsc_assessment_spark_result.md) of the Spark data analysis
- **GitHub Issues Data**: [Detailed data and schema](document/de_expsc_assessment_scrape_data_issues.md) of the scraped GitHub issues
- **GitHub Comments Data**: [Detailed data and schema](document/de_expsc_assessment_scrape_data_comments.md) of the scraped GitHub comments
- **SQL Script**: Implementation of [`average_resolution_by_month.sql`](https://github.com/makenaichu970413/exp-science-de-assessment/blob/main/sql/average_resolution_by_month.sql) used in Spark analysis

## Features

- **GitHub Data Scraping**: Automated collection of issues and comments with retry mechanism
- **Data Validation**: Robust validation using `Pydantic` models to ensure data quality
- **Spark Data Analysis**: Advanced processing of GitHub data including nested structure handling
- **Menu-Driven Interface**: User-friendly console interface for easy operation
- **Data Persistence**: Flexible storage options (CSV, JSON, SQLite)
- **Workflow Visualization**: Mermaid diagrams documenting data flows
- **Error Handling**: Comprehensive logging and status tracking
- **Reporting**: Automated report generation for scraping and analysis results

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The project requires a `.env` file in the root directory with the following environment variables. Customize these values according to your specific setup:

```env
# GitHub CCC personal access token
GITHUB_TOKEN=your_github_token_here

# Java and Hadoop paths (Windows example)
JAVA_HOME="C:\\Program Files\\Java\\jdk-17"
HADOOP_HOME="C:\\Program Files\\Hadoop\\hadoop-3.3.6"
```

**Important Security Note**:

- Replace `your_github_token_here` with a valid [GitHub personal access token](https://github.com/settings/tokens)
- The token needs `repo` scope access to read repository issues

**Version Compatibility**:

- PySpark 4.0
- Hadoop 3.3.6
- Java 17+

## Usage

Run the application:

```bash
python -B main.py
```

### Menu Options

1. **Scrape GitHub Issues & Comments Data**: Collects issue and comment data from GitHub repositories
2. **Spark Analysis**: Performs data analysis on collected GitHub data using PySpark
3. **Exit**: Quits the application

### Folder Structure

- **[`input/`](input/)**: Contains the `github_urls.xlsx` file which stores GitHub repository URLs. The web scraping process automatically extracts URLs from this file at startup.
- **[`temp/`](temp/)**: Stores intermediate scraped data (issues and comments) as JSON files from each API request. Used to resume scraping if the process is interrupted.
- **[`log/`](log/)**: Contains database log files tracking the status (PENDING, PROCESS, FAILED, COMPLETE) of each API request during scraping.
- **[`output/`](output/)**: Holds the final exported CSV files after successful completion of the scraping process.

### GitHub API Endpoints Used

The following GitHub API endpoints are used for data scraping:

- **Repository Issues**:

  - Method: `GET`
  - Path: `/repos/{owner}/{repo}/issues`
  - Parameters: `state=all`, `per_page=100`, `page={page_number}`
  - Example: `https://api.github.com/repos/Uniswap/v3-core/issues?state=all&per_page=100&page=1`

- **Repository Issue Comments**:
  - Method: `GET`
  - Path: `/repos/{owner}/{repo}/issues/{issue_number}/comments`
  - Example: `https://api.github.com/repos/Uniswap/v3-core/issues/1049/comments`

## Scrape Data

![Data Scraping Workflow](document/de_expsc_assessment_scrape_flow.png)

The scraping process involves:

1. **Initialization**:

   - Check database initialization status
   - Exit scraping if database not initialized
   - Read repository URLs from Excel file
   - Insert new URLs to database with status: PENDING (skip existing)

2. **Repository Processing**:

   - Each repository marked as PROCESS before scraping
   - Loop continues until all repositories are processed

3. **Issue Scraping**:

   - Checks temporary storage for existing page data
   - Calls GitHub API with retry logic (max 3 attempts)
   - Saves raw data to temporary storage
   - Exports clean data to CSV

4. **Comment Scraping**:

   - Filters issues with comments
   - Scrapes comments only for `PENDING`/`PROCESS`/`FAILED` issues
   - Similar retry logic and temp storage as issue scraping

5. **Status Tracking & Reporting**:
   - Repository status updated to `COMPLETE` after success
   - Detailed error logging for failed scrapes
   - [Final report generated with statistics](document/de_expsc_assessment_scrape_result.md)

## Spark Analysis

![Data Analysis Workflow](document/de_expsc_assessment_spark_flow.png)

The Spark analysis process involves:

1. **Data Ingestion**:

   - Raw CSV files loaded into Spark DataFrames
   - Schema validation applied during ingestion

2. **Schema Application**:

   - Predefined schemas from `SparkSchema.py` structure the data
   - Complex nested structures (users, reactions, milestones) are properly typed

3. **Data Processing**:

   - **GitHub Issues**: Processed in `SparkIssue.py`
     - Nested structures (assignees, labels) flattened
     - Milestone data extracted
   - **GitHub Comments**: Processed in `SparkComment.py`
     - User information enriched
     - Reaction metrics calculated

4. **Analysis Operations**:

   - Coordinated by `Spark.py`
   - Joins issue and comment datasets
   - Performs aggregations (comment counts, reaction metrics)
   - Generates repository health metrics

5. **Result Output**:
   - [Summary of statistical results and visualizations generated](document/de_expsc_assessment_spark_result.md)
