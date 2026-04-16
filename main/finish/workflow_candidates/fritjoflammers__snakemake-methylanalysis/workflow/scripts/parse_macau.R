########################
####### Model 1 ########
########################
files <- list.files("./results/macau_output/", pattern = "model1")[grep(x = list.files(path = "./results/macau_output/", pattern = "model1"), pattern = "w_cell_type", invert = T)]

out <- read.table(paste("./results/macau_output/", files[1], sep = ""), header = T)
for (f in 2:length(files)) {
  temp <- read.table(paste("./results/macau_output/", files[f], sep = ""), header = T)
  out2 <- rbind.data.frame(out, temp)
  out <- out2
  rm(out2)
}

# Calculating p-values from MACAU

# get beta values (col4) and alpha value for each predictor (that is every second column starting from col 11)
beta <- cbind.data.frame(out[, seq(11, dim(out)[2], 2)], out[, 4])

# do the same for standard errors (col5)
se_beta <- cbind.data.frame(out[, seq(12, dim(out)[2], 2)], out[, 5])
# calculate bhat
# bhat is beta divided by the square root of 1 minus the square of the standard error
# bhat signifies the effect size of the predictor, it stands for the number of standard deviations the predictor is away from 0
# bhat is the z-score of the predictor
bhat <- as.matrix(beta / (1 - se_beta^2))
# calculate bse
# bse is the standard error of the beta value
# it is calculated by dividing the standard error of the beta value by the square root of 1 minus the square of the standard error
bse <- as.matrix(se_beta / sqrt(1 - se_beta^2))
# calculate p-value using pchisq
# pchisq is the probability of the chi-square distribution
# it is calculated by taking the square of the bhat value divided by the square of the bse value
# the p-value is calculated by taking 1 minus the probability of the chi-square distribution
pvalue <- 1 - pchisq((bhat / bse)^2, 1)

colnames(pvalue) <- c(
  "intercept", "mol_ecol_dark", "mol_ecol_non_dark", "new_batch",
  "november", "drrbs", "r21", "mapped_reads",
  "bscr", "habitat_quality", "cumulative", "male_rank", "female_rank", "age"
)


# Store the necessary outputs -- Habitat quality, male rank, and female rank effects
results_model1 <- cbind.data.frame(bhat[, c(10, 11, 12, 13, 14)], se_beta[, c(10, 11, 12, 13, 14)], pvalue[, c(10, 11, 12, 13, 14)])
colnames(results_model1) <- apply(expand.grid(colnames(pvalue)[c(10, 11, 12, 13, 14)], c("bhat", "se_beta", "pvalue")), 1, paste, collapse = "_")
rownames(results_model1) <- out$id
