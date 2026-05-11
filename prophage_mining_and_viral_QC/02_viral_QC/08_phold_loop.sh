#!/usr/bin/env bash

# Number of threads (modify as needed)
THREADS=8

# Loop through all .gbk files in the current directory
for gbk in *.gbk; do
  # Strip the .gbk extension to get the base name
  base="${gbk%.gbk}"
  
  # Define the output directory and prefix based on the input file name
  outdir="$base"
  prefix="$base"
  
  # Print status
  echo "Running phold on '$gbk' -> output directory '$outdir', prefix '$prefix'"
  
  # Run phold
  phold run -i "$gbk" -o "$outdir" -t "$THREADS" -p "$prefix"
done
