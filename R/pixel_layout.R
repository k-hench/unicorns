library(tidyverse)
library(prismatic)
library(colorspace)
library(ggforce)

vlines <- tibble(x  = 0:16)
hlines <- tibble(y  = 0:7)

p_grid <- ggplot() +
    geom_linerange(data = vlines, aes(x = x, ymin = 0, ymax = 7)) +
    geom_linerange(data = hlines, aes(xmin = 0, xmax = 16, y = y)) +
    coord_equal() +
    theme_void()

png_array <- png::readPNG("data/froggy01.png")

x_dim <- 16
y_dim <- 7

png_array[,,1]

png_df <- tibble(idx = 1:(x_dim * y_dim),
                 x = rep(1:x_dim, y_dim),
                 y = rep(1:y_dim, each = x_dim)) |>
    mutate(r = map2_dbl(x, y, \(x,y){png_array[x,y,1]}),
           g = map2_dbl(x, y, \(x,y){png_array[x,y,2]}),
           b = map2_dbl(x, y, \(x,y){png_array[x,y,3]}),
        rgb = rgb(r,g,b)) 

ggplot() +
    geom_raster(data = png_df,
      aes(y = x - .5, x = y -.5, fill = rgb)) +
    geom_linerange(data = hlines, aes(x = y, ymin = 0, ymax = 16), color = rgb(1,1,1,.25)) +
    geom_linerange(data = vlines, aes(xmin = 0, xmax = 7, y = x) , color = rgb(1,1,1,.25)) +
    scale_y_reverse() +
    scale_fill_identity()  +
    coord_equal() +
    theme_void()
