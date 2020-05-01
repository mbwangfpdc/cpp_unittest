COMPILER=g++ -std=c++11
FLAGS=-Werror -Wall -O3

OBJS=build/student.o build/solution.o build/main.o

objs: $(OBJS)

build/%.o: %.cpp
	$(COMPILER) $(FLAGS) -c $< -o $@

clean:
	rm -rf build/*
