from pyspark.sql import functions as F
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.types import StringType, StructType, StructField, FloatType, IntegerType, ArrayType
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, collect_list
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.classification import LinearSVC
import re
import joblib

spark = SparkSession.builder \
    .appName("TwitterSentimentAnalysis") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

# Load the CountVectorizer model
vectorizer_model = joblib.load("count_vectorizer.joblib")

# Load the LinearSVC model
svc_model = joblib.load("svc_model.joblib")

# Define the Kafka source configuration
kafka_source_config = {
    "kafka.bootstrap.servers": "192.168.1.101:9092",
    "subscribe": "twitter01",
    "failOnDataLoss": "false"
}

# Define the Kafka schema
kafka_schema = StructType([
    StructField("url", StringType(), True),
    StructField("author", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("content", StringType(), True),
])

# Read data from Kafka
df = spark.readStream \
    .format("kafka") \
    .options(**kafka_source_config) \
    .load()

# Define functions for data cleaning and sentiment analysis
def clean_tweet(tweet):
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'bit.ly/\S+', '', tweet)
    tweet = tweet.strip('[link]')
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)
    my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@â'
    tweet = re.sub('[' + my_punctuation + ']+', ' ', tweet)
    tweet = re.sub('([0-9]+)', '', tweet)
    tweet = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)
    return tweet

def get_sentiment(tweet):
    try:
        vectorized_tweet = vectorizer_model.transform([tweet])
        prediction = svc_model.predict(vectorized_tweet)
        if prediction[0] == 1:
            return 'Positive'
        elif prediction[0] == 0:
            return 'Neutral'
        else:
            return 'Negative'
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 'Error'

# Define UDFs for data cleaning and sentiment analysis
clean_tweet_udf = F.udf(clean_tweet, StringType())
get_sentiment_udf = F.udf(get_sentiment, StringType())

# Parse the JSON data from Kafka
parsed_df = df.selectExpr("CAST(value AS STRING) as json") \
    .select(F.from_json("json", kafka_schema).alias("data")) \
    .select("data.*")

# Apply data cleaning and sentiment analysis
cleaned_df = parsed_df.withColumn("cleaned_content", clean_tweet_udf(col("content")))
sentiment_df = cleaned_df.withColumn("sentiment", get_sentiment_udf(col("cleaned_content")))

# Select relevant columns
result_df = sentiment_df.select("author", "timestamp", "sentiment")

# Define Elasticsearch sink configuration
es_sink_config = {
    "es.nodes": "0.0.0.0",
    "es.port": "9200",
    "es.index.auto.create": "true",
    "es.resource": "sentiments",
    "checkpointLocation": "checkpoints"  # Provide the path to a directory for checkpointing
    
}

# Write the data to Elasticsearch
query = result_df.writeStream \
    .outputMode("append") \
    .format("org.elasticsearch.spark.sql") \
    .options(**es_sink_config) \
    .start()

# Wait for the streaming query to terminate
query.awaitTermination()


##spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.elasticsearch:elasticsearch-spark-30_2.12:<your_elasticsearch_version> streamingPipeline.py
