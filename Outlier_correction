# Load necessary libraries
library(flowCore)
library(flowAI)
library(dplyr)
library(magrittr)
library(FlowSOM)

# Define the file path
fcsfile = " "

# Read in the FCS file
fcs_data = read.FCS(fcsfile)


# Returns data corrected for outliers

outlier_correction = function(fcsfile) {
    resQC <- flow_auto_qc(fcsfile)
    resQC_df = resQC@exprs
    return(as.data.frame(resQC_df))
}

# Apply the outlier detection function
outlier_corrected_data = outlier_correction(fcsfile)

# Plot a boxplot to compare a channel before and after preprocessing
boxplot_compare = function(column_name) {
    # Ensure the column exists in the data
    if (!(column_name %in% colnames(fcs_data@exprs))) {
        stop(paste("Column", column_name, "not found in the FCS data"))
    }
    
    # Extract the original and outlier detection columns
    col_df_original = fcs_data@exprs[, column_name]
    col_df_outlier = outlier_corrected_data[, column_name]
    
    # Plot boxplots
    par(mfrow = c(1, 2))  # Set up a 1x2 plotting area
    boxplot(col_df_original, main = paste("Original Data:", column_name), ylab = "Intensity", xlab = "Original Data")
    boxplot(col_df_outlier, main = paste("Processed Data:", column_name), ylab = "Intensity", xlab = "Processed Data")
}

# Example usage: Plotting boxplots for the "FSC-A" channel
#boxplot_compare("FSC-A")


# Density Plot of a marker; original vs outlier corrected data
densityplot_compare = function(column_name) {
  # Calculate density estimates
  density1 <- density(outlier_corrected_data[, column_name])
  density2 <- density(fcs_data@exprs[, column_name])
  
  # Create data frames for densities
  density_df1 <- data.frame(x = density1$x, y = density1$y, group = "Original Data")
  density_df2 <- data.frame(x = density2$x, y = density2$y, group = "Outlier Processed Data")
  
  # Identify differences
  density_diff <- merge(density_df1, density_df2, by = "x", suffixes = c("_1", "_2"))
  density_diff <- density_diff %>%
    mutate(difference = ifelse(y_1 > y_2, "Unique to Dist 1", "Unique to Dist 2"))
  
  # Plot the distributions with conditional coloring
  ggplot() +
    geom_line(data = density_df1, aes(x = x, y = y, color = group)) +
    geom_line(data = density_df2, aes(x = x, y = y, color = group)) +
    geom_ribbon(data = density_diff, aes(x = x, ymin = 0, ymax = y_1, fill = difference), alpha = 0.3) +
    scale_fill_manual(values = c("Unique to Dist 1" = "red", "Unique to Dist 2" = "blue")) +
    labs(title = "Density Plots with Highlighted Differences",
         x = "Value",
         y = "Density",
         color = "Distribution",
         fill = "Difference") +
    theme_minimal()
}

# sample usage
#densityplot_compare("FSC-H")



