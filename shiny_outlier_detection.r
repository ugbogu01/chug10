library(shiny)
library(flowCore) 
library(flowAI)  
library(ggplot2)
library(dplyr)

# set directory
setwd("~")

# Load A flowframe
fcsfile = ""

# Read in the FCS file
fcs_data = read.FCS(fcsfile)

rawdata = exprs(fcs_data)

# Define the outlier detection function
outlier_detection = function(fcsfile) {
  resQC = flow_auto_qc(fcsfile)
  resQC_df = resQC@exprs
  return(as.data.frame(resQC_df))
}

markernames = colnames(fcs_data)

# Apply the outlier detection function
outlier_data = outlier_detection(fcsfile)

# Construct the correct path to the "resultsQC" directory
current_working_directory = getwd()  # Assuming current working directory is defined
resultsQC_path = file.path(current_working_directory, "resultsQC")

# Set the working directory to "resultsQC"
setwd(resultsQC_path)

# Construct path to QCmini.txt
miniQC_path = file.path(resultsQC_path, "QCmini.txt")

# Read the QCmini.txt to readable format
miniQCdata = read.delim(miniQC_path, header = TRUE, sep = "\t")
#print(miniQCdata)

# Plot a boxplot to compare a channel before and after preprocessing
boxplot_preprocessing = function(marker) {
  # Ensure the column exists in the data
  if (!(marker %in% colnames(fcs_data@exprs))) {
    stop(paste("Column", marker, "not found in the FCS data"))
  }
  
  # Extract the original and outlier detection columns
  col_df_original = fcs_data@exprs[, marker]
  col_df_outlier = outlier_data[, marker]
  
  # Plot boxplots
  par(mfrow = c(1, 2))  # Set up a 1x2 plotting area
  boxplot(col_df_original, main = paste("Original:", marker), ylab = "Intensity", xlab = "Original Data")
  boxplot(col_df_outlier, main = paste("Outlier Detected:", marker), ylab = "Intensity", xlab = "Processed Data")
}

# Density Plot of a marker; original vs outlier corrected data
densityplot_compare = function(marker) {
  # Ensure the column exists in the data
  if (!(marker %in% colnames(fcs_data@exprs))) {
    stop(paste("Column", marker, "not found in the FCS data"))
  }
  
  # Calculate density estimates
  density1 = density(outlier_data[, marker])
  density2 = density(fcs_data@exprs[, marker])
  
  # Create data frames for densities
  density_df1 = data.frame(x = density1$x, y = density1$y, group = "Outlier")
  density_df2 = data.frame(x = density2$x, y = density2$y, group = "Processed Data")
  
  # Identify differences
  density_diff = merge(density_df1, density_df2, by = "x", suffixes = c("_1", "_2"))
  density_diff = density_diff %>%
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
# Custom summary function
custom_summary_combined = function(outlier_data, rawdata, marker) {
  summary_outlier = summary(outlier_data[, marker])
  summary_raw = summary(rawdata[, marker])
  df = data.frame(
    Statistic = c("Min", "1st Qu.", "Median", "Mean", "3rd Qu.", "Max"),
    `Outlier Data` = as.numeric(summary_outlier),
    `Raw Data` = as.numeric(summary_raw)
  )
  return(df)
}

# Define the UI
ui = fluidPage(
  titlePanel("FCS Outlier Detection and Visualization"),
  
  sidebarLayout(
    sidebarPanel(
      
      selectInput("markernames", label = "Markers", choices = markernames),
      actionButton("process", "Process File")
    ),
    
    mainPanel(
      tabsetPanel(
        type = "tabs",
        tabPanel("Summary",
                 fluidRow(
                   column(12,
                    h4("Summary of Raw and Outlier Data"),
                   tableOutput("combined_summary"))

                 ))
                   ,
        tabPanel("Plots",
                 fluidRow(
                   column(6, plotOutput("boxplot")),
                   column(6, plotOutput("densityplot"))
                 )),
        tabPanel("HTML", htmlOutput("inc"))
      )
    )
  )
)

# Define the server logic
server = function(input, output, session) {
  outlierreact = reactive({
    outlier_data[, input$markernames, drop = FALSE]
  })
  
  rawreact = reactive({
    rawdata[, input$markernames, drop = FALSE]
  })

 output$combined_summary = renderTable({
    custom_summary_combined(outlier_data, rawdata, input$markernames)
  })
  
  output$boxplot = renderPlot({
    boxplot_preprocessing(input$markernames)
  })

  output$densityplot = renderPlot({
    densityplot_compare(input$markernames)
  })

  getPage = function() {
    html_files = list.files(resultsQC_path, pattern = "\\.html$", full.names = TRUE)
    
    if (length(html_files) > 0) {
      return(includeHTML(html_files[1]))
    } else {
      return("No HTML files found.")
    }
  }
  
  output$inc = renderUI({
    getPage()
  })
}

# Run the application
shinyApp(ui = ui, server = server)
