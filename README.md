test-dashboard
==================
The Mozilla Mobile Test Dashboard is data aggregator that collects data from multiple input sources, caches and exposes it via a JSON API for consumption via re-dash.

* [STAGING Dashboard](https://sql.telemetry.mozilla.org/dashboard/tests-found-by-automation)
* PRODUCTION Dashboard

Note:
The test-dashboard is currently in a DRAFT state.


Backend
---------

**Aggregator**

A collection of python modules that collect data from the following input sources:

* Testrail
* Github
* Taskcluster
* Bitrise.io

**Database**

Data is aggregated / cached in a Cloud SQL database.



