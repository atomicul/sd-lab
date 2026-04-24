CXXFLAGS := $(CXXFLAGS) -std=c++23 -O3
CPPFLAGS := $(CPPFLAGS) -Iinclude

SRC_DIR = src

main:

%: $(SRC_DIR)/%
	cp $< $@

$(SRC_DIR)/%: $(SRC_DIR)/%.o
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.PHONY: clean
clean:
	rm -f main
