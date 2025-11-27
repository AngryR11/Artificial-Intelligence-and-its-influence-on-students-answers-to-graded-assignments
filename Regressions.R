#source('Regressions_Jaccard_Similarity.R')

rm(list = ls())


# Concatenate the data frames using rbind
combined_df <- read.csv('shuffled_combined_data.csv')

# Run the specified regression models (can replace AI by jaccard_similarity to get the second regression from the paper)
model1 <- lm(favorable ~ AI, data = combined_df)
model2 <- lm(favorable ~ AI + had_pair, data = combined_df)
model3 <- lm(favorable ~ AI + had_pair + average_grade, data = combined_df)
model4 <- lm(favorable ~ AI + had_pair + average_grade + df_fe, data = combined_df)

# Create a summary table
library(stargazer)

stargazer(model1, model2, model3, model4, type = "latex",
          title = "Summary of Regression Models",
          dep.var.labels = "favorable",
          covariate.labels = c("AI", "had pair", "average grade", "Section Dummy"),
          out = "regression_summary_jaccard_similarity.txt")


plot(combined_df$jaccard_similarity,combined_df$AI)
abline(lm(AI ~ jaccard_similarity, data=combined_df))

correlation<-cor(combined_df$AI,combined_df$jaccard_similarity,use="complete.obs")
print(c('correlation: ',correlation))
