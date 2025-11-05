"""
Sample Spark Pipeline for DataSherpa Documentation Demo
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, when

def create_spark_session():
    """Create and configure Spark session"""
    return SparkSession.builder \
        .appName("SampleDataPipeline") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()

def read_data(spark, input_path):
    """Read data from parquet files"""
    return spark.read.parquet(input_path)

def transform_data(df):
    """Apply transformations to the data"""
    # Filter invalid records
    df_clean = df.filter(col("value").isNotNull())
    
    # Add derived columns
    df_transformed = df_clean.withColumn(
        "category",
        when(col("value") > 100, "high")
        .when(col("value") > 50, "medium")
        .otherwise("low")
    )
    
    # Aggregate data
    df_agg = df_transformed.groupBy("category") \
        .agg(
            count("*").alias("count"),
            avg("value").alias("avg_value")
        )
    
    return df_agg

def write_data(df, output_path):
    """Write results to parquet"""
    df.write.mode("overwrite").parquet(output_path)

def main():
    """Main pipeline execution"""
    spark = create_spark_session()
    
    # Read
    df = read_data(spark, "s3://bucket/input/")
    
    # Transform
    df_result = transform_data(df)
    
    # Write
    write_data(df_result, "s3://bucket/output/")
    
    spark.stop()

if __name__ == "__main__":
    main()
