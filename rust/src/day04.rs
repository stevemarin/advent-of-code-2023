use std::{collections::HashSet, fs, hash::Hash, num::ParseIntError};

use pest::{iterators::Pairs, Parser};
use pest_derive::Parser;

const MAX_CARD_ID: usize = 202;

#[derive(Parser)]
#[grammar = "day04.pest"] // relative to src
struct CardParser;

fn extract_numbers(pair_iter: &mut Pairs<Rule>) -> Vec<i32> {
    let numbers: Vec<i32> = pair_iter
        .next()
        .expect("no winning numbers")
        .into_inner()
        .map(|v| v.as_str().parse::<i32>())
        .flatten()
        .collect();
    numbers
}

pub fn part1(filename: &str) -> Result<usize, ParseIntError> {
    let unparsed = fs::read_to_string(filename).expect("cannot read file");
    let mut pairs = CardParser::parse(Rule::cards, &unparsed)
        .expect("cannot parse file")
        .into_iter();

    let mut sum: usize = 0;
    while let Some(item) = pairs.next() {
        if item.as_str() == "" {
            continue;
        }

        let _idx = item.as_str().parse::<usize>()?;

        let winning_numbers: HashSet<i32> = extract_numbers(&mut pairs).into_iter().collect();
        let card_numbers: HashSet<i32> = extract_numbers(&mut pairs).into_iter().collect();
        let num_winners = winning_numbers.intersection(&card_numbers).count();

        let score = match num_winners {
            0 => 0,
            1 => 1,
            c => 2_usize.pow((c as u32) - 1),
        };
        sum += score;
    }

    Ok(sum)
}

pub fn part2(filename: &str) -> Result<usize, ParseIntError> {
    let unparsed = fs::read_to_string(filename).expect("cannot read file");
    let mut pairs = CardParser::parse(Rule::cards, &unparsed)
        .expect("cannot parse file")
        .into_iter();

    let mut sum: usize = 0;
    let mut num_cards: [usize; MAX_CARD_ID + 1] = [0; MAX_CARD_ID + 1];

    while let Some(item) = pairs.next() {
        if item.as_str() == "" {
            continue;
        }

        let idx = item.as_str().parse::<usize>()?;
        num_cards[idx] += 1;

        let current_num_cards = num_cards[idx];

        let winning_numbers: HashSet<i32> = extract_numbers(&mut pairs).into_iter().collect();
        let card_numbers: HashSet<i32> = extract_numbers(&mut pairs).into_iter().collect();
        let num_winners = winning_numbers.intersection(&card_numbers).count();

        for i in (idx + 1)..(idx + 1 + num_winners) {
            num_cards[i] += current_num_cards;
        }

        sum += current_num_cards;
    }

    println!("NUM_CARDS: {num_cards:?}");

    Ok(sum)
}

#[cfg(test)]
mod tests {
    use super::{part1, part2};

    #[test]
    fn test_part1() {
        assert!(part1("../data/day04_sample.txt") == Ok(13));
        assert!(part1("../data/day04.txt") == Ok(23678));
    }

    #[test]
    fn test_part2() {
        assert!(part2("../data/day04_sample.txt") == Ok(30));
        assert!(part2("../data/day04.txt") == Ok(15455663));
    }
}
