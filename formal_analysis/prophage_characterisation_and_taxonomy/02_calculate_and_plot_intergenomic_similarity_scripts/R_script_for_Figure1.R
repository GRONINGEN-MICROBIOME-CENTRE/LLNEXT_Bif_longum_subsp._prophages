# --------------------------------------------
# Packages
# --------------------------------------------
library(readr)
library(heatmap3)
library(grid)
library(ComplexHeatmap)

# --------------------------------------------
# Inputs / Outputs
# --------------------------------------------
ani_path <- "completed_ani_matrix.csv"
meta_path <- "metadata_file.tsv"
pdf_out  <- "ani_heatmap.pdf"

# --------------------------------------------
# Load ANI matrix
# --------------------------------------------
ani_matrix <- read.csv(ani_path, header = TRUE, row.names = 1, check.names = FALSE)
ani_matrix <- as.matrix(ani_matrix)

# --------------------------------------------
# Load metadata
# --------------------------------------------
metadata <- read_tsv(meta_path, show_col_types = FALSE, na = character())

# --------------------------------------------
# Align metadata to matrix row order
# --------------------------------------------
metadata <- metadata[metadata$Prophage %in% rownames(ani_matrix), ]
metadata <- metadata[match(rownames(ani_matrix), metadata$Prophage), ]
stopifnot(identical(metadata$Prophage, rownames(ani_matrix)))

# --------------------------------------------
# Heatmap color gradient
# --------------------------------------------
breaks <- seq(min(ani_matrix, na.rm = TRUE), 100, length.out = 100)
hm.colors <- colorRampPalette(c("white", "navy"))(length(breaks) - 1)

# --------------------------------------------
# Row color strips (NO FAMILY)
# --------------------------------------------
to_na_str <- function(x) {
  x2 <- x
  x2[is.na(x2) | x2 == ""] <- "NA"
  x2
}

# Subspecies
subspecies_colors <- metadata$hex_code_subsp
names(subspecies_colors) <- metadata$Prophage
subsp_map <- unique(metadata[, c("subsp_cluster", "hex_code_subsp")])
subsp_map <- subsp_map[!duplicated(subsp_map$subsp_cluster), ]
subsp_legend_labels <- subsp_map$subsp_cluster
subsp_legend_cols   <- subsp_map$hex_code_subsp

# Feeding mode (complex)
set.seed(43)
ffq_complex_vals <- to_na_str(metadata$infant_ffq_feeding_mode_complex)
uniq_ffq_complex <- unique(ffq_complex_vals)
ffq_complex_pool <- sample(colors(), length(uniq_ffq_complex))
ffq_complex_map  <- setNames(ffq_complex_pool, uniq_ffq_complex)
if ("NA" %in% names(ffq_complex_map)) ffq_complex_map["NA"] <- "grey"
ffq_complex_colors <- unname(ffq_complex_map[ffq_complex_vals])
names(ffq_complex_colors) <- metadata$Prophage

# Birth mode
set.seed(44)
birth_mode_vals <- to_na_str(metadata$birth_deliverybirthcard_mode_binary)
uniq_birth_mode <- unique(birth_mode_vals)
birth_mode_pool <- sample(colors(), length(uniq_birth_mode))
birth_mode_map  <- setNames(birth_mode_pool, uniq_birth_mode)
if ("NA" %in% names(birth_mode_map)) birth_mode_map["NA"] <- "grey"
birth_mode_colors <- unname(birth_mode_map[birth_mode_vals])
names(birth_mode_colors) <- metadata$Prophage

# Combine ONLY Subspecies, Feeding, Birth (NO FAMILY)
row_colors <- cbind(
  Subspecies = subspecies_colors,
  `Feeding (complex)` = ffq_complex_colors,
  `Birth mode` = birth_mode_colors
)

# --------------------------------------------
# Legends
# --------------------------------------------
legend_title_gp  <- gpar(fontsize = 16, fontface = "bold")
legend_labels_gp <- gpar(fontsize = 12)

lg_subsp <- Legend(
  at = subsp_legend_labels,
  legend_gp = gpar(fill = subsp_legend_cols),
  title = "Subspecies",
  title_gp = legend_title_gp,
  labels_gp = legend_labels_gp,
  labels_rot = 45,
  legend_height = unit(8, "cm")
)

lg_ffq <- Legend(
  at = names(ffq_complex_map),
  legend_gp = gpar(fill = unname(ffq_complex_map)),
  title = "Feeding (complex)",
  title_gp = legend_title_gp,
  labels_gp = legend_labels_gp,
  labels_rot = 45,
  legend_height = unit(8, "cm")
)

lg_birth <- Legend(
  at = names(birth_mode_map),
  legend_gp = gpar(fill = unname(birth_mode_map)),
  title = "Birth mode (binary)",
  title_gp = legend_title_gp,
  labels_gp = legend_labels_gp,
  labels_rot = 45,
  legend_height = unit(8, "cm")
)

combined_legend <- packLegend(lg_subsp, lg_ffq, lg_birth, direction = "vertical")

# --------------------------------------------
# Plot to PDF
# --------------------------------------------
pdf(pdf_out, width = 18, height = 14)

layout(matrix(c(1, 2), nrow = 1), widths = c(4.5, 2.5))

par(oma = c(4, 1, 1, 1))

heatmap3(
  ani_matrix,
  scale = "none",
  trace = "none",
  col = hm.colors,
  cexRow = 0.5,
  cexCol = 0.5,
  key = TRUE,
  key.title = NA,
  key.xlab = "ANI",
  dendrogram = "both",
  Rowv = TRUE,
  Colv = TRUE,
  symm = TRUE,
  density.info = "none",
  RowSideColors = row_colors
)

pushViewport(viewport(layout = grid.layout(1, 1)))
pushViewport(viewport(layout.pos.row = 1))
draw(combined_legend, x = unit(1, "npc") - unit(10, "mm"), just = "right")
popViewport(2)

dev.off()

cat("Wrote heatmap:", pdf_out, "\n")
