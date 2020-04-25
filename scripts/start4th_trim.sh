for file in $(ls . |grep start4th); do
		python3 ../scripts/trimming_data.py "${file}" 1 200 ../data_generated_20Hz/"${file}"
done
