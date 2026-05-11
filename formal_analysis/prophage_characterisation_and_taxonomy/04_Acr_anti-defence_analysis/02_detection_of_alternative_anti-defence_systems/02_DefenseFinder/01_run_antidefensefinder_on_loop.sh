# DefenseFinder `--antidefensefinder` module
#!/bin/bash

# Loop through each directory
for dir in */; do
  # Remove trailing slash from directory name
  dir=${dir%/}
  
  # Construct the .faa file path
  faa_file="${dir}/${dir}.faa"
  
  # Run the defense-finder command if the .faa file exists
  if [[ -f "$faa_file" ]]; then
    echo "Running defense-finder for $faa_file"
    defense-finder run "$faa_file" --out-dir "defensefinder_$dir" --antidefensefinder
  else
    echo "File $faa_file not found. Skipping."
  fi
done
