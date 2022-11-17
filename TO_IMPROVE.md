Here are describe things I believe should be improve in my solution.

1 - The `postcodes` API is not accepting a high number of coordinates to get the list of Postcode by coordinate, so the input
CSV file should be break in smaller parts and the command to get the outcodes should get the informations part by part
instead of using the entire CSV file.

2 - The Dockerfile can be optmized, for example, different stages could be build to install and configure the rest of the application.

3 - Should exist more tests to cover the command that gets the outcode information.

4 - The command could be places in a cronjob to run periodically.
