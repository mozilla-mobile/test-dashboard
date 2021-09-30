test-dashboard
==================
The Mozilla Mobile Test Dashboard is data aggregator that collects data from multiple input sources and aggregates it in a Cloud SQL database for display in Looker graphs. 

Note:
The test-dashboard is currently in a DRAFT state.


Backend
---------

**Data Sources**

* Testrail
* Github - TBD
* Taskcluster - TBD
* Bitrise.io - TBD

**Database**

Data is aggregated / cached in a Cloud SQL database.  Data queries are constructed using BigQuery views.





