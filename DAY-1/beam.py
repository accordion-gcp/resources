import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions

PROJECT_ID = "your-project-id"
REGION = "us-central1"
BUCKET_URI = "gs://your-bucket-name"   # reuse the bucket from the flex template notebook

options = PipelineOptions()
options.view_as(GoogleCloudOptions).project = PROJECT_ID
options.view_as(GoogleCloudOptions).region = REGION
options.view_as(GoogleCloudOptions).staging_location = f"{BUCKET_URI}/staging"
options.view_as(GoogleCloudOptions).temp_location = f"{BUCKET_URI}/temp"
options.view_as(StandardOptions).runner = "DataflowRunner"

with beam.Pipeline(options=options) as p:
    (
        p
        | beam.Create([1, 2, 3, 4, 5])
        | beam.Map(lambda x: x * 10)
        | beam.Filter(lambda x: x > 20)
        | beam.Map(lambda x: str(x))          # WriteToText needs strings
        | beam.io.WriteToText(f"{BUCKET_URI}/output/demo")
    )

print("Job submitted — check the Dataflow console for status.")