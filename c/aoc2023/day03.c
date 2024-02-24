
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
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
// dynamic array stuff
//

// typedef struct {
//   Shape *data;
//   size_t used;
//   size_t size;
// } Array;

// void Array_init(Array *arr, size_t num) {
//   arr->data = malloc(num * sizeof(Shape));
//   arr->used = 0;
//   arr->size = num;
// }

// void Array_insert(Array *arr, Shape shape) {
//   if (arr->used == arr->size) {
//     arr->size *= 2;
//     arr->data = realloc(arr->data, arr->size * sizeof(Shape));
//   }
//   arr->data[arr->used++] = shape;
// }

// void Array_free(Array *arr) {
//   free(arr->data);
//   arr->data = NULL;
//   arr->used = arr->size = 0;
// }

//
// Matrix struct stuff
//
typedef struct Matrix {
  Shape shape;
  char *data;
  size_t *strides;
} Matrix;

size_t Matrix_element_from_Shape(Matrix const* const matrix, Shape shape) {
  return (*matrix).shape.cols * shape.rows + shape.cols;
}

Shape Matrix_idx_to_coords(Matrix const *const matrix, size_t idx) {
  size_t col = idx % (*matrix).shape.rows;
  size_t row = (idx - col) / (*matrix).shape.cols;
  Shape shape = {.rows=row, .cols=col};
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

  size_t num_locations = 0;
  Shape symbol_locations[1024] = {0};
  for (size_t idx = 0; idx < Shape_num_elements(matrix.shape); idx++) {
    char c = matrix.data[idx];
    printf("c: %c\n", c);
    if ((c < '0' || c > '9') && c != '.') {
      symbol_locations[num_locations++] = Matrix_idx_to_coords(&matrix, idx);
    }
  }

  printf("Num Locations: %zu\n", num_locations);
  for (size_t idx = 0; idx < num_locations; idx++) {
    Shape shape = symbol_locations[idx];
    printf("Shape: row=%zu, col=%zu\n", shape.rows, shape.cols);
  }

  Matrix_free(&matrix);

  return 0;
}