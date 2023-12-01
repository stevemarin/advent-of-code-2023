use std::fs;


fn read_input(filename: &str) -> Vec<u8> {
    let data_path = format!("../../data/{}", filename);
    let input = fs::read(data_path).expect("cannot read file");
    input
}

fn part1(filename: &str) -> i32 {
    let input = read_input(filename);

    5
}

#[cfg(test)]
mod tests {
    use super::part1;


    #[test]
    fn it_works() {
        assert!(part1("day01_part1_sample.txt") == 142)
            }
}