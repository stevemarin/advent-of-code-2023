
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>

//
// Shape struct stuff
//
typedef struct Shape {
  size_t rows;
  size_t cols;
} Shape;

Shape Shape_from_file(FILE *fh) {

  Shape shape = {0};
  bool seen_newline = false;

  fseek(fh, 0, SEEK_SET);

  int c_as_int;
  while ((c_as_int = getc(fh)) != EOF) {
    if (c_as_int > CHAR_MAX) {
      printf("cannot covert int to char");
      exit(1);
    }
    char c = (char)c_as_int;

    if (c == '\n') {
      seen_newline = true;
      shape.rows++;
    }
    if (!seen_newline) {
      shape.cols++;
    }
  }
  return shape;
}

size_t Shape_num_elements(Shape shape) { return shape.rows * shape.cols; }

//
// Number struct stuff
//
typedef struct Number {
  Shape start;
  size_t length;
  size_t value;
} Number;

void Number_print(Number const *const number) {
  printf("Number: value: %zu, shape: row=%zu, col=%zu, length: %zu",
         number->value, number->start.rows, number->start.cols, number->length);
}

//
// Matrix struct stuff
//
typedef struct Matrix {
  Shape shape;
  char *data;
  size_t *strides;
} Matrix;

size_t Matrix_element_from_Shape(Matrix const *const matrix, Shape shape) {
  return (*matrix).shape.cols * shape.rows + shape.cols;
}

Shape Matrix_idx_to_coords(Matrix const *const matrix, size_t idx) {
  size_t col = idx % (*matrix).shape.rows;
  size_t row = (idx - col) / (*matrix).shape.cols;
  Shape shape = {.rows = row, .cols = col};
  return shape;
}

Matrix Matrix_init_from_file(FILE *fh) {
  Shape shape = Shape_from_file(fh);
  fseek(fh, 0, SEEK_SET);
  char *data = (char *)calloc(Shape_num_elements(shape), sizeof(char));

  printf("Rows: %zu. Cols: %zu\n", shape.rows, shape.cols);

  int c_as_int;
  size_t idx = 0;
  while ((c_as_int = getc(fh)) != EOF) {
    if (c_as_int > CHAR_MAX) {
      printf("cannot covert int to char");
      exit(1);
    }
    char c = (char)c_as_int;
    if (c != '\n') {
      data[idx++] = (char)c;
    }
  }

  size_t strides[2] = {0};
  strides[0] = shape.cols;
  strides[1] = 1;

  Matrix matrix = {.shape = shape, .data = data, .strides = strides};
  return matrix;
}

void Matrix_free(Matrix *matrix) { free(matrix->data); }

void Matrix_print(Matrix matrix) {
  char *data = matrix.data;
  for (size_t row = 0; row < matrix.shape.rows; row++) {
    for (size_t col = 0; col < matrix.shape.cols; col++) {
      printf("%c", *data++);
    }
    printf("\n");
  }
}

//
// problem specific
//

//
// main
//
int main() {
  const char *filename = "../data/day03_sample.txt";
  FILE *fh = fopen(filename, "r");
  if (fh == NULL) {
    printf("cannot open file\n");
    exit(1);
  }

  Matrix matrix = Matrix_init_from_file(fh);
  Matrix_print(matrix);

  size_t num_symbols = 0;
  Shape symbol_locations[1024] = {0};

  for (size_t idx = 0; idx < Shape_num_elements(matrix.shape); idx++) {
    char c = matrix.data[idx];
    if ((c < '0' || c > '9') && c != '.') {
      symbol_locations[num_symbols++] = Matrix_idx_to_coords(&matrix, idx);
    }
  }

  printf("\nNum Symbols: %zu\n", num_symbols);
  for (size_t idx = 0; idx < num_symbols; idx++) {
    Shape shape = symbol_locations[idx];
    printf("Shape: row=%zu, col=%zu\n", shape.rows, shape.cols);
  }

  size_t num_numbers = 0;
  Number numbers[1024] = {0};

  for (size_t idx = 0; idx < Shape_num_elements(matrix.shape); idx++) {
    char c = matrix.data[idx];

    u_int8_t number_length = 0;
    Shape number_start;
    bool first_number = true;

    while ('0' <= c && c <= '9') {
      if (first_number) {
        number_start = Matrix_idx_to_coords(&matrix, idx);
        first_number = false;
      }
      c = matrix.data[idx + ++number_length];
    }

    if (number_length > 0) {
      char *buffer[5] = {0};
      memcpy(buffer, &matrix.data[idx], number_length);
      size_t value = atol((char *)&buffer);
      
      Number number = {.start = number_start, .length = number_length, .value = value};
      numbers[num_numbers++] = number;

      idx += number_length;
      number_length = 0;
      first_number = true;
    }
  }

  printf("\nNum Numbers: %zu\n", num_numbers);
  for (size_t idx = 0; idx < num_numbers; idx++) {
    Number const *const num = &numbers[idx];
    Number_print(num);
    printf("\n");
  }

  Matrix_free(&matrix);

  return 0;
}