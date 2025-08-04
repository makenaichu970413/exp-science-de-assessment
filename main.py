# Scraper
from scraper.GitHub import Scrape as GitHubScrape

# Spark
from spark.GitHub import Spark as GitHubSpark

# Utils
from utils.function.FuncFile import export_csv_comments, export_csv_issues


# Run with `-B`` flag to prevent "__pycache__/"
# python -B main.py


def github():

    while True:
        print("\nMenu:")
        print("[1] Scrape GitHub Issues & Comments Data")
        print("[2] Spark Analysis of GitHub Issues & Comments Data")
        print("[3] Exit")
        choice = input("Enter your choice (1-3): ").strip()

        print(f"\n\n")
        if choice == "1":
            GitHubScrape.run()

        elif choice == "2":
            GitHubSpark.run()

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":

    # name = "Uniswap_v3-core"
    # export_csv_issues(name)
    # export_csv_comments(name)

    github()
