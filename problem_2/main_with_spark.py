from pyspark.sql import SparkSession
from pyspark.sql.functions import sha2, col


def anonymize_data_with_spark(input_path, output_dir):
    spark = SparkSession.builder.appName("DataAnonymization").getOrCreate()
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    anonymized_df = (
        df.withColumn("first_name", sha2(col("first_name"), 256))
        .withColumn("last_name", sha2(col("last_name"), 256))
        .withColumn("address", sha2(col("address"), 256))
    )

    anonymized_df.write.csv(output_dir, header=True, mode="overwrite")
    spark.stop()

    print(f"Anonymized data saved to {output_dir}")


if __name__ == "__main__":
    anonymize_data_with_spark("sample_data.csv", "anonymized_data_spark_output")
