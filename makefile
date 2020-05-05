RECIPES:=recipes.mk
SOLUTION_MAKEFILE:=solution/makefile
STUDENT_MAKEFILES:=$(wildcard student/*/makefile)

${SOLUTION_MAKEFILE}: ${RECIPES}
	cp $< $@

student/%/makefile: ${RECIPES}
	cp $< $@

.PHONY: solution
solution: ${SOLUTION_MAKEFILE}
	cd solution && make partial

.PHONY: student
student/%: student/%/makefile
	cd student/$* && make partial

.phony: partial
partial: ${SOLUTION_MAKEFILE} ${STUDENT_MAKEFILES}
	cd solution && make partial
	for d in student/*/ ; do cd $$d && make partial && cd - ; done

.phony: clean
clean: ${SOLUTION_MAKEFILE} ${STUDENT_MAKEFILES}
	cd solution && make clean
	for d in student/*/ ; do cd $$d && make clean && cd - ; done
