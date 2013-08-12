from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO




def findORF(file_name, file_format, table, min_pro_len):  #finds 6 open reading frames
	
	record = SeqIO.read(file_name,file_format)	
	
	### Use this to Debug ###
	#record = SeqIO.read("NC_005816.fna","fasta")
	#table = 11
	#min_pro_len = 100
	pro_array = []

	for strand, nuc in [(+1, record.seq), (-1, record.seq.reverse_complement())]:
		for frame in range(3):
			length = 3 * ((len(record) - frame) //3) #Multiple of three
			for pro in nuc[frame: frame+length].translate(table).split("*"):
				if len(pro) >= min_pro_len:
					print "%s...%s - length %i, strand %i, frame %i"  %(pro[:30], pro[-3:], len(pro), strand, frame)
					pro_array.append(pro)
	return pro_array




def blastNtFile(file_name, file_format):  #performs an online BLAST search for the file
	E_VALUE_THRESH = 0.04

	record = SeqIO.read(file_name, file_format)
	
	result_handle = NCBIWWW.qblast("blastn", "nt", record.seq)
	
	save_file = open("my_blast.xml", 'w')
	save_file.write(result_handle.read() )
	save_file.close()
	result_handle.close()

	result_handle = open("my_blast.xml")
	blast_records = NCBIXML.read(result_handle)

	for alignment in blast_records.alignments:
		for hsp in alignment.hsps:
			print '****Alignment****'
			print 'sequence:', alignment.title
			print 'length:', alignment.length

def blastPtSeq(seq):
	#results = []
	#for i in range( len(seq) )
	result_handle = NCBIWWW.qblast("blastp", "nr", seq)
	
	save_file = open("my_blast.xml", 'w')
	save_file.write(result_handle.read() )
	save_file.close()
	result_handle.close()

	result_handle = open("my_blast.xml")
	blast_records = NCBIXML.read(result_handle)

	for alignment in blast_records.alignments:
		for hsp in alignment.hsps:
			print '****Alignment****'
			print 'sequence:', alignment.title
			print 'length:', alignment.length
	
	
#blastSeq("CAGCGCCCCCAGCTCGAAGCGCTGCTGAGCTTCGTCCGCGAAGGCGATACAGTGGTGGTGCACAGCATGG")

pro_array = findORF("NC_005816.fna","fasta",11, 100)
for i in range (len(pro_array)):
	blastPtSeq(pro_array[i])

blastNtFile("NC_005816.fna","fasta")

	
