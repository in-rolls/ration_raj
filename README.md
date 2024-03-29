## Transaction Level Ration Card Data From Rajasthan (2021)

We scraped https://food.raj.nic.in/DistrictWiseCategoryDetails.aspx to get transaction level ration card data along with all the details about the beneficiary.

### Scripts

* [Scripts](scripts/)

### Data

The quantitative data are available to researchers with an approved IRB request at the Harvard Dataverse at: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/FIFZEX

The rural and urban files are separately stored. The data are nested with each layer stored in a separate file.

The Urban data is structured as follows:
State -> District -> Nagarpalika -> Ward -> FPS -> Ration Card -> Ration Card Data -> Ration Card Transactions

The Rural data is structured as follows:
State -> District -> Panchayat -> Village -> FPS -> Ration Card -> Ration Card Data -> Ration Card Transactions

If you wanted to see a sample image of a webpage for each step of the sequence, look at [img/](img/)

We have the photos of the beneficiaries also. But given the size, they are hosted on GCS. 

### Authors

Suriyan Laohaprapanon and Gaurav Sood
