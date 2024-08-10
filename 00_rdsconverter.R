library(readr)
library(here)

# Check if the file exists
file_path <- here("tweets.rds")
if (!file.exists(file_path)) {
  stop("File does not exist:", file_path)
}

data <- readRDS(file_path)

# Write the data to a CSV file
write_csv(data, here("tweets.csv"))

