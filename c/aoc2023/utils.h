#ifndef UTILS
#define UTILS

#include <stdio.h>
#include <stdlib.h>

static inline size_t get_file_size(FILE *fh) {
  size_t current = ftell(fh);
  fseek(fh, 0, SEEK_END);
  size_t size = ftell(fh);
  fseek(fh, current, SEEK_SET);
  return size;
}

static inline char* read_filehandle(FILE* fh) {
  size_t file_size = get_file_size(fh);
  char* str = (char*) malloc(file_size * sizeof(char));
  size_t chars_read = fread(str, sizeof(char), file_size, fh);
  if (chars_read != file_size) {
    printf("don't match: %zu, %zu", file_size, chars_read);
  }
  return str;
}

static inline char* read_file(char* filename) {
  FILE *fh = fopen(filename, "r");
  if (fh == NULL) {
    printf("cannot open file\n");
    exit(1);
  } else {
    char* str = read_filehandle(fh);
    fclose(fh);
    return str;
  }
}

#endif