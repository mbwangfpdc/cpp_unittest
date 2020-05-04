COMPILER=g++ -std=c++11
FLAGS=-Werror -Wall -O3

OBJS=$(patsubst %.cpp, build/%.o, $(wildcard *.cpp))
PARTIAL_OBJ=build/PARTIAL.o

partial: ${OBJS}
	ld -r -o ${PARTIAL_OBJ} $^

build/%.o: %.cpp
	$(COMPILER) $(FLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -rf build/*
