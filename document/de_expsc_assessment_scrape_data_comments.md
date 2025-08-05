### 🚀 GitHub Issues Comments: 600 Records Processed in Spark

Spark successfully loaded **600** issue records from:
`/exp-science-de-assessment/output/github_issues_comments_Uniswap_v3-core.csv`

```shell
+-----+---------+--------------------+--------------------+-------------------+
|index|  user_id|                 url|                body|       created_date|
+-----+---------+--------------------+--------------------+-------------------+
|    0| 95510084|https://api.githu...|**Review the foll...|2025-07-20 21:14:24|
|    1| 95510084|https://api.githu...|> [!WARNING]\n> *...|2025-07-20 21:14:26|
|    2| 95510084|https://api.githu...|**Review the foll...|2025-06-15 23:43:07|
|    3| 26384082|https://api.githu...|Is this still rel...|2025-06-01 18:43:36|
|    4| 95510084|https://api.githu...|**New, updated, a...|2025-03-31 23:15:56|
|    5| 95510084|https://api.githu...|**🚨 Potential se...|2025-03-31 23:15:58|
|    6| 26384082|https://api.githu...|Is this still rel...|2025-05-31 00:06:01|
|    7| 95510084|https://api.githu...|**🚨 Potential se...|2025-03-07 21:23:36|
|    8| 95510084|https://api.githu...|<!-- overview-com...|2025-03-08 18:40:40|
|    9| 26384082|https://api.githu...|Is this still rel...|2025-06-15 15:59:49|
|   10| 26384082|https://api.githu...|Is this still rel...|2025-04-16 01:52:31|
|   11| 62060278|https://api.githu...|yes, it is releva...|2025-04-16 03:53:36|
|   12| 26384082|https://api.githu...|Is this still rel...|2025-06-15 04:08:18|
|   13| 26384082|https://api.githu...|Is this still rel...|2025-04-05 23:46:33|
|   14|125138460|https://api.githu...|hello, there is n...|2025-03-22 18:49:11|
|   15| 34962750|https://api.githu...|Theres a branch c...|2025-01-14 21:16:04|
|   16| 26384082|https://api.githu...|Is this still rel...|2025-03-14 19:39:39|
|   17| 26384082|https://api.githu...|Is this still rel...|2025-02-19 05:16:34|
|   18| 26384082|https://api.githu...|Is this still rel...|2025-02-15 11:50:18|
|   19| 26384082|https://api.githu...|Is this still rel...|2025-02-15 11:50:16|
+-----+---------+--------------------+--------------------+-------------------+
only showing top 20 rows
```

### 📜 DataFrame Schema: GitHub Issues Comments in Spark

```shell
root
 |-- url: string (nullable = true)
 |-- html_url: string (nullable = true)
 |-- issue_url: string (nullable = true)
 |-- id: integer (nullable = true)
 |-- node_id: string (nullable = true)
 |-- user: struct (nullable = true)
 |    |-- login: string (nullable = true)
 |    |-- id: integer (nullable = true)
 |    |-- node_id: string (nullable = true)
 |    |-- avatar_url: string (nullable = true)
 |    |-- gravatar_id: string (nullable = true)
 |    |-- url: string (nullable = true)
 |    |-- html_url: string (nullable = true)
 |    |-- followers_url: string (nullable = true)
 |    |-- following_url: string (nullable = true)
 |    |-- gists_url: string (nullable = true)
 |    |-- starred_url: string (nullable = true)
 |    |-- subscriptions_url: string (nullable = true)
 |    |-- organizations_url: string (nullable = true)
 |    |-- repos_url: string (nullable = true)
 |    |-- events_url: string (nullable = true)
 |    |-- received_events_url: string (nullable = true)
 |    |-- type: string (nullable = true)
 |    |-- site_admin: boolean (nullable = true)
 |    |-- user_view_type: string (nullable = true)
 |-- created_at: timestamp (nullable = true)
 |-- updated_at: timestamp (nullable = true)
 |-- author_association: string (nullable = true)
 |-- body: string (nullable = true)
 |-- reactions: struct (nullable = true)
 |    |-- url: string (nullable = true)
 |    |-- total_count: integer (nullable = true)
 |    |-- plus1: integer (nullable = true)
 |    |-- minus1: integer (nullable = true)
 |    |-- laugh: integer (nullable = true)
 |    |-- hooray: integer (nullable = true)
 |    |-- confused: integer (nullable = true)
 |    |-- heart: integer (nullable = true)
 |    |-- rocket: integer (nullable = true)
 |    |-- eyes: integer (nullable = true)
 |-- performed_via_github_app: struct (nullable = true)
 |    |-- id: integer (nullable = true)
 |    |-- client_id: string (nullable = true)
 |    |-- slug: string (nullable = true)
 |    |-- node_id: string (nullable = true)
 |    |-- owner: struct (nullable = true)
 |    |    |-- login: string (nullable = true)
 |    |    |-- id: integer (nullable = true)
 |    |    |-- node_id: string (nullable = true)
 |    |    |-- avatar_url: string (nullable = true)
 |    |    |-- gravatar_id: string (nullable = true)
 |    |    |-- url: string (nullable = true)
 |    |    |-- html_url: string (nullable = true)
 |    |    |-- followers_url: string (nullable = true)
 |    |    |-- following_url: string (nullable = true)
 |    |    |-- gists_url: string (nullable = true)
 |    |    |-- starred_url: string (nullable = true)
 |    |    |-- subscriptions_url: string (nullable = true)
 |    |    |-- organizations_url: string (nullable = true)
 |    |    |-- repos_url: string (nullable = true)
 |    |    |-- events_url: string (nullable = true)
 |    |    |-- received_events_url: string (nullable = true)
 |    |    |-- type: string (nullable = true)
 |    |    |-- site_admin: boolean (nullable = true)
 |    |    |-- user_view_type: string (nullable = true)
 |    |-- name: string (nullable = true)
 |    |-- description: string (nullable = true)
 |    |-- external_url: string (nullable = true)
 |    |-- html_url: string (nullable = true)
 |    |-- created_at: string (nullable = true)
 |    |-- updated_at: string (nullable = true)
 |    |-- permissions: map (nullable = true)
 |    |    |-- key: string
 |    |    |-- value: string (valueContainsNull = true)
 |    |-- events: array (nullable = true)
 |    |    |-- element: string (containsNull = true)

```
