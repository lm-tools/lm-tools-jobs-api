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

* `count`: the max number of jobs to return from the Adzuna API.

## API endpoints

`/api/top_categories`: ordered list of categories per area.
`/api/jobadverts/`: List of all job adverts.

### Filtering and limiting

* Limit by adding `limit=n`.
* Filter by job centre by adding `job_centre_label=foo`.


## Recalculating travelling times

Sometimes it's useful to recalculate travelling times.  Do this by opening a django shell (`./manage.py shell`) and running:

```
from jobs.models import JobAdvert
[j.calculate_travelling_time(force=True) for j in JobAdvert.objects.all()]
```
