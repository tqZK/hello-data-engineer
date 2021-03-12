# hello-data-engineer
Recruitement homework - solved!

Script to parse clicstream logs file and generate output CSV file.
Output file will provide information with `user_id` and if given user visited the same wiki (`is_same_wiki`) and article 
(`is_same_article`) in the first and last event that was logged in input log file.

## How to run

Script was tested on Python 3.6.9.

To create virtualenv in the current directory and install packeges required for script to work:
```shell
make venv
```

To run script (using virtualenv above):
```shell
make run input_path=<<INPUT_PATH>> output_path=<<OUTPUT_PATH>>
```
where `<<INPUT_PATH>>` is path to clicstream logs file (required; format: each log in new line) 
and `<<OUTPUT_PATH>>` is path to output file (optional, default value is `output.csv`).

If you are in prepared virtualenv you can also run script directly:
```shell
python3 parse_clickstream_logs.py --input_path=<<INPUT_PATH>> --output_path=<<OUTPUT_PATH>>
```
with arguments as defined above.

## How to develop

To create developent virtualenv in the current directory and install development packeges:
```shell
make venv-dev
```

To run unit tests:
```shell
make test
```

## About the solution

As the task of parsing the log file is quite simple and there is a requirement to **make it work with different inputs 
and scheduling**, I decided to create a simple one-file script with input arguments. 
This way, given prepared environment, we could run it with different inputs and outputs.

Despite that the solution could be done in pure Python, I decided to use Pandas library because provides **easier and
quicker data analysis and processing** using `.groupby()` and `.aggregate()`. I decided not to use PySpark as it is 
a small task and with size of test data that I've been provided it would be too big tool to use. However, because code
uses Pandas we are able to quickly migrate it to PySpark, if needed.

To ensure **easy maintananace and furter developemnt** of the solution:
- I created `Makefile` with decription how to use it in `README.md` to enable easy deployment and testing 
  of the solution, including splitting production and development requirements to seperate files
- I created simple unit tests that improve redeability and show all steps of the solution - next person who will be 
  working on the project could start with looking at these to understand how it works. I copied one
  of the example logs I've been provided and modified it in a way that will
- I followed PEP8 to write clean code
- I added docstrings and decriptive comments (in places where pandas usage knowledge is needed)

**If I could dedicate more time** to the solution, I would write more unit test - for now we are testing only happy path
and simple examples. I would also add additional validation of data and checking if input and output paths/directories 
exist.

To make it even **more production-ready**, I would add versioning (e.g. semantic versioning) with changelog - this way
we could omit problems with other product components not being compatible with a new version of the script. 
Also, probably naming the script in more easy to remember way (or more matching to other components of the product)
would be good for maintaining clear communication in possible further development.

Also, I've encoutered that **sometimes the `article_id` is not provided in the URL**. I presume that these are the cases
when user tried to load a page that doesn't exist and was redirected to wiki's 404 page or was just browsing
the wiki without enering any of the articles. In these cases my solution returns `is_same_article=False` as the user
was not browsing any article. This could be easily changed in function `is_same_wiki_and_article()`.
