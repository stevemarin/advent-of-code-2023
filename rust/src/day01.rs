use std::{char, fs};

fn read_input(filename: &str) -> Vec<char> {
    let data_path = format!("../data/{}", filename);
    let input = fs::read(data_path).expect("cannot read file");
    let input: Vec<char> = input.into_iter().map(|x| x as char).collect();
    input
}

fn extract_digits_part1(chars: &[char]) -> i32 {
    let x: Vec<&char> = chars.iter().filter(|x| (x.is_ascii_digit())).collect();

    let s = format!("{}{}", x.first().unwrap(), x.last().unwrap());
    s.parse::<i32>().unwrap()
}

pub fn part1(filename: &str) -> i32 {
    let input = read_input(filename);
    input
        .split(|&x| x == '\n')
        .map(|x| match x {
            [] => 0_i32,
            l => extract_digits_part1(l),
        })
        .sum()
}

fn extract_digits_part2(chars: &[char]) -> i32 {
    let num_chars = chars.len();
    let digits: Vec<Option<i32>> = chars
        .iter()
        .enumerate()
        .map(|(idx, c)| match c {
            c if c.is_ascii_digit() => {
                let d: Option<u32> = c.to_digit(10);
                d.map(|x| x as i32)
            }
            'o' => {
                if (idx + 3 <= num_chars) && chars[idx..idx + 3] == ['o', 'n', 'e'] {
                    Some(1)
                } else {
                    None
                }
            }
            't' => {
                if (idx + 3 <= num_chars) && chars[idx..idx + 3] == ['t', 'w', 'o'] {
                    Some(2)
                } else if (idx + 5 <= num_chars) && chars[idx..idx + 5] == ['t', 'h', 'r', 'e', 'e'] {
                    Some(3)
                } else {
                    None
                }
            }
            'f' => {
                if (idx + 4 <= num_chars) && chars[idx..idx + 4] == ['f', 'o', 'u', 'r'] {
                    Some(4)
                } else if (idx + 4 <= num_chars) && chars[idx..idx + 4] == ['f', 'i', 'v', 'e'] {
                    Some(5)
                } else {
                    None
                }
            }
            's' => {
                if (idx + 3 <= num_chars) && chars[idx..idx + 3] == ['s', 'i', 'x'] {
                    Some(6)
                } else if (idx + 5 <= num_chars) && chars[idx..idx + 5] == ['s', 'e', 'v', 'e', 'n'] {
                    Some(7)
                } else {
                    None
                }
            }
            'e' => {
                if (idx + 5 <= num_chars) && chars[idx..idx + 5] == ['e', 'i', 'g', 'h', 't'] {
                    Some(8)
                } else {
                    None
                }
            }
            'n' => {
                if (idx + 4 <= num_chars) && chars[idx..idx + 4] == ['n', 'i', 'n', 'e'] {
                    Some(9)
                } else {
                    None
                }
            }
            _ => None,
        })
        .collect();

    let d: Vec<i32> = digits
        .into_iter()
        .filter(|x| !x.is_none())
        .map(|x| x.unwrap())
        .collect();
    let as_string = format!("{}{}", d.first().unwrap(), d.last().unwrap());
    let x = as_string.as_str().parse::<i32>().unwrap();
    x
}

pub fn part2(filename: &str) -> i32 {
    let input = read_input(filename);
    input
        .split(|&x| x == '\n')
        .map(|x| match x {
            [] => 0_i32,
            l => extract_digits_part2(l),
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::{part1, part2};

    #[test]
    fn test_part1() {
        assert!(part1("day01_part1_sample.txt") == 142);
        assert!(part1("day01.txt") == 54968);
    }

    #[test]
    fn test_part2() {
        assert!(part2("day01_part2_sample.txt") == 281);
        assert!(part2("day01.txt") == 54094);
    }
}
