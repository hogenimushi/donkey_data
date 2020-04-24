#
# By Hogenimushi
#
PYTHON=python
START_RIGHT= data_20Hz/startright_01 data_20Hz/startright_02 data_20Hz/startright_03  data_20Hz/startright_04 \
data_20Hz/startright_05 data_20Hz/startright_06 data_20Hz/startright_07 data_20Hz/startright_08 \
data_20Hz/startright_09 data_20Hz/startright_10 data_20Hz/startright_11 data_20Hz/startright_12 \
data_20Hz/startright_13 data_20Hz/startright_14 data_20Hz/startright_15 data_20Hz/startright_16 \
data_20Hz/startright_17 data_20Hz/startright_18 data_20Hz/startright_19 data_20Hz/startright_20
DATASET_SLOW=data_20Hz/middle_001 $(START_RIGHT)
DATASET_FAST=data_20Hz/lap_001 data_20Hz/lap_002 data_20Hz/lap_003 data_20Hz/lap_004 data_20Hz/lap_005 \
data_20Hz/lap_006 data_20Hz/lap_007 data_20Hz/lap_008 data_20Hz/leftcut_001 data_20Hz/rightcut_001 $(START_RIGHT) 

COMMA=,
EMPTY=
SPACE=$(EMPTY) $(EMPTY)
DATASET_SLOW_ARG=$(subst $(SPACE),$(COMMA),$(DATASET_SLOW))


none:
	@echo "Argument is required."

record05:
	$(PYTHON) manage.py drive --js --myconfig=configs/myconfig_05Hz.py

record10:
	$(PYTHON) manage.py drive --js --myconfig=configs/myconfig_10Hz.py

record20:
	$(PYTHON) manage.py drive --js 


run05: models/lap_05.h5
	$(PYTHON) manage.py drive --model=models/lap_05.h5 --type=linear

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
	@make models/default.h5
train_3d:
	@make models/default_3d.h5

train_fast20:
	@make models/fast_20.h5

train_slow20:
	@make models/slow_20.h5

models/slow_20.h5: $(DATASET_SLOW)
	$(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=linear

models/fast_20.h5: $(DATASET_FAST)
	$(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=linear

models/fast3d_20.h5: $(DATASET_FAST)
	$(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=3d

models/default.h5:
	$(PYTHON) manage.py train --tub=`ls data | tr '\n' ' '` --model=$@ --type=linear
	
models/default_3d.h5:
	$(PYTHON) manage.py train --tub=`ls data | tr '\n' ' '` --model=$@ --type=3d

models/default_rnn.h5:
	$(PYTHON) manage.py train --tub=`ls data | tr '\n' ' '` --model=$@ --type=rnn

# Yattsuke
models/lap_05.h5: data_05Hz/lap_001 data_05Hz/lap_002 data_05Hz/leftcut_001 data_05Hz/rightcut_001
	$(PYTHON) manage.py train --tub=$(subst $(SPACE),$(COMMA),$^) --model=$@ --type=linear

trimming_crash_001:
	$(PYTHON) configs/trimming.py --input data_20Hz/crash_001 --output data/crash_001 --file configs/trimming_crash_001

clean:
	rm -fr models/slow_20.h5 models/fast_20.h5 models/fast3d_20.h5 models/*.png
