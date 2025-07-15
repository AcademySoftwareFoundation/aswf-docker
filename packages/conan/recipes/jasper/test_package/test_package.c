/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/5f19361f49bc31a349b383c1f95c7f79627f728a/recipes/jasper/all/test_package/test_package.c
*/

#include <jasper/jasper.h>

#include <stdio.h>

int main(int argc, char **argv)
{
	int i;
	jas_tmr_t tmr;
	jas_tmr_t dummytmr;
	double t;
	int numiters;

	numiters = 2;

	jas_tmr_start(&tmr);
	for (i = numiters; i > 0; --i) {
		jas_tmr_start(&dummytmr);
	}
	jas_tmr_stop(&tmr);
	t = jas_tmr_get(&tmr);
	t /= numiters;
	printf("jas_tmr_start %.3f us\n", t * 1e6);

	jas_tmr_start(&tmr);
	for (i = numiters; i > 0; --i) {
		jas_tmr_stop(&dummytmr);
	}
	jas_tmr_stop(&tmr);
	t = jas_tmr_get(&tmr);
	t /= numiters;
	printf("jas_tmr_stop  %.3f us\n", t * 1e6);

	t = 0;
	for (i = numiters; i > 0; --i) {
		jas_tmr_start(&tmr);
		jas_tmr_stop(&tmr);
		t += jas_tmr_get(&tmr);
	}
	t /= numiters;
	printf("zero time %.3f us\n", t * 1e6);

	return 0;
}
