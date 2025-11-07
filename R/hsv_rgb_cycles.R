library(tidyverse)

n <- 100
data <- tibble(
  theta = rep(seq(0, 2 * pi, length.out = n), 3),
  y = rep(c(.33, .66, 1), each = n),
  d = rep(rev(c(.85, .95, 1)), each = n),
  x = theta / (2 * pi),
) |>
  mutate(clr = hsv(h = x, s = y, v = d))

data |>
  ggplot(aes(x = x, y = y)) +
  geom_point(aes(color = clr), size = 2.5) +
  scale_color_identity() +
  scale_y_continuous(limits = c(0, 1)) +
  coord_polar()

hsv(1, s = 1, v = 1)

coord_polar()
