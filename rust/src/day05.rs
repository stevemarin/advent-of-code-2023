use std::fs;

#[derive(Debug)]
struct MappingLine {
    source: i32,
    target: i32,
    length: i32,
}

impl From<&str> for MappingLine {
    fn from(value: &str) -> Self {
        let values: Vec<i32> = value
            .split(" ")
            .map(str::parse::<i32>)
            .flatten()
            .collect();
        assert!(values.len() == 3);
        MappingLine {
            source: values[0],
            target: values[1],
            length: values[2],
        }
    }
}

#[derive(Debug)]
struct Mappings {
    lines: Vec<MappingLine>,
}

// humidity-to-location map:
// 60 56 37
// 56 93 4

impl From<&str> for Mappings {
    fn from(value: &str) -> Self {
        let lines = value.split("\n").skip(1);
        let lines: Vec<MappingLine> = lines
            .into_iter()
            .map(str::trim)
            .map(MappingLine::from)
            .collect();
        Mappings { lines }
    }
}

#[derive(Debug)]
struct Maps {
    seeds: Vec<i32>,
    maps: Vec<Mappings>,
}

impl From<&str> for Maps {
    fn from(value: &str) -> Self {
        let mut sections = value.split("\n\n");
        let seeds: Vec<i32> = sections
            .next()
            .unwrap()
            .split(":")
            .last()
            .unwrap()
            .trim()
            .split(" ")
            .map(str::parse::<i32>)
            .flatten()
            .collect();
        let maps: Vec<Mappings> = sections
            .into_iter()
            .map(str::trim)
            .map(Mappings::from)
            .collect();
        Maps { seeds, maps }
    }
}

pub fn part1(filename: &str) -> () {
    let input = &*fs::read_to_string(format!("../data/{filename}")).expect("cannot find file");

    let maps = Maps::from(input);
    println!("{maps:#?}");
}

pub fn part2() {
    todo!();
}

#[cfg(test)]
mod tests {
    use super::{part1, part2};

    #[test]
    fn test_part1() {
        part1("../data/day05_sample.txt");
        assert!(false);
    }

    // #[test]
    // fn test_part2() {
    //     assert!(part2("../data/day04_sample.txt") == Ok(30));
    //     assert!(part2("../data/day04.txt") == Ok(15455663));
    // }
}

// seeds: 79 14 55 13

// seed-to-soil map:
// 50 98 2
// 52 50 48

// soil-to-fertilizer map:
// 0 15 37
// 37 52 2
// 39 0 15

// fertilizer-to-water map:
// 49 53 8
// 0 11 42
// 42 0 7
// 57 7 4

// water-to-light map:
// 88 18 7
// 18 25 70

// light-to-temperature map:
// 45 77 23
// 81 45 19
// 68 64 13

// temperature-to-humidity map:
// 0 69 1
// 1 0 69

// humidity-to-location map:
// 60 56 37
// 56 93 4
