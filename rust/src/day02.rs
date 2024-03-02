use std::fs;

use pest::{iterators::Pair, Parser};
use pest_derive::Parser;

#[derive(Parser)]
#[grammar = "day02.pest"] // relative to src
struct GameParser;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Pull {
    red: usize,
    green: usize,
    blue: usize,
}

impl<'a> Pull {
    fn from_parser_pull(parser_pull: Pair<'a, Rule>) -> Self {
        let mut pull: Self = Self {
            red: 0,
            green: 0,
            blue: 0,
        };

        for number_and_color in parser_pull.into_inner() {
            let mut inner = number_and_color.into_inner();
            let n = inner.next().unwrap().as_span().as_str().parse::<usize>().unwrap();
            let c = inner.next().unwrap().as_span().as_str();

            match c {
                "red" => pull.red = n,
                "green" => pull.green = n,
                "blue" => pull.blue = n,
                _ => unreachable!(),
            };
        }
        pull
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Game {
    idx: usize,
    pulls: Vec<Pull>,
}

impl<'a> Game {
    fn from_parser_game(game: Pair<'a, Rule>) -> Self {
        let mut game = game.into_inner();
        let game_idx = game.next().unwrap().as_str().parse::<usize>().unwrap();

        Self {
            idx: game_idx,
            pulls: game.map(Pull::from_parser_pull).collect(),
        }
    }
}

pub fn part1(filename: &str) -> usize {
    let unparsed = fs::read_to_string(filename).expect("cannot read file");
    let file = GameParser::parse(Rule::file, &unparsed)
        .expect("cannot parse file")
        .next()
        .unwrap();

    let mut sum: usize = 0;
    for game in file.into_inner() {
        if game.as_str() == "" {
            break;
        }
        let g: Game = Game::from_parser_game(game);

        let max_red: usize = g.pulls.iter().map(|p| p.red).max().unwrap();
        let max_green: usize = g.pulls.iter().map(|p| p.green).max().unwrap();
        let max_blue: usize = g.pulls.iter().map(|p| p.blue).max().unwrap();

        if max_red <= 12 && max_green <= 13 && max_blue <= 14 {
            sum += g.idx;
        }
    }

    sum
}

pub fn part2(filename: &str) -> usize {
    let unparsed = fs::read_to_string(filename).expect("cannot read file");
    let file = GameParser::parse(Rule::file, &unparsed)
        .expect("cannot parse file")
        .next()
        .unwrap();

    let mut sum: usize = 0;
    for game in file.into_inner() {
        if game.as_str() == "" {
            break;
        }
        let g: Game = Game::from_parser_game(game);

        let max_red: usize = g.pulls.iter().map(|p| p.red).max().unwrap();
        let max_green: usize = g.pulls.iter().map(|p| p.green).max().unwrap();
        let max_blue: usize = g.pulls.iter().map(|p| p.blue).max().unwrap();

        sum += max_red * max_green * max_blue;
    }

    sum
}

#[cfg(test)]
mod tests {
    use super::{part1, part2};

    #[test]
    fn test_part1() {
        assert!(part1("../data/day02_sample.txt") == 8);
        assert!(part1("../data/day02.txt") == 2256);
    }

    #[test]
    fn test_part2() {
        assert!(part2("../data/day02_sample.txt") == 2286);
        assert!(part2("../data/day02.txt") == 74229);
    }
}
