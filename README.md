# TheCountrynomics
Please click the link to access the final production: http://www.thecountrynomics.com/

The Countrynomics is a website providing analytics of economic indicators for G20 countries. The economic indicators are queried from international organizations such as IMF, OECD, and World Trade Organization.

[API Query from DBnomics and Quandl](https://github.com/sh2nam/TheCountrynomics/blob/master/mysite/applications/derivatives/project_code/Downlaod_Dbnomics_API_Data.py):
This class allows users to input country name, indicator name, start date, and end date to query economic indicator through an API call from [DBnomics](https://db.nomics.world/) or [Quandl](https://www.quandl.com/). For the names of countries and indicators refer to the below config files.





[Config - Countries](https://github.com/sh2nam/TheCountrynomics/blob/master/mysite/applications/derivatives/project_code/config_country.yaml): This config file stores list of available countries and country codes. 

[Config - Indicators](https://github.com/sh2nam/TheCountrynomics/blob/master/mysite/applications/derivatives/project_code/config_indicator.yaml): This config file stores list of indicator names and indicator codes.
