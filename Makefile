#
# By Hogenimushi
#
PYTHON=python
START_RIGHT= data_20Hz/startright_01 data_20Hz/startright_02 data_20Hz/startright_03  data_20Hz/startright_04 \
data_20Hz/startright_05 data_20Hz/startright_06 data_20Hz/startright_07 data_20Hz/startright_08 \
data_20Hz/startright_09 data_20Hz/startright_10 

START_RIGHT= data_20Hz/startright_01 data_20Hz/startright_02 data_20Hz/startright_03 data_20Hz/startright_04 data_20Hz/startright_05 \
data_20Hz/startright_06 data_20Hz/startright_07 data_20Hz/startright_08 data_20Hz/startright_09 data_20Hz/startright_10 

DATASET_SLOW=data_20Hz/middle_001 $(START_RIGHT)
DATASET_FAST=data_20Hz/lap_001 data_20Hz/lap_002 data_20Hz/lap_003 data_20Hz/lap_004 data_20Hz/lap_005 \
data_20Hz/lap_006 data_20Hz/lap_007 data_20Hz/lap_008 data_20Hz/leftcut_001 data_20Hz/rightcut_001 $(START_RIGHT) 


DATASET_10Hz = $(shell find data_10Hz -type d | sed -e '1d' | tr '\n' ' ')
#DATASET_10Hz=data_10Hz/lap_01 data_10Hz/lap_02 data_10Hz/lap_03 data_10Hz/lap_04 data_10Hz/lap_05 \
#data_10Hz/lap_06 data_10Hz/lap_07 data_10Hz/lap_08 data_10Hz/lap_09 data_10Hz/lap_10 \
#data_10Hz/leftcut_01 data_10Hz/rightcut_01 data_10Hz/slow_01

DATASET_05Hz = $(shell find data_05Hz -type d | sed -e '1d' | tr '\n' ' ')

#DATASET_05Hz=data_05Hz/conservative_001 data_05Hz/conservative_002 data_05Hz/conservative_003 data_05Hz/conservative_004 \
#data_05Hz/lap_001 data_05Hz/lap_002 data_05Hz/lap_003 data_05Hz/lap_004 data_05Hz/lap_005 \
#data_05Hz/rightcut_001 data_05Hz/leftcut_001 \
#data_05Hz/startright_01 data_05Hz/startright_02 data_05Hz/startright_03 data_05Hz/startright_04 \
#data_05Hz/startright_05 \
#data_05Hz/startright_06 data_05Hz/startright_07 data_05Hz/startright_08 data_05Hz/startright_09 data_05Hz/startright_00 \
#data_05Hz/startleft_01 data_05Hz/startleft_02 data_05Hz/startleft_03 data_05Hz/startleft_04 data_05Hz/startleft_05 \
#data_05Hz/startleft_06 data_05Hz/startleft_07 data_05Hz/startleft_08 data_05Hz/startleft_09 data_05Hz/startleft_10

#DATASET_05Hz=data_05Hz/lap_003 data_05Hz/lap_004 data_05Hz/lap_005 \
#data_05Hz/lap_006 data_05Hz/leftcut_001 data_05Hz/rightcut_001 data_20Hz/startright_01


COMMA=,
EMPTY=
SPACE=$(EMPTY) $(EMPTY)
DATASET_SLOW_ARG=$(subst $(SPACE),$(COMMA),$(DATASET_SLOW))


none:
	@echo "Argument is required."


run: models_prebuilt/fastrnn_10.h5
	$(PYTHON) manage.py drive --model=$< --type=rnn --myconfig=configs/myconfig_10Hz.py

race: models_prebuilt/fastrnn_10.h5
	$(PYTHON) manage.py drive --model=$< --type=rnn --myconfig=configs/race_10Hz.py

train:
	make models_prebullt/fastrnn10.h5

models_prebullt/fastrnn_10.h5: models/laprnn_10.h5	
	cp models/raprnn_10.h5 models_prebuilt/fastrnn10.h5

record05:
	$(PYTHON) manage.py drive --js --myconfig=configs/myconfig_05Hz.py

record10:
	$(PYTHON) manage.py drive --js --myconfig=configs/myconfig_10Hz.py

record20:
	$(PYTHON) manage.py drive --js 


run05: models/lap_05.h5
	$(PYTHON) manage.py drive --model=models/lap_05.h5 --type=linear

runrnn05: models/laprnn_05.h5
	$(PYTHON) manage.py drive --model=models/laprnn_05.h5 --type=rnn --myconfig=configs/myconfig_05Hz.py

run_fast20: models/fast_20.h5
	$(PYTHON) manage.py drive --model=models/fast_20.h5 --type=linear

run_slow20:
	$(PYTHON) manage.py drive --model=models/slow_20.h5 --type=linear

race_fast20: models/fast_20.h5
	$(PYTHON) manage.py drive --model=$< --type=linear --myconfig=configs/race.py

race_slow20: models/slow_20.h5
	$(PYTHON) manage.py drive --model=$< --type=linear --myconfig=configs/race.py

race05: models/lap_05.h5
	$(PYTHON) manage.py drive --model=$< --type=linear --myconfig=configs/race_05Hz.py

train:
	make models/default.h5

train_3d:
	make models/default_3d.h5

train_fast20:
	make models/fast_20.h5

train_slow20:
	make models/slow_20.h5
train_lap05:
	make models/lap_05.h5
train_lap3d05:
	make models/lap3d_05.h5

train_laprnn05:
	make models/laprnn_05.h5

train_laprnn10:
	make models/laprnn_10.h5

models/slow_20.h5: $(DATASET_SLOW)
	$(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=linear

models/fast_20.h5: $(DATASET_FAST)
	$(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=linear

models/fast3d_20.h5: $(DATASET_FAST)
	$(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=3d

models/default.h5:
	$(PYTHON) manage.py train --tub=`ls data | tr '\n' ' '` --model=$@ --type=linear

models/default_3d.h5:
	TF_FORCE_GPU_ALLOW_GROWTH=true $(PYTHON) manage.py train --tub=`ls data | tr '\n' ' '` --model=$@ --type=3d

models/default_rnn.h5:
	TF_FORCE_GPU_ALLOW_GROWTH=true $(PYTHON) manage.py train --tub=`find data -name *| tr '\n' ','` --model=$@ --type=rnn

models/lap_05.h5: $(DATASET_05Hz)
	$(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=linear --myconfig=configs/myconfig_05Hz.py

models/lap3d_05.h5: $(DATASET_05Hz)
	TF_FORCE_GPU_ALLOW_GROWTH=true $(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=3d --myconfig=configs/myconfig_05Hz.py

models/laprnn_05.h5: $(DATASET_05Hz)
	TF_FORCE_GPU_ALLOW_GROWTH=true $(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=rnn --myconfig=configs/myconfig_05Hz.py

models/laprnn_10.h5: $(DATASET_10Hz)
	TF_FORCE_GPU_ALLOW_GROWTH=true $(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=rnn --myconfig=configs/myconfig_10Hz.py

models/laprnn_20.h5: $(DATASET_10Hz)
	TF_FORCE_GPU_ALLOW_GROWTH=true $(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=rnn --myconfig=configs/myconfig.py

trim_crash_001:
	$(PYTHON) scripts/trimming.py --input data_20Hz/crash_001 --output data_generated/crash_001 --file data_20Hz/crash_001_trim.txt

trim_10Hz_leftcut_01:
	$(PYTHON) scripts/trimming.py --input data_10Hz/leftcut_01 --output data_generated/leftcut_01 --file data_10Hz/leftcut_01_trim.txt

trim_10Hz_rightcut_01:
	$(PYTHON) scripts/trimming.py --input data_10Hz/rightcut_01 --output data_generated/rightcut_01 --file data_10Hz/rightcut_01_trim.txt

trim_20Hz_car_01:
	$(PYTHON) scripts/trimming.py --input data_20Hz/car_01 --output data_generated/car_01 --file data_20Hz/car_01_trim.txt
	
trim_20Hz_car_02:
	$(PYTHON) scripts/trimming.py --input data_20Hz/car_02 --output data_generated/car_02 --file data_20Hz/car_02_trim.txt

clean:
	rm -fr models/*
