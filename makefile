COMPILER=g++ -std=c++11
FLAGS=-Werror -Wall -O3
PARTIAL_LINK=ld -r

OBJS=student.o solution.o

PLINK_TARGET=partial.o

objs: $(OBJS)

%.o: %.cpp
	$(COMPILER) $(FLAGS) -c $<

plink: $(OBJS) 
	$(PARTIAL_LINK) $(OBJS) -o $(PLINK_TARGET)

clean:
	rm -rf *.o
