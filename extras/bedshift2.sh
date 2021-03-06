#!/bin/bash
for filename in *.bed; do
	CHROM_LENGTHS=../tests/hg38.chrom.sizes
	BEDFILE=$filename
	DROP_RATE=0.3

	ADD_RATE=0.2
	ADD_MEAN=320.0
	ADD_STDEV=30.0

	SHIFT_RATE=0.2
	SHIFT_MEAN=0.0
	SHIFT_STDEV=150.0

	CUT_RATE=0.0
	MERGE_RATE=0.0

	bedshift --bedfile $BEDFILE --chrom-lengths $CHROM_LENGTHS --droprate $DROP_RATE --addrate $ADD_RATE --addmean $ADD_MEAN --addstdev $ADD_STDEV --shiftrate $SHIFT_RATE --shiftmean $SHIFT_MEAN --shiftstdev $SHIFT_STDEV --cutrate $CUT_RATE --mergerate $MERGE_RATE
done