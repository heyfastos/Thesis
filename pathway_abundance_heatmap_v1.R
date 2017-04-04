setwd("C:/PATH/TO/WORKING/DIRECTORY")

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

#the pathways "relative abundance" table (the % or reads assigned to a pathway out of all reads assigned to the taxon)
# should have the following format:
#header line: Pathawy \t sample1 \t sample2 \t sample3 ...
# name of pathways \t % out of sample1 reads \t % out of sample2 reads (and so on)

# read in raw abundance table
KEGG_PW_AbundanceTable <- read.csv(file = "NAME_OF_PATHWAYS_TABLE.tab", row.names = 1, stringsAsFactors = F, 
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

# increasing the max_value variable may result in stronger shades of color, play with the last argument in the 
# "makeColorRampPalette" function to adjust the sensitivity /resolution of the colors in the heatmap

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

