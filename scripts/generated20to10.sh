for file in *; do
		python3 ../scripts/change_freq.py --input "${file}" --test --output ../data_generated_10Hz/"${file}"
done
