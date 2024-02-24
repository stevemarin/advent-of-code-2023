
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>

#define BUFFER_LENGTH 256
#define NUM_ROUNDS 10
#define NUM_COLORS 3

//
// Buffer stuff
//
struct Buffer {
  char _[BUFFER_LENGTH];
  u_int8_t idx;
} Buffer;

struct Buffer init_buffer() {
  struct Buffer buffer = {._ = {0}, .idx = 0};
  return buffer;
}

void reset_buffer(struct Buffer *buffer) {
  memset(buffer, 0, BUFFER_LENGTH);
  (buffer)->idx = 0;
}

//
// Color stuff
//
enum Color {
  RED,
  GREEN,
  BLUE,
} Color;

enum Color char_to_color(char first_letter) {
  if (first_letter == 'r') {
    return RED;
  } else if (first_letter == 'g') {
    return GREEN;
  } else if (first_letter == 'b') {
    return BLUE;
  } else {
    printf("unknown color first letter: '%c'\n", first_letter);
    exit(1);
  }
}

struct MaxColors {
  u_int32_t red;
  u_int32_t green;
  u_int32_t blue;
} MaxColors;

//
// Game stuff
//
struct Game {
  u_int32_t idx;
  u_int32_t _[NUM_ROUNDS][NUM_COLORS];
} Game;

struct Game init_game() {
  struct Game game = {
      .idx = 0,
  };
  for (u_int32_t round = 0; round < NUM_ROUNDS; round++) {
    for (u_int32_t color = 0; color < NUM_COLORS; color++) {
      game._[round][color] = 0;
    }
  }
  return game;
}

void print_game(struct Game game) {
  printf("Game id: %u\n", game.idx);
  for (u_int8_t round = 0; round < NUM_ROUNDS; round++) {
    for (u_int8_t color = 0; color < NUM_COLORS; color++) {
      printf("%5hhu", game._[round][color]);
    }
    printf("\n");
  }
}

struct MaxColors game_to_max_colors(struct Game game) {
  // this repeated code should be refactored
  struct MaxColors max_colors = {.red = -1, .green = -1, .blue = -1};

  u_int32_t max_color;
  u_int32_t color;

  max_color = 0;
  for (u_int8_t round = 0; round < NUM_ROUNDS; round++) {
    color = game._[round][RED];
    if (color > max_color) {
      max_color = color;
    }
  }
  max_colors.red = max_color;

  max_color = 0;
  for (u_int8_t round = 0; round < NUM_ROUNDS; round++) {
    color = game._[round][GREEN];
    if (color > max_color) {
      max_color = color;
    }
  }
  max_colors.green = max_color;

  max_color = 0;
  for (u_int8_t round = 0; round < NUM_ROUNDS; round++) {
    color = game._[round][BLUE];
    if (color > max_color) {
      max_color = color;
    }
  }
  max_colors.blue = max_color;

  return max_colors;
}

//
// parsing stuff
//
void parse_pull(u_int8_t round, struct Buffer *buffer, struct Game *game) {
  // printf("    ... parsing pull - %s\n", buffer->_);

  char c = buffer->_[buffer->idx++];
  while (c == ' ') {
    c = buffer->_[buffer->idx++];
  }

  // read the integer number of balls
  u_int8_t local_idx = 0;
  char local_buffer[5] = {0};
  while ('0' <= c && c <= '9') {
    local_buffer[local_idx++] = c;
    c = buffer->_[buffer->idx++];
  }

  c = buffer->_[buffer->idx++];
  if (c == ' ') {
    c = buffer->_[buffer->idx++];
  }
  enum Color color = char_to_color(c);

  game->_[round][color] = atoi(local_buffer);
}

void parse_round(u_int8_t round_idx, struct Buffer *buffer, struct Game *game) {
  // printf("  ... parsing round - %s\n", buffer->_);

  char c = buffer->_[buffer->idx++];
  while (c == ' ') {
    c = buffer->_[buffer->idx++];
  }

  while (c != '\0') {
    struct Buffer local_buffer = init_buffer();
    while (c != ',' && c != '\0') {
      local_buffer._[local_buffer.idx++] = c;
      c = buffer->_[buffer->idx++];
    }
    local_buffer.idx = 0;
    parse_pull(round_idx, &local_buffer, game);
    c = buffer->_[buffer->idx++];
  }
}

struct Game parse_game(struct Buffer *buffer) {
  // printf("...parsing game - %s\n", buffer->_);

  struct Game game = init_game();
  struct Buffer local_buffer = init_buffer();

  // grab game id and skip "Game " part
  buffer->idx = strlen("Game ");
  char c = buffer->_[buffer->idx++];

  while (c != ':') {
    local_buffer._[local_buffer.idx++] = c;
    c = buffer->_[buffer->idx++];
  }

  game.idx = atoi(local_buffer._);

  // grab rounds
  buffer->idx += 1; // skip space
  c = buffer->_[buffer->idx++];

  u_int8_t round_idx = 0;
  while (c != '\0') {
    reset_buffer(&local_buffer);

    while (c != ';' && c != '\0') {
      local_buffer._[local_buffer.idx++] = c;
      c = buffer->_[buffer->idx++];
    }
    local_buffer.idx = 0;
    parse_round(round_idx++, &local_buffer, &game);
    c = buffer->_[buffer->idx++];
  }

  return game;
}

size_t part1(char *filename) {
  // open file handle
  FILE *fh = fopen(filename, "r");
  if (fh == NULL) {
    printf("cannot open file\n");
    exit(1);
  }

  struct Buffer buffer = init_buffer();

  struct MaxColors max = {.red = 12, .green = 13, .blue = 14};

  char c;
  u_int32_t sum = 0;
  while ((c = getc(fh)) != EOF) {
    if (c == '\n') {
      buffer.idx = 0;
      struct Game game = parse_game(&buffer);
      struct MaxColors max_colors = game_to_max_colors(game);
      reset_buffer(&buffer);

      if (max_colors.red <= max.red && max_colors.green <= max.green &&
          max_colors.blue <= max.blue) {
        sum += game.idx;
      }

    } else {
      buffer._[buffer.idx++] = c;
    }
  }

  return sum;
}

size_t part2(char *filename) {
  // open file handle
  FILE *fh = fopen(filename, "r");
  if (fh == NULL) {
    printf("cannot open file\n");
    exit(1);
  }

  struct Buffer buffer = init_buffer();

  char c;
  u_int32_t sum = 0;
  while ((c = getc(fh)) != EOF) {
    if (c == '\n') {
      buffer.idx = 0;
      struct Game game = parse_game(&buffer);
      reset_buffer(&buffer);

      struct MaxColors max_colors = game_to_max_colors(game);
      u_int32_t product = max_colors.red * max_colors.green * max_colors.blue;
      sum += product;

      // printf("red: %u, green: %u, blue: %u\n", max_colors.red, max_colors.green,
      //        max_colors.blue);
      // printf("GAME: %u, POWER: %u\n", game.idx, product);
      // print_game(game);

    } else {
      buffer._[buffer.idx++] = c;
    }
  }

  return sum;
}

int main() {
  size_t sum;

  sum = part1("../data/day02_sample.txt");
  assert(sum == 8);
  sum = part1("../data/day02.txt");
  assert(sum == 2256);

  sum = part2("../data/day02_sample.txt");
  assert(sum == 2286);
  sum = part2("../data/day02.txt");
  assert(sum == 74229);

  return 0;
}