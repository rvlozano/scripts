# Migrate a List of Jobs with its associated Pipelines for Legacy SCH 3.x

from streamsets.sdk import ControlHub as ControlHub_lower
from streamsets.sdk import ControlHub as ControlHub_upper
sch_dev = ControlHub_lower('https://cloud.streamsets.com', username=<username>, password=<password>)
sch_prod = ControlHub_upper('https://cloud.streamsets.com', username=<username>, password=<password>)

# Step 1: make a list of jobs to export then export them from DEV.
dev_job=sch_dev.jobs.get(job_name='Job for richard_migrate_test')

dev_exported_jobs = []
dev_exported_jobs.append(dev_job) # Keep on appending as many jobs you'd like to the list.
dev_exported_jobs.append(sch_dev.jobs.get_all()[1]) # grab another random job throw in list.

# Add to dev_exported_jobs Local Archive.
pipeline_export_data = sch_dev.export_jobs(jobs=dev_exported_jobs)


# Write the exported jobs data to a local archive
jobs_export_file='/Users/rlozano/Downloads/dev_jobs_exports.zip'
with open (jobs_export_file, 'wb') as output_file:
    output_file.write(pipeline_export_data)

print(f'Exported {len(dev_exported_jobs)} Jobs')

# Step 2: make a list of associated pipelines(jobs) to export then export them from DEV.
dev_exported_piplines = []
for i in dev_exported_jobs:
    print(i.pipeline_name)
    dev_exported_piplines.append(
        sch_dev.pipelines.get(pipeline_id=i.pipeline_id)
    )

# Export the pipelines from Control Hub
pipeline_export_data = sch_dev.export_pipelines(pipelines=dev_exported_piplines)

# Write the exported pipeline data to a local archive
pipelines_export_file='/Users/rlozano/Downloads/dev_pipeline_exports.zip'
with open (pipelines_export_file, 'wb') as output_file:
    output_file.write(pipeline_export_data)

print(f'Exported {len(dev_exported_piplines)} associated pipelines')


# Step 3 : Import Dev associated Pipelines into Prod

with open(pipelines_export_file, 'rb') as input_file:
    pipelines_zip_data = input_file.read()
pipelines = sch_prod.import_pipelines_from_archive(archive=pipelines_zip_data,
                                              commit_message='Imported Pipelinees from Dev')

print(f'Imported {len(dev_exported_piplines)} associated pipelines')

# Step 4 : Import Dev jobs into Prod

with open(jobs_export_file, 'rb') as jobs_file:
    jobs = sch_prod.import_jobs(archive=jobs_file,pipeline=True)
