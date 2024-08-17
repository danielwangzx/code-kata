# Data Anonymization Project

This project includes scripts for anonymizing sensitive fields (`first_name`, `last_name`, `address`) in a large CSV file using two methods: with Spark and without Spark.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- PySpark (for Spark-based anonymization)

## Installation

To install PySpark and other required dependencies, run:

```bash
pip install pyspark faker
```

## Generating a CSV File

To generate a CSV file of a specific size (in MB) for testing, use:

```bash
python generate_data.py --size 20
```

This command generates a CSV file of approximately 20MB (20MB). You can adjust the `--size` parameter to generate a file of a different size. for instance 2000 for 2GB

## Anonymization

### Without Spark

To anonymize the data using Python's multiprocessing, run:

```bash
python main.py
```

### With Spark

To anonymize the data using PySpark, run:

```bash
python main_with_spark.py
```

## Testing

To run tests, use the following command:

```bash
python -m unittest discover -s test
```

The tests will verify that both the Spark and non-Spark anonymization methods work correctly.
