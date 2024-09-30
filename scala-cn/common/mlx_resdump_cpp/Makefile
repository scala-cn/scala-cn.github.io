# Compiler and flags
CXX := g++
CXXFLAGS := -Wall -fpermissive -fPIC -std=c++11
# LDFLAGS := -shared
LDFLAGS := -ldl -libverbs -lmlx5 -shared
# CFLAGS   := -Wall -fPIC -std=c++11

# Directories
SRC_DIR := src
INCLUDE_DIR := include
BUILD_OBJ_DIR := $(BUILD_DIR)/obj/resourcedump
LIB_DIR := $(BUILD_DIR)/lib

# SUBDIRS := $(wildcard $(SRC_DIR)/*)

# Source files
# SRCS := $(foreach subdir, $(SUBDIRS), $(wildcard $(subdir)/*.cpp))
SRCS := $(wildcard $(SRC_DIR)/*.cpp $(SRC_DIR)/*.c $(SRC_DIR)/*/*.cpp $(SRC_DIR)/*/*.c)
HDRS := $(wildcard $(INCLUDE_DIR)/* $(INCLUDE_DIR)/*)

# Object files
# OBJS := $(foreach subdir, $(SUBDIRS), $(BUILD_DIR)/$(notdir $(subdir))/$(patsubst %.cpp, %.o, $(wildcard $(subdir)/*.cpp)))
OBJS := $(patsubst %.c, %.o, $(patsubst %pp, %, $(SRCS)))
OBJS := $(patsubst $(SRC_DIR)%, $(BUILD_OBJ_DIR)%, $(OBJS))

# Target shared library
TARGET := $(LIB_DIR)/libresdump.so

# Include directories
# INC_DIRS := -I$(INCLUDE_DIR)

# $(warning wild is $(wildcard src/commands/*.cpp))
# $(warning   BUILD_DIR is $(BUILD_DIR))
# $(warning   SUBDIRS is $(SUBDIRS))
$(warning   SRCS is $(SRCS))
# $(warning   HDRS is $(HDRS))
$(warning   OBJS is $(OBJS))
$(warning   LIB_DIR is $(LIB_DIR))
$(warning   TARGET is $(TARGET))

# EXT := c cpp

# define rule =
# $(BUILD_DIR)/%.$(1).o: $(SRC_DIR)/%.$(1)
# 	@mkdir -p $(@D)
# 	$$(COMPILE.$(1)) $$< -o $$@
# endef

# Build rule
all: $(TARGET)

# Compile source files to object files
$(BUILD_OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(HDRS:%=-I%) -c $< -o $@

$(BUILD_OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(HDRS:%=-I%) -c $< -o $@

# Link object files to create shared library
$(TARGET): $(OBJS)
	@mkdir -p $(@D)
	$(CXX) $(LDFLAGS) $^ -o $@

# $(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp $(SRC_DIR)/%.c
# 	@mkdir -p $(@D)
# 	$(CXX) $(CXXFLAGS) $(HDRS:%=-I%) -c $< -o $@

# $(foreach ext, $(EXT), $(eval $(call rule,$(ext))))

# Clean rule
clean:
	rm -rf $(BUILD_OBJ_DIR) $(LIB_DIR)

# Phony target to clean and build
rebuild: clean all

# .PHONY tells make that the specified targets do not represent files
.PHONY: all clean rebuild