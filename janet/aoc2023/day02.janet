
(def parse-game
  '{:prefix (* "Game " (<- :d+) ":")
    :color (+ "red" "green" "blue")
    :ball (* " " (<- :d+) " " (<- :color))
    :pull (* (any (* :ball ",")) :ball)
    :pulls (* (any (sequence :pull (<- ";"))) :pull)
    :main (* :prefix :pulls)})

(def s "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red")

(peg/match parse-game s)
