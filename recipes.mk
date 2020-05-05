COMPILER=g++ -std=c++11
FLAGS=-Werror -Wall -O3

OBJS=$(patsubst %.cpp, build/%.o, $(wildcard *.cpp))
PARTIAL_OBJ=build/PARTIAL.o

build:
	mkdir build

partial: ${OBJS} | build
	ld -r -o ${PARTIAL_OBJ} $^

build/%.o: %.cpp | build
	$(COMPILER) $(FLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -rf build/*
