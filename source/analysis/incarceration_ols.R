# Reproduce the conventional OLS summary in Incarceration_Regression.ipynb.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) {
  stop("Usage: Rscript incarceration_ols.R INPUT_CSV OUTPUT_CSV")
}

incar_df <- read.csv(args[1], check.names = FALSE)
incar_df$treated <- as.integer(incar_df$STATE == "California")
incar_df$post1994 <- as.integer(incar_df$Year >= 1994)
incar_df <- incar_df[!is.na(incar_df[["Total People Incarcerated"]]), ]

model_incar <- lm(
  `Total People Incarcerated` ~ post1994 + treated + post1994:treated,
  data = incar_df
)
coefs <- coef(summary(model_incar))
table <- data.frame(
  term = rownames(coefs),
  estimate = coefs[, 1],
  standard_error = coefs[, 2],
  p_value = coefs[, 4],
  observations = nobs(model_incar)
)
dir.create(dirname(args[2]), recursive = TRUE, showWarnings = FALSE)
write.csv(table, args[2], row.names = FALSE)
