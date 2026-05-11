#1
spacepharer createsetdb filtered_phage_set.fasta phageDB tmp_phage

#2
spacepharer createsetdb filtered_phage_set.fasta phageDB_rev tmp_phage_rev --reverse-fragments 1

#3
spacepharer createsetdb concatenated_spacers.fa spacerDB tmp_spacer --extractorf-spacer 1

#4
spacepharer predictmatch spacerDB phageDB phageDB_rev CRISPR_phage_matches.tsv tmp_run
