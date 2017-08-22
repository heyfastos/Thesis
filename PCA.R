# Required packs
install.packages("FactoMineR")
install.packages("devtools")
devtools::install_github("kassambara/factoextra")
library("FactoMineR")
library("factoextra")

#setwd(dir = "C:/Users/tricho/Desktop/science/PhD/Crete/PCA")

# Upload
InputTab <- read.csv(file = "PCA_table_Samples_are_lines.txt")
D=InputTab
View(D)

Treatment = D$Taxon
D=`row.names<-`(D,Treatment)

# Extract active variables/individuals for PCA
PCAD <- D[1:18, 2:219]
#View(Env.mtx)
View(PCAD)

### Principal component analysis using FactoMineR
head(PCAD[, 1:200])
res.pca <- PCA(PCAD, graph = TRUE)
print(res.pca)

#### Interpreting PCA
#Variances of the principal components
eigenvalues <- res.pca$eig
head(eigenvalues[,])

#The importance of PCs can be visualized using a scree plot :
library("factoextra")
fviz_screeplot(res.pca, ncp=10)
### Plot the correlations/loadings of the variables with the components
# Coordinates of variables
head(res.pca$var$coord)
# Visualization of the variables on the factor map :
fviz_pca_var(res.pca, select.var = list(contrib = 5))  # Correlation circle can help to visualize the most correlated variables (i.e, variables that group together).

## Cos2 : quality of the representation for variables on the factor map
head(res.pca$var$cos2)
fviz_pca_var(res.pca, col.var="cos2", select.var = list(cos2 = 0.6)) +
  scale_color_gradient2(low="white", mid="blue", 
                        high="red", midpoint=0.5) + theme_minimal()


#Filtering results- select.var.

#The contribution of variables can be extracted as follow :
head(res.pca$var$contrib)
# Contributions of variables on PC1
fviz_contrib(res.pca, choice = "var", axes = 1)
# Contributions of variables on PC2
fviz_contrib(res.pca, choice = "var", axes = 2)
# Total contribution on PC1 and PC2
fviz_contrib(res.pca, choice = "var", axes = 1:2)
# Control variable colors using their contributions
fviz_pca_var(res.pca, col.var="contrib")
# Change the gradient color
fviz_pca_var(res.pca, col.var="contrib", select.var= list(cos2 = 10), repel = TRUE) +
  scale_color_gradient2(low="white", mid="blue", 
                        high="red", midpoint=0.9) + theme_minimal()

#identify the most correlated variables with a given principal component.
dimdesc(res.pca, axes = 1:3, proba = 0.05)
#res : an object of class PCA
#axes : a numeric vector specifying the dimensions to be described
#prob : the significance level
res.desc <- dimdesc(res.pca, axes = c(1,2))
# Description of dimension 1
res.desc$Dim.1
# Description of dimension 2
res.desc$Dim.2

#Graph of individuals
head(res.pca$ind$coord)
fviz_pca_ind(res.pca)
head(res.pca$ind$cos2)
fviz_pca_ind(res.pca, col.ind="cos2") +
  scale_color_gradient2(low="lightblue", mid="blue", 
                        high="red", midpoint=0.3) + theme_minimal()
#Contribution of the individuals to the princial components
head(res.pca$ind$contrib)
# Contributions of individuals to PC1
fviz_contrib(res.pca, choice = "ind", axes = 1)
# Contributions of the individuals to PC2
fviz_contrib(res.pca, choice = "ind", axes = 2)
# Total contribution on PC1 and PC2
fviz_contrib(res.pca, choice = "ind", axes = 1:2)
# Change the gradient color
fviz_pca_ind(res.pca, col.ind="contrib") +
  scale_color_gradient2(low="lightblue", mid="blue", 
                        high="red", midpoint=5) + theme_minimal()
