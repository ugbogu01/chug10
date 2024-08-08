# Load the required package
library(flowCore)

# Identify the files
fcs_file = ""
wsp_file = ""
# A vector
celltypes = ""

csvlabels = function(fcs_file, wsp_file, celltypes){
  #check if file path exist
  if (file.exists(fcs_file)) {
    print("The .fcs file exists!")
  } else {
    print("The .fcs file does not exist.")
  }
  
  if (file.exists(wsp_file)) {
    print("The .wsp file exists!")
  } else {
    print("The .wsp file does not exist.")
  }
  
  # List all FCS files in the given directory
  fcs_files = list.files(fcs_file, pattern = ".fcs", recursive = TRUE)

  # Parse the FlowJo workspace
  gatingResult = GetFlowJoLabels(fcs_files, wsp_file,
                                 cellTypes = celltypes,
                                 getData = TRUE)
  
  # Define the column names to be included in the subset
  # This could be related to the celltypes given initially
  selected_columns = c("Lymphocytes", "Single Cells", "Live", "CD3+")
  
  # Loop over each element in gatingResult and extract the matrix and save the subset
  for (i in names(gatingResult)) {
    # Extract the matrix
    subset_matrix = gatingResult[[i]]$matrix[, selected_columns, drop=FALSE]
    i = gsub("\\.fcs$", "", i)
    
    # Give the output folder
    output_folder = sprintf("/path/to/%s.csv", i)
    
    # Extract the directory path from output_folder
    dir_path = dirname(output_folder)
    
    # Create the directory if it does not exist
    if (!dir.exists(dir_path)) {
      dir.create(dir_path, recursive = TRUE)
    }
    
    # Write the CSV file
    write.csv(subset_matrix, file = output_folder, row.names = FALSE)
  }
}

