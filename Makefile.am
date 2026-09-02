AUTOMAKE_OPTIONS = foreign

bin_PROGRAMS = cudaica
SRC=src
INCLUDE=-Iinclude/ -Ilib/include
R250_sources=lib/r250/r250.c lib/r250/randlcg.c
Python_sources=python/Makefile.in python/bindings.c python/setup.py
STATICLIBS=$(R250)
EXTRALIBS=lib/
EXTRA_DIST=cudaica.c $(R250_sources) lib/r250/Makefile LICENSE matlab/cudaica.m $(Python_sources) \
	README.md CHANGELOG.md OPTIMIZATION_NOTES.md BENCHMARKS.md LICENSE_AUDIT.md \
	THIRD_PARTY_NOTICES.md CITATION.cff SOURCE_ONLY_AUDIT.md PRE_PUBLICATION_AUDIT.md \
	scripts/run_cudaica_mkl.sh tests/README.md tests/run_regression.py \
	tests/fixtures/input_16x40000.fdt patches/stage1_memory_probe.patch \
	patches/stage3_varsort.patch benchmarks/a100_64ch_180k_results.txt
SRCINCLUDE=include/
noinst_HEADERS = $(SRCINCLUDE)/config.h $(SRCINCLUDE)/whitening.h $(SRCINCLUDE)/device.h $(SRCINCLUDE)/loader.h $(SRCINCLUDE)/centering.h $(SRCINCLUDE)/error.h $(SRCINCLUDE)/common.h $(SRCINCLUDE)/infomax.h $(SRCINCLUDE)/postprocess.h lib/include/r250.h lib/include/randlcg.h $(SRCINCLUDE)/cblas.h $(SRCINCLUDE)/preprocess.h
cudaica_SOURCES = $(SRC)/whitening.cu $(SRC)/device.cu $(SRC)/loader.cu $(SRC)/config.cu $(SRC)/centering.cu $(SRC)/error.cu $(SRC)/common.cu $(SRC)/infomax.cu $(SRC)/postprocess.cu
cudaica_LDADD =
SUFFIXES=.cu
.cu.o:
	$(NVCC) $(NVCCFLAGS) $(INCLUDE) -c -o $@ $<

cudaica$(EXEEXT): cudaica.c $(cudaica_OBJECTS) $(STATICLIBS)
	$(NVCC) $(NVCCFLAGS) $(INCLUDE) $(LAPACK_LIBS) $(BLAS_LIBS) $(LIBS) $(FLIBS) $(CUDA_LIBS) -o $@ $^

$(R250): $(R250_sources)
	cd lib/r250/ && make $(R250_target)

dist-hook:
	echo "echo $(shell ./evalrev) " > $(distdir)/evalrev
	chmod +x $(distdir)/evalrev
