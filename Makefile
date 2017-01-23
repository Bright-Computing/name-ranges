REPORT_DIR=$(PWD)/static-check

export REPORT_DIR

all: static-check static-check-report

syntax-static-check:
	$(MAKE) -C nameranges static-check

static-check-report: syntax-static-check
	$(MAKE) -C $(REPORT_DIR) all


