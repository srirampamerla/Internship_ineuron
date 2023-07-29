# Internship_ineuron
# Sentiment_Analysis_Project
The main objective of this project is to design a scalable pipeline using Spark to read customer reviews from the S3 bucket and store them into HDFS. The sentiment analysis conducted on the reviews offers a comprehensive understanding of customer perceptions, enabling the identification of specific areas that require enhancement. By pinpointing strengths and weaknesses, the company can focus its resources on improving critical aspects of its products and services, ultimately enhancing the overall customer experience. Scheduling the pipeline to run iteratively after each hour brings significant advantages. It enables the company to receive up-to-date and near real-time feedback on customer sentiments, facilitating a rapid response to emerging trends and issues. This proactive approach empowers the company to address customer concerns promptly, leading to improved customer satisfaction and loyalty.
# Architecture
The architecture of the proposed pipeline consists of three main components:
Data Source: The pipeline will read customer reviews data from an S3 bucket. This data will be in JSON format.
Processing Engine: Spark will be used to process the data, perform sentiment analysis using ML libraries, and store the output in HDFS.
Storage: The final output of the pipeline, which includes sentiment analysis results, will be stored in HDFS.


 ![image](https://github.com/srirampamerla/Internship_ineuron/assets/53964156/146df594-6b64-4960-8af7-1b93373b114b)

# Design Details
Data Source: The pipeline will read customer reviews data from an S3 bucket. This data will be in JSON format.
We will upload a file to s3 which is in csv format. By using Lambda functions we are changing the format from csv to json and saving the json file in different folder in same s3 bucket.
For every 1 hour lambda function will get triggered by event bridge.
## Processing Engine:
Once the data is uploaded to the S3 bucket, the pipeline will be triggered manually or automatically to read data from the S3 bucket and dump it into HDFS. We will use Spark to perform this operation.
The data will be processed using Spark, which is a fast and distributed processing engine for big data. We will use Spark’s Machine Learning Library (ML libraries) for performing sentiment analysis on the customer reviews.
To execute the pipeline, we will create a Spark job in Python. The job will be responsible for reading data from the S3 bucket, performing sentiment analysis using ML libraries, and storing the output in HDFS.
## Storage:
The final output of the pipeline, which includes sentiment analysis results, will be stored in HDFS. The output can be analysed further using other big data tools such as Apache Hive, Hue…
# Detailed Steps to implement
AWS S3:
1.Create a folder in the S3 bucket.
2.Upload the csv file.(sentiment-anal-intern26/data.csv)

## AWS Lambda:

Navigate to the AWS Management Console and search for "Lambda".
Click the "Create function" button to start creating a new Lambda function.
Select "Author from scratch" and enter a descriptive name for your function.
Choose "Python 3.8" as the runtime for your Lambda function.
Under "Permissions," create a new execution role with S3 full access policy, granting the function the necessary permissions to interact with S3.
Click the "Create function" button to create the Lambda function.
Now, you can write the Python code for your Lambda function. This code will read the CSV file from the specified S3 bucket, convert it into JSON format, and store it in the designated JSON location. Once you've written the code, click on the "Deploy" button to save your function.

To test the Lambda function, you can use the built-in test functionality provided by AWS Lambda. You can also check the execution logs in CloudWatch to monitor the function's performance and troubleshoot any issues that may arise during execution.

## EventBridge (formerly CloudWatch Events):
To create a scheduled job using AWS EventBridge, follow these steps:

Go to the AWS Management Console and navigate to "EventBridge."

Select "Create Rule" to create a new rule for scheduling events.

Under "Event Source," choose "Schedule" to configure a scheduled event.

Enter a name for your rule and choose the "Fixed rate of" option.

Set the rate to 1 hour to trigger the rule every hour.

Click "Add target" and choose "Lambda function" as the target.

Select your previously created Lambda function from the drop-down list.

Click "Configure details" to review and confirm your rule's settings.

Finally, click "Create rule" to create the scheduled job.

With this setup, your scheduled job will trigger the Lambda function at regular hourly intervals. The Lambda function will then process the CSV file from the specified S3 bucket and store the resulting JSON data in the designated JSON location.

You can monitor the scheduled job's execution and Lambda function's performance through the CloudWatch logs, gaining valuable insights into the pipeline's behavior and making any necessary adjustments for optimal performance.
Once created, Every 1 hour it will run automatically. If any new data is received it will update.
## AWS CLI
To install the AWS CLI and interact with S3 from within a Docker container, you can follow the steps below:

Install the AWS CLI in the Docker container:
In your Dockerfile, include the following lines to install the AWS CLI and any other dependencies needed to interact with S3:
Use the base image with Hadoop and PySpark installed

--FROM your-base-image

Install the AWS CLI and other necessary dependencies

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install awscli

Run the Docker container with AWS CLI and mount a volume:
After building the Docker image with the AWS CLI installed, you can run a container using that image and mount a volume to access files between the host machine and the container. The AWS CLI will be available within the container to interact with S3.

docker run -v /path/to/host/folder:/path/to/container/folder your-image aws configure

The aws configure command will prompt you to enter your AWS Access Key ID, Secret Access Key, and default region. This will set up the AWS CLI within the container to access your S3 bucket.

Download the file from S3 using the AWS CLI:
To download a file from S3, use the following command inside the container:
This command will download the file example.txt from the S3 bucket my-bucket to the specified location inside the container (/path/to/container/folder). The -v flag is used to mount the host folder to the container folder, so you can access the downloaded file outside the container.

Move the downloaded file to HDFS:
Now that you have downloaded the file to the host folder, you can use Hadoop commands to move the file from the host machine to HDFS. Assuming you want to move the file to the /input directory in HDFS, you can use the following command:

docker exec my-container hdfs dfs -put /path/to/host/folder/example.txt /input/

Replace my-container with the name of your running Docker container, and /path/to/host/folder/example.txt with the actual path to the downloaded file on the host machine. This command will put the file into the HDFS directory /input/ within the container.
## Spark:
In this step, we are using Spark Machine Learning with PySpark to perform sentiment analysis on customer reviews. The results of the sentiment analysis will be stored in Hadoop Distributed File System (HDFS) in a new directory.

First, make sure you have PySpark set up and configured to run Spark jobs in Python.

Next, let's assume you have performed the sentiment analysis and stored the results in a DataFrame called result.

Now, execute the following commands to store the results in HDFS:

docker exec my-container hdfs dfs -mkdir /output: This command creates a new directory named 'output' in HDFS. Replace 'my-container' with the actual name of your Docker container running HDFS.

result.write.mode("overwrite").format("csv").option("header", "true").save("/output/sentiment_results"): 

This line of code writes the DataFrame 'result' to the HDFS directory '/output/sentiment_results' in CSV format. The mode("overwrite") ensures that any existing data in the directory is overwritten if it already exists. The option("header", "true") specifies that the CSV file should include a header row with column names.

Once the code is executed, the results of the sentiment analysis will be stored in HDFS under the directory '/output/sentiment_results'. The data will be available in CSV format and can be further processed or queried as needed.



