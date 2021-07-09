#!/usr/bin/env bash

# make sure the paths are correct before starting the script.
# the absolute path should be used without .vcf


declare -a files=("PGPC_0002_S1.flt" "PGPC_0012_S1.flt" "1412KHX-0011_PGPC-0022_SNP_INDEL")


snpeff="/home/armin/Downloads/Data_integratie/snpEff_latest_core/snpEff/snpEff.jar"
snpsft="/home/armin/Downloads/Data_integratie/snpEff_latest_core/snpEff/SnpSift.jar"
pythonex="extract_versions.py"
pythondb="DB_connect.py"
usagi="Usagi_v1.4.3.jar"

main()
{
	addPersons
	pipeline
}

addPersons()
{
	print "Adding person and condition info to db..."
	python3 $pythondb
}

pipeline()
{
	for file in "${files[@]}" ; do
		print "Running pipeline with: ${file}.vcf"
		print "(1/10) Filtering on chromosome 21..."
		grep -w '^#\|^#CHROM\|^chr21' ${file}.vcf > "${file}_chr21.vcf"

		print "(2/8) Annotating..."
		java -jar $snpeff GRCh37.75 -no-downstream -no-intergenic -no-intron -no-upstream -no-utr -verbose "${file}_chr21.vcf" > "${file}_ann.vcf"

		print "(3/8) Filtering missenses..."
		java -jar $snpsft filter "ANN[0].EFFECT has 'missense_variant'" "${file}_ann.vcf"  > "${file}_fmiss.vcf"

		print "(4/8) Filtering frameshifts..."
		java -jar $snpsft filter "ANN[0].EFFECT has 'frameshift_variant'" "${file}_ann.vcf"  > "${file}_fframe.vcf"

		print "(5/8) Merging missenses and frameshifts..."
		merge "${file}_fmiss.vcf" "${file}_fframe.vcf" "${file}_merged.vcf"

		print "(6/8) Deleting temporary files..."
		rm -f "${file}_chr21.vcf" "${file}_ann.vcf" "${file}_fmiss.vcf" "${file}_fframe.vcf"

		print "(7/8) Extracting 10 random samples and formatting file..."
		python3 $pythonex "${file}_merged.vcf" "${file}_USAGI.csv"

		# print "(8/10) Opening Usagi. open the file marked USAGI. follow documentation closely"
		# print "a few files are created, when saving from USAGI use those files for the correct names"
		# touch "Conditions.csv"
		# print "PIPELINE WILL CONTINUE WHEN USAGI IS CLOSED, MAKE SURE THE FILES ARE NAMED CORRECTLY"
		# java -jar $usagi

		print "(8/8) Starting DB insertion"
		python3 $pythondb

		echo "----------------------------- JOB DONE -----------------------------"

	done
		echo "------------------------ ALL JOBS COMPLETED ------------------------"
}

merge()
{
	bgzip -c "$1" > "$1.gz"
	bgzip -c "$2" > "$2.gz"
	tabix -p vcf "$1.gz"
	tabix -p vcf "$2.gz"
	bcftools merge --force-samples "$1.gz" "$2.gz" > "$3"
	rm -f "$1.gz" "$2.gz" "$1.gz.tbi" "$2.gz.tbi"
}

print(){
	now=$(date +"%T")
	echo "$now $1"
}

main
