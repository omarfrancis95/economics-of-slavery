library(tidyverse)
library(ggrepel)

df_1790 <- read_csv("1790 census data on slavery.csv")
df_1860 <- read_csv("1860 census data on slavery.csv")
colnames(df_1790)
colnames(df_1860)

df_1790 <- df_1790 %>%
  mutate(
    slaves_per_capita = non_white_slave / state_population,
    year = 1790
  )

df_1860 <- df_1860 %>%
  mutate(
    slaves_per_capita = total_enslaved / state_population,
    year = 1860
  )

df <- bind_rows(df_1790, df_1860)

df <- df %>%
  mutate(year_dummy = ifelse(year == 1860, 1, 0))

model_time <- lm(slaves_per_capita ~ year_dummy, data = df)
summary(model_time)


model_state <- lm(slaves_per_capita ~ year_dummy + STATE, data = df)
summary(model_state)

model_interaction <- lm(slaves_per_capita ~ year_dummy * STATE, data = df)
summary(model_interaction)


df <- df %>%
  mutate(
    highlight = ifelse(
      STATE %in% c("South Carolina", "Georgia", "Virginia",
                   "Alabama", "Mississippi",
                   "New York", "Pennsylvania", "Massachusetts"),
      STATE,
      "Other"
    )
  )

top5_states <- df %>%
  select(STATE, year, slaves_per_capita) %>%
  pivot_wider(
    names_from = year,
    values_from = slaves_per_capita
  ) %>%
  mutate(change = `1860` - `1790`) %>%
  arrange(desc(change)) %>%
  slice(1:5) %>%
  pull(STATE)

df_plot <- df %>%
  mutate(highlight = ifelse(STATE %in% top5_states, STATE, "Other"))

# 3) Plot
ggplot(df_plot, aes(x = year, y = slaves_per_capita, group = STATE)) +
  geom_line(color = "gray", alpha = 0.3) +
  geom_point(color = "gray", alpha = 0.3) +
  
  geom_line(
    data = df_plot %>% filter(highlight != "Other"),
    aes(color = highlight),
    linewidth = 1.2
  ) +
  geom_point(
    data = df_plot %>% filter(highlight != "Other"),
    aes(color = highlight),
    size = 3
  ) +
  
  geom_text_repel(
    data = df_plot %>% filter(year == 1860, highlight != "Other"),
    aes(label = STATE, color = highlight),
    size = 4,
    nudge_x = 5,
    direction = "y",
    box.padding = 0.5,
    point.padding = 0.3,
    segment.color = "gray50"
  ) +
  
  labs(
    title = "Top 5 State changes in Slavery Intensity (1790–1860)",
    subtitle = "States ranked by change in slaves per capita",
    x = "Year",
    y = "Slaves per Capita",
    color = "Top 5 States"
  ) +
  theme_minimal() +
  xlim(1790, 1870)
