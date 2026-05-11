import re

input_file = "CDS_summary_output.txt"
output_file = "prophages_passed_QC.txt" # save output

parent_re = re.compile(r'^File:\s+\./([^/]+)/')
ge3_re = re.compile(r'≥\s*3\s*structural\?\s*:\s*(Yes|No)', re.IGNORECASE)
ge20_re = re.compile(r'≥\s*20%\s*of\s*total\?\s*:\s*(Yes|No)', re.IGNORECASE)

selected = []

current_parent = None
ge3_yes = False
ge20_yes = False

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        m_parent = parent_re.match(line)
        if m_parent:
            # If previous record qualifies, save it
            if current_parent and ge3_yes and ge20_yes:
                selected.append(current_parent)

            # Start new record
            current_parent = m_parent.group(1)
            ge3_yes = False
            ge20_yes = False
            continue

        m_ge3 = ge3_re.search(line)
        if m_ge3:
            ge3_yes = (m_ge3.group(1).lower() == "yes")

        m_ge20 = ge20_re.search(line)
        if m_ge20:
            ge20_yes = (m_ge20.group(1).lower() == "yes")

# Check last record
if current_parent and ge3_yes and ge20_yes:
    selected.append(current_parent)

# Print the results
for parent in selected:
    print(parent)

# Optionally, save to a text file
with open(output_file, "w", encoding="utf-8") as out:
    for parent in selected:
        out.write(parent + "\n")

print(f"\n✅ Found {len(selected)} qualifying parent directories. Saved to '{output_file}'.")
