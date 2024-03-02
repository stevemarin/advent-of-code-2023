use std::{collections::HashMap, fs};

fn read_input(filename: &str) -> Vec<Vec<char>> {
    let path = format!("../data/{}", filename);
    let data = String::from_utf8(fs::read(path).expect("cannot read file"))
        .expect("cannot convert to string");

    data.trim()
        .split('\n')
        .map(|x| x.chars().collect::<Vec<char>>())
        .collect::<Vec<Vec<char>>>()
}

fn extract_numbers_from_row(arr: &Vec<char>, row: usize) -> Vec<((usize, usize, usize), usize)> {
    let mut idx: usize = 0;
    let mut length: usize = 0;
    let mut locations: Vec<(usize, usize)> = vec![];

    loop {
        let maybe_c = arr.get(idx);
        match maybe_c {
            Some(c) if c.is_ascii_digit() => length += 1,
            Some(_) if length > 0 => {
                locations.push((idx - length, idx));
                length = 0;
            }
            None if length > 0 => {
                locations.push((idx - length, idx));
                break;
            }
            None => break,
            _ => (),
        }
        idx += 1;
    }

    let numbers = locations
        .into_iter()
        .map(|(start, stop)| {
            let value: usize = arr[start..stop]
                .into_iter()
                .collect::<String>()
                .parse()
                .expect("cannot parse into usize");
            ((row, start, stop - 1), value)
        })
        .collect();

    numbers
}

pub fn part1(filename: &str) -> usize {
    let input = read_input(filename);
    let num_rows = input.len();
    let num_cols = input[0].len();

    let symbols: HashMap<(usize, usize), char> = (0..num_rows)
        .flat_map(|row| (0..num_cols).map(move |col| (row, col)))
        .filter_map(
            |(row, col)| match *input.get(row).unwrap().get(col).unwrap() {
                c if c.is_ascii_digit() || c == '.' => None,
                c => Some(((row, col), c)),
            },
        )
        .collect();

    println!("SYMBOLS: {:?}, {:#?}", symbols.len(), symbols);

    let numbers: Vec<((usize, usize, usize), usize)> = input
        .iter()
        .enumerate()
        .map(|(row, arr)| extract_numbers_from_row(arr, row))
        .flatten()
        .collect();

    println!("NUMBERS: {:?}, {:#?}", numbers.len(), numbers);

    let mut sum = 0;
    'number_loop: for ((row, col_start, col_stop), value) in numbers.iter() {
        let start_row = 0.max((*row as i64) - 1) as usize;
        let stop_row = (num_rows - 1).min(*row + 1);
        for current_row in start_row..=stop_row {
            let start_col = 0.max((*col_start as i64) - 1) as usize;
            let stop_col = (num_cols - 1).min(*col_stop + 1);
            for current_col in start_col..=stop_col {
                if symbols.contains_key(&(current_row, current_col)) {
                    sum += value;
                    continue 'number_loop;
                }
            }
        }
    }
    sum
}

pub fn part2(filename: &str) -> usize {
    let input = read_input(filename);
    let num_rows = input.len();
    let num_cols = input[0].len();

    let symbols: HashMap<(usize, usize), char> = (0..num_rows)
        .flat_map(|row| (0..num_cols).map(move |col| (row, col)))
        .filter_map(
            |(row, col)| match *input.get(row).unwrap().get(col).unwrap() {
                c if c == '*' => Some(((row, col), c)),
                _ => None,
            },
        )
        .collect();

    println!("SYMBOLS: {:?}, {:#?}", symbols.len(), symbols);

    let numbers: Vec<((usize, usize, usize), usize)> = input
        .iter()
        .enumerate()
        .map(|(row, arr)| extract_numbers_from_row(arr, row))
        .flatten()
        .collect();

    println!("NUMBERS: {:?}, {:#?}", numbers.len(), numbers);

    let mut sum = 0;
    'symbol_loop: for (symbol_row, symbol_col) in symbols.keys() {
        let mut prod = 1;
        let mut num_found = 0;
        for ((num_row, num_col_start, num_col_stop), value) in numbers.iter() {
            let col_start = 0.max((*num_col_start as i64) - 1) as usize;
            let col_stop = (num_cols - 1).min(num_col_stop + 1);

            if symbol_row.abs_diff(*num_row) <= 1
                && col_start <= *symbol_col
                && *symbol_col <= col_stop
            {
                num_found += 1;
                prod *= value;
            }

            if num_found == 2 {
                sum += prod;
                continue 'symbol_loop;
            }
        }
    }
    sum
}

#[cfg(test)]
mod tests {
    use super::{part1, part2};

    #[test]
    fn test_part1() {
        assert!(part1("../data/day03_sample.txt") == 4361);
        assert!(part1("../data/day03.txt") == 537832);
    }

    #[test]
    fn test_part2() {
        assert!(part2("../data/day03_sample.txt") == 467835);
        assert!(part2("../data/day03.txt") == 81939900);
    }
}
