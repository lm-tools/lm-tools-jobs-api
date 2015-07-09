# Jobs API

Imports jobs from Adzuna and stores them in a model with an API on top.

## Setup 

This is a standard django setup.  You'll need to either export `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` or add them to `settings/local.py` before running:

* [optional virtualenv]
* `pip install -r requirements/local.txt`
*  `./manage.py runserver`.

## Importing data

The `jobs_import_from_adzuna` command imports jobs from Adzuna and takes the following arguments:

* `Job centre label`: text that will be stored against the job adverts imported.  This is only a convention.  The label is exposed in the API as typed, and filtering is allowed on this field.

* `location`: Three layers of comma separated place names, as the Adzuna API expects.  Use Adzuna's `jobs/{country}/geodata` endpoint to get these values.  For example, "UK,London,West London".

* `count`: the max number of jobs to return from the Adzuna API.

## API endpoints

`/api/top_categories`: ordered list of categories per area.
`/api/jobadverts/`: List of all job adverts.

### Filtering and limiting

* Limit by adding `limit=n`.
* Filter by job centre by adding `job_centre_label=foo`.