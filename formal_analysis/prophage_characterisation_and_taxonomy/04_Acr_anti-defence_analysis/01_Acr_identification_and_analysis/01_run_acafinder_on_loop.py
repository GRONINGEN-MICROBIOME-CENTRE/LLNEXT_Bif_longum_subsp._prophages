import os
import subprocess

# Set your directory containing the fasta files
input_dir = '/path/to/individual/phage_genomes.fna'
threads = 8

for fasta_file in os.listdir(input_dir):
    if fasta_file.endswith('.fna'):
        fasta_path = os.path.join(input_dir, fasta_file)
        output_folder = os.path.join(input_dir, 'acafinder_' + fasta_file.replace('.fna', ''))
        cmd = [
            'python3', 'AcaFind_runner.py',
            '--FNA_file', fasta_path,
            '-d', str(threads),
            '--Virus',
            '-o', output_folder
        ]
        print("Running:", " ".join(cmd))
        subprocess.run(cmd)
