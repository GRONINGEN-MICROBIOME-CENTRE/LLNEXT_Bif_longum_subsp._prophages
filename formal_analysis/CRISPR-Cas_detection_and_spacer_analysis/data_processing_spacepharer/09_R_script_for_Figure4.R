# Load required libraries
library(tidyverse)
library(cowplot)

# Load input
tsv_file <- "STS_with_function_with_subtype.tsv"
raw <- read_tsv(tsv_file, show_col_types = FALSE)

# ─────────────────────────────────────────────────────
# PANEL A
# Bar chart of Phage_target_function
fun_cols <- c(
  "Nucleotide Metabolism"        = "#f000ff",
  "Connector"                    = "#5A5A5A",
  "Head and Packaging"           = "#ff008d",
  "Integration and Excision"     = "#E0B0FF",
  "Lysis"                        = "#001eff",
  "Moron, AMG and Host Takeover" = "#8900ff",
  "Other"                        = "#4deeea",
  "Tail"                         = "#74ee15",
  "Transcription Regulation"     = "#ffe700",
  "Unknown Function"             = "#AAAAAA",
  "No match"                     = "#000000"
)

fun_df <- raw %>%
  filter(Match_context != "Intergenic") %>%
  mutate(Function_grp = case_when(
    str_detect(tolower(Phage_target_function), "dna|nucleotide")        ~ "Nucleotide Metabolism",
    str_detect(tolower(Phage_target_function), "connector")             ~ "Connector",
    str_detect(tolower(Phage_target_function), "head|packaging")        ~ "Head and Packaging",
    str_detect(tolower(Phage_target_function), "integration|excision")  ~ "Integration and Excision",
    str_detect(tolower(Phage_target_function), "lysis")                 ~ "Lysis",
    str_detect(tolower(Phage_target_function), "moron|auxiliary|host")  ~ "Moron, AMG and Host Takeover",
    str_detect(tolower(Phage_target_function), "tail")                  ~ "Tail",
    str_detect(tolower(Phage_target_function), "transcription")         ~ "Transcription Regulation",
    str_detect(tolower(Phage_target_function), "^unknown")              ~ "Unknown Function",
    is.na(Phage_target_function)                                        ~ "No match",
    TRUE                                                                ~ "Other"
  )) %>%
  count(Function_grp, Match_context, name = "n") %>%
  arrange(desc(n))

p_fun <- ggplot(fun_df,
                aes(x = reorder(Function_grp, n), y = n, fill = Function_grp)) +
  geom_col(width = 0.7, position = "dodge") +
  geom_text(aes(label = n),
            position = position_dodge(width = 0.7),
            hjust = -0.2,
            size = 3.5) +
  scale_fill_manual(values = fun_cols, guide = "none") +
  scale_y_continuous(
    breaks = c(250, 500, 750, 1000),
    limits = c(0, 1125),
    expand = c(0, 0)
  ) +
  facet_wrap(~ Match_context) +
  coord_flip() +
  labs(
    x = "Target Function",
    y = "No. of Spacer Matches",
    title = "Spacer Matches by Phage Target Function"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title  = element_text(size = 14),
    plot.margin = margin(5, 40, 5, 5)
  )

ggsave("panelA_function_by_context.pdf", p_fun, width = 8, height = 6)

# ─────────────────────────────────────────────────────
# PANEL B
# CRISPR_subtype_updated bar chart

subtype_df <- raw %>%
  mutate(CRISPR_subtype_updated = replace_na(CRISPR_subtype_updated, "Unknown")) %>%
  count(CRISPR_subtype_updated, name = "n") %>%
  arrange(desc(n))

p_sub <- ggplot(subtype_df,
                aes(x = reorder(CRISPR_subtype_updated, n),
                    y = n,
                    fill = CRISPR_subtype_updated)) +
  geom_col(width = 0.7) +
  geom_text(aes(label = n), hjust = -0.2, size = 3.5) +
  scale_fill_viridis_d(option = "C", guide = "none") +
  scale_y_continuous(limits = c(0, 2000), expand = c(0, 0)) +
  coord_flip(expand = TRUE) +
  labs(
    x = "CRISPR-Cas Subtype",
    y = "No. of Spacer Matches",
    title = "Spacer Counts by CRISPR Subtype"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title  = element_text(size = 14),
    plot.margin = margin(5, 40, 5, 5)
  )

ggsave("panelB_crispr_subtype_counts.pdf", p_sub, width = 8, height = 6)

# ─────────────────────────────────────────────────────
# COMBINED – ONLY Panels A and B
combo_AB <- plot_grid(
  p_fun, p_sub,
  labels = c("A", "B"),
  ncol = 2,
  rel_widths = c(1, 1)
)

ggsave("figure_combined_panels_AB.pdf", combo_AB, width = 16, height = 8)

message("Outputs: panelA_function_by_context.pdf, panelB_crispr_subtype_counts.pdf, figure_combined_panels_AB.pdf")
