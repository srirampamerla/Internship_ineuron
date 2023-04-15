#Step 1: Importing Required Libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, FloatType, StringType, StructType, StructField
from pyspark.ml.feature import hash_trafo, id_fit, Tokenizer
from pyspark.ml.classification import NaiveBayes
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#Step 2: Create SparkSession
spark = SparkSession.builder.appName("SentimentANA").getOrCreate()

#Step 3: Read JSON data from HDFS location
df_old = spark.read.json("hdfs://localhost:8080/sentiment/datajson.json")
df_old.printSchema()

#Step 4: Converting Data Types
df = df_old.withColumn("helpful_no", df_old["helpful_no"].cast(IntegerType()))
df = df_old.withColumn("day_diff", df_old["day_diff"].cast(IntegerType()))
df = df_old.withColumn("helpful_yes", df_old["helpful_yes"].cast(IntegerType()))
df = df_old.withColumn("overall", df_old["overall"].cast(IntegerType()))
df = df_old.withColumn("score_average_rating", df_old["score_average_rating"].cast(IntegerType()))
df = df_old.withColumn("score_pos_neg_diff", df_old["score_pos_neg_diff"].cast(IntegerType()))
df = df_old.withColumn("total_vote", df_old["total_vote"].cast(IntegerType()))
df = df_old.withColumn("wilson_lower_bound", df_old["wilson_lower_bound"].cast(IntegerType()))

df.printSchema()

#Step 5: Sort data by any value in descending order/ascending order
df = df.sort('wilson_lower_bound', ascending=False)

#Step 6: write the function to handle and perform missing value analysis
def miss_value_analy(df):
    no_col = [col for col in df.columns if df[col].isNull().sum() > 0]
    no_missing = df.select([count(col).alias(col) for col in no_col]).collect()[0]
    ratio_ = [(no_missing[i] / df.count())*100 for i in range(len(no_col))]
    missing_df = spark.createDataFrame(zip(no_col, no_missing, ratio_), 
                                       schema=['Column Name', 'Missing Values', 'Ratio (%)'])
    return missing_df

#Step 7: Function to check dataframe characteristics
def check_dataframe(df, head=5, tail=5):
    print("SHAPE".center(82,'~'))
    print("ROWS:{}".format(df.count()))
    print('COLUMNS:{}'.format(len(df.columns)))
    print('TYPES'.center(82,'~'))
    df.printSchema()
    print("".center(82,'~'))
    print(miss_value_analy(df).show())
    print('DUPLICATED VALUES'.center(83,'~'))
    print(df.dropDuplicates().count())
    print("QUANTILES".center(82,'~'))
    df.select([col for col in df.columns if df.schema[col].dataType in 
               [IntegerType(), FloatType()]]).summary("0%", "5%", "50%", "95%", "99%", "100%").show()


# Step 8:Define UDFs for sentiment analysis
def textblobsentiment(sentence):
    blob = TextBlob(sentence)
    return blob.sentiment.polarity

def vaderSentiment(sentence):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(sentence)
    return scores['compound']

#Step 9: Create UDFs
text_blob_udf = udf(textblobsentiment, FloatType())
vader_sent_udf = udf(vaderSentiment, FloatType())

#Step 10: Add columns for sentiment analysis using UDFs
df = df.withColumn("Text_blob_sentiment", text_blob_udf(df["reviewText"]))
df = df.withColumn("Vader_sentiment", vader_sent_udf(df["reviewText"]))

#Step 11: Create tokenizer and hashing TF objects
tokenizer = Tokenizer(inputCol="reviewText", outputCol="words")
hash_trafo = hash_trafo(inputCol=tokenizer.getOutputCol(), outputCol="features")

#Step 12: Fit the tokenizer and hashing TF objects to the data
worddata = tokenizer.transform(df)
trsfodata = hash_trafo.transform(worddata)

#Step 13: Create id_fit object and fit to the data
id_fit = id_fit(inputCol=hash_trafo.getOutputCol(), outputCol="tf_id_fit")
id_model = id_fit.fit(trsfodata)
tf_data = id_model.transform(trsfodata)

#Step 14: Split data into training and test sets
(trainingData, testData) = tf_data.randomSplit([0.7, 0.3], seed=100)

#Step 15: Train Naive Bayes model on training data
NB_Model = NaiveBayes(smoothing=1)
model = NB_Model.fit(trainingData)

#Step 16: Make predicted on test data
predicted = model.transform(testData)

#Step 17: Select necessary columns and rename for output
out = predicted.select("reviewText", "textblob_sentiment", "vader_sentiment", "prediction") \
    .withColumnRenamed("prediction", "naivebayes_predicted")

#Step 18: Write output to HDFS
out.write.json("hdfs://localhost:8080/sentiment/finaloutputfrompyspark.json")
