// Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
// Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
// Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
// Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
// Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

use std::fs;

#[derive(Debug, Copy, Clone)]
struct Round {
    red: i32,
    green: i32,
    blue: i32,
}

impl From<String> for Round {
    fn from(value: String) -> Self {
        
    }
}

#[derive(Debug, Clone)]
struct Game {
    id: i32,
    rounds: Vec<Round>,
}

fn read_input(filename: &str) -> Vec<Game> {
    let data_path = format!("../data/{}", filename);
    let input: String = fs::read(data_path)
        .expect("cannot read file")
        .into_iter()
        .map(|x| x as char)
        .collect();

    for line in input.trim().split('\n') {
        println!("line: {:?}", line);
    }

    vec![]
}

#[cfg(test)]
mod tests {
    use super::read_input;

    #[test]
    fn test_part1() {
        read_input("day02_sample.txt");
    }
}
