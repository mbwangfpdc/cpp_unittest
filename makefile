COMPILER=g++ -std=c++11
FLAGS=-Werror -Wall -O3
PARTIAL_LINK=ld -r

OBJS=student.o solution.o main.o

PLINK_TARGET=partial.o

all: $(OBJS)
	$(COMPILER) $(FLAGS) $^ -o main.exe

objs: $(OBJS)

%.o: %.cpp
	$(COMPILER) $(FLAGS) -c $<

clean:
	rm -rf *.o main.exe
