# Compiler
CC = g++

# Compilation options
CFLAGS = -Wall -g

# Source files
SRCS = fs.c superblock.c inode.c

# Object files
OBJS = $(SRCS:.c=.o)

# Executable file
TARGET = fs

# Default target
all: $(TARGET)

# Generate the executable file
$(TARGET): $(OBJS)
       $(CC) $(CFLAGS) $^ -o $@

# Rule for generating object files
%.o: %.c
       $(CC) $(CFLAGS) -c $< -o $@

# Clean rule
clean:
       rm -f $(OBJS) $(TARGET)    

