#include <assert.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum CharType {
  NEWLINE,
  DIGIT,
  ALPHA,
};

enum CharType as_char_type(char c) {
  if (c == '\n') {
    return NEWLINE;
  } else if (isdigit(c)) {
    return DIGIT;
  } else if (isalpha(c)) {
    return ALPHA;
  }
  printf("unknown char type");
  exit(1);
}

size_t convert_to_int(char first, char last) {
  if (last == 0) {
    last = first;
  }

  char c[2] = {first, last};
  return atoi(c);
}

int part1(const char *filename) {
  FILE *fh = fopen(filename, "r");

  if (fh == NULL) {
    printf("cannot open file\n");
    exit(1);
  }

  size_t sum = 0;

  char c;
  char first = 0;
  char last = 0;

  while ((c = getc(fh)) != EOF) {
    enum CharType ct = as_char_type(c);
    switch (ct) {
    case NEWLINE:
      sum += convert_to_int(first, last);
      first = 0;
      last = 0;
      break;
    case DIGIT:
      if (first == 0) {
        first = c;
      } else {
        last = c;
      }
      break;
    default:
      break;
    };
  }
  return sum;
}

#define Case(bytes_to_read, rest_of_number, number)                            \
  bytes_read = fread(buf, sizeof(char), bytes_to_read, fh);                    \
  if (bytes_read != bytes_to_read) {                                           \
    break;                                                                     \
  }                                                                            \
  fseek(fh, -bytes_to_read, SEEK_CUR);                                         \
  if (strncmp(buf, rest_of_number, bytes_to_read) == 0) {                      \
    if (first == 0) {                                                          \
      first = number;                                                          \
    } else {                                                                   \
      last = number;                                                           \
    }                                                                          \
    break;                                                                     \
  }

int part2(const char *filename) {
  FILE *fh = fopen(filename, "r");

  if (fh == NULL) {
    printf("cannot open file\n");
    exit(1);
  }

  size_t sum = 0;
  char first = 0;
  char last = 0;
  size_t bytes_read = 0;
  char buf[5] = "00000";

  char c;
  while ((c = getc(fh)) != EOF) {
    enum CharType ct = as_char_type(c);
    switch (ct) {
    case NEWLINE:
      sum += convert_to_int(first, last);
      first = 0;
      last = 0;
      break;
    case DIGIT:
      if (first == 0) {
        first = c;
      } else {
        last = c;
      }
      break;
    case ALPHA:
      switch (tolower(c)) {
      case 'z':
        Case(3, "ero", '0');
        break;
      case 'o':
        Case(2, "ne", '1');
        break;
      case 't':
        Case(2, "wo", '2');
        Case(4, "hree", '3');
        break;
      case 'f':
        Case(3, "our", '4');
        Case(3, "ive", '5');
        break;
      case 's':
        Case(2, "ix", '6');
        Case(4, "even", '7');
        break;
      case 'e':
        Case(4, "ight", '8');
        break;
      case 'n':
        Case(3, "ine", '9');
        break;
      default:
        break;
      }
    default:
      break;
    }
  }

  if (first != 0 || last != 0) {
      sum += convert_to_int(first, last);
  }
  
  return sum;
}

#undef Case

int main() {
  size_t sum;

  sum = part1("../data/day01_part1_sample.txt");
  assert(sum == 142);
  sum = part1("../data/day01.txt");
  assert(sum == 54968);

  sum = part2("../data/day01_part2_sample.txt");
  assert(sum == 281);
  sum = part2("../data/day01.txt");
  assert(sum == 54094);

  return 0;
}