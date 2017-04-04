setwd("C:/Users/tricho/Desktop/science/PhD/Eilat_summerCruise_2012/Analysis/04_selected_KOs_and_pathways/KASS/Prochlorococcus/new/heatmaps/")

source("http://bioconductor.org/biocLite.R")


if (!require("RColorBrewer")){
  install.packages("RColorBrewer", dependencies = TRUE)
  library(RColorBrewer)
}

if (!require("gplots")){
  install.packages("gplots", dependencies = TRUE)
  library(RColorBrewer)
}

if (!require("pheatmap")){
  install.packages("pheatmap", dependencies = TRUE)
  library("pheatmap")
}



# read in raw abundance table
KEGG_PW_AbundanceTable <- read.csv(file = "merged_pro_table.tab", row.names = 1, stringsAsFactors = F, 
                               header = TRUE, sep = "\t", comment.char = "#")
head(KEGG_PW_AbundanceTable)
nrow(KEGG_PW_AbundanceTable)

# filter out lowly expressed
#keep <- rowSums(MEROPSAbundanceTable) >=2
#sum(keep)
#MEROPSAbundanceTable <- MEROPSAbundanceTable[keep, ]

KEGG_PW_AbundanceMatrix <- as.matrix(KEGG_PW_AbundanceTable)
rownames(KEGG_PW_AbundanceMatrix)
colnames(KEGG_PW_AbundanceMatrix)
# ------------------
#   plot
# ------------------
col <- brewer.pal(9, "Blues")
#col <- colorRampPalette(c("navy", "white", "firebrick3"))(50)

makeColorRampPalette <- function(colors, cutoff.fraction, num.colors.in.palette)
{
  stopifnot(length(colors) == 4)
  ramp1 <- colorRampPalette(colors[1:2])(num.colors.in.palette * cutoff.fraction)
  ramp2 <- colorRampPalette(colors[3:4])(num.colors.in.palette * (1 - cutoff.fraction))
  return(c(ramp1, ramp2))
}



cutoff_value <- 10
#max_value <- max(MEROPSAbundanceMatrix)
max_value <- 60
cutoff.fraction <- cutoff_value/max_value

cols <- makeColorRampPalette(c("white", "lightblue",    # distances 0 to 3 colored from white to red
                               "skyblue", "royalblue"), # distances 3 to max(distmat) colored from green to black
                             cutoff.fraction,
                             100)


NrRows <- nrow(KEGG_PW_AbundanceMatrix)
NrRows
pdf("Pro_pheatmap_v4.pdf", onefile = F, width=9, height=NrRows/5)
pheatmap(mat = KEGG_PW_AbundanceMatrix,
         cluster_cols = F,
         #cluster_rows = F,
         fontsize_row = 8, 
         fontsize_col = 8,  
         treeheight_col = 50, 
         color = cols, 
         cellwidth = 20, 
         cellheight = 10, 
         #filename = "test.pdf",
         labels_row = rownames(KEGG_PW_AbundanceMatrix))
dev.off()

