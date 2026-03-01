# Compiler
CC = g++

# Compilation options
CFLAGS = -Wall -g

# Source files for fs
SRCS = fs1.c superblock1.c inode1.c
OBJS = $(SRCS:.c=.o)
TARGET = fs1

# Source for client
CLIENT_SRC = client.c
CLIENT_TARGET = client

# Source for disk1
DISK_SRC = disk1.c
DISK_TARGET = disk1

# Default target: build fs, client, and disk1
all: $(TARGET) $(CLIENT_TARGET) $(DISK_TARGET)

# fs build
$(TARGET): $(OBJS)
        $(CC) $(CFLAGS) $^ -o $@

%.o: %.c
        $(CC) $(CFLAGS) -c $< -o $@

# client build
$(CLIENT_TARGET): $(CLIENT_SRC)
        $(CC) $(CFLAGS) -o $(CLIENT_TARGET) $(CLIENT_SRC)

# disk1 build
$(DISK_TARGET): $(DISK_SRC)
        $(CC) $(CFLAGS) -o $(DISK_TARGET) $(DISK_SRC)

# Clean rule
clean:
        rm -f $(OBJS) $(TARGET) $(CLIENT_TARGET) $(DISK_TARGET)
