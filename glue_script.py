
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load CSV from S3
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://your-bucket/raw/"]},
    format="csv",
    format_options={"withHeader": True}
)

# Clean and cast
transformed = datasource.resolveChoice(specs=[
    ("total_amount", "cast:double"),
    ("total_items", "cast:int")
]).drop_nulls(["total_amount"])

# Write to S3 as Parquet
glueContext.write_dynamic_frame.from_options(
    frame=transformed,
    connection_type="s3",
    connection_options={"path": "s3://your-bucket/processed/"},
    format="parquet"
)

job.commit()
