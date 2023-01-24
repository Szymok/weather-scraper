In this repository we scrape data from the open data sources: severeweather.wmo.int - aggregator of current weather warnings across the globe, and iccs-ccs.org - aggregator of piracy warnings across the globe. We use googleapis to obtain latitude and longitude coordinates of warning locations from text.

We scrape every 30 minutes using GitHub actions.