CXX = c++
CXXFLAGS = -std=c++20 -Wall -Wextra

TARGET = main

OBJS = main.o

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

.PHONY: clean
clean:
	rm -f $(TARGET) $(OBJS)
