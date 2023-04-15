# Sentiment_Analysis_Project

The use case is for a company that receives a large volume of customer reviews on a regular basis. The company may want to analyze the sentiment of the reviews to gain insights into customer satisfaction and identify areas for improvement. By using a scalable pipeline with Spark to read and store the reviews in HDFS, the company can efficiently process and analyze the data. Additionally, scheduling the pipeline to run iteratively after each hour ensures that the analysis is up-to-date and can provide real-time feedback on customer satisfaction.


# Tech Stack used

1.AWS Lambda 

2.AWS S3

3.Hadoop

4.Spark

5.Docker

# Architecture
![image](https://user-images.githubusercontent.com/58679637/222682521-771e4588-a4cf-496d-a8ee-8ebacd3fa423.png)


# Architecture explanation

1.AWS Lambda will be triggered by an S3 Event Notification configured on the s3 buckett. The Lambda function will read the CSV file, transformed it to JSON format, and store the resulting file in the same bucket with specified name.

2.The data will be stored in the S3 bucket

3.To extract data from an S3 bucket and store it in HDFS, we can use the Hadoop container with the AWS CLI credentials configured and the S3. connector installed to mount the S3 bucket as an HDFS directory. Then, we can copy the JSON file from the S3 bucket to HDFS using the hadoop fs -cp command.

4.Once we have loaded the data into a Spark DataFrame from hdfs, we can use PySpark's MLlib library to perform the sentiment analysis. 

5.Finally, we can save the resulting image to HDFS using the write method of the DataFrameWriter


# Detailed Procedure

1.
AWS Lambda will be triggered by an S3 Event Notification configured on the S3 bucket. The Lambda function will read the CSV file, transform it to JSON format, and store the resulting file in the S3bucket. 

AWS Lambda code is (csv_to_json_AWS.py)

2.
The data will be stored in the S3 bucket. data.csv and datajson.json is attached

In json, all the columns will be string. convert the required columns into integer while running sentiment_analysis_pyspark.py

3.
Run the docker compose:(If yhere is no docker image locally, it will download and runs the docker)
docker compose -f docker-compose.yaml up -d
4.
In the docker run command we have also AWS credentials as we need to download the json file from S3 Bucket.

After running docker, run the below coommand to install s3a connctor
hadoop fs -copyToLocal s3://<your-bucket-name>/jars/hadoop-aws-<your-hadoop-version>.jar /usr/local/hadoop/share/hadoop/common/lib/

5.
Now we will check whether our s3a connecor is working or not 
 
hadoop fs -mkdir /mnt/s3
hadoop fs -D fs.s3a.access.key=<your_access_key> -D fs.s3a.secret.key=<your_secret_key> -D fs.s3a.endpoint=<your_s3_endpoint> -D fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -ls s3://<your-bucket-name>/
hadoop fs -D fs.s3a.access.key=<your_access_key> -D fs.s3a.secret.key=<your_secret_key> -D fs.s3a.endpoint=<your_s3_endpoint> -D fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -mount /mnt/s3 s3://<your-bucket-name>/

6.
 After successfully connecting s3a with hadoop, lets copy the json file into hdfs location
 hadoop fs -cp s3://my-bucket/data/datajson.json /sentiment/

7.
 Now run the spark ml code(sentiment_analysis_pyspark.py) on pyspark terminal. I have also used libraries like pandas and NLP on amazon.csv dataset for practise.
8.
 Store the final result in new hdfs location 
 out.write.json("hdfs://localhost:8080/sentiment/finaloutputfrompyspark.json")
 
