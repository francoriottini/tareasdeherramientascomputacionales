'
Prior to use, install the following packages:
install.packages("ggplot2")
install.packages("tibble")
install.packages("dplyr")
install.packages("gridExtra")
install.packages("Lock5Data")
install.packages("ggthemes")

install.packages("maps")
install.packages("mapproj")
install.packages("corrplot")
install.packages("fun")
install.packages("zoo")

Used datafiles and sources:
a) gapminder.csv - Modified dataset from various datasets available at:
https://www.gapminder.org/data/
b) xAPI-Edu-Data.csv:
https://www.kaggle.com/aljarah/xAPI-Edu-Data/data
c) LoanStats.csv:
Loan Data from Lending Tree - https://www.lendingclub.com/info/download-data.action
d) Lock5Data

'

#Load Libraries
library("ggplot2")
library("tibble")
library("gridExtra")
library("dplyr")
library("Lock5Data")
library("ggthemes")
library("fun")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")
library("ggplot2")
#Set pathname for the directory where you have data
setwd("/Usuarios/Tomas/Documents/1.TOMAS/1.MASTER UDESA/2.2DO TRIMESTRE/Herramientas computacionales/5 DATA VISUALIZATION/Applied-Data-Visualization-with-R-and-ggplot2-master")
#Check working directory
getwd()

#Note: Working directory should be "Beginning-Data-Visualization-with-ggplot2-and-R"

#Load the data files
df <- read.csv("data/gapminder-data.csv")
df2 <- read.csv("data/xAPI-Edu-Data.csv")
df3 <- read.csv("data/LoanStats.csv")

#Summary of the three datasets
str(df)
str(df2)
str(df3)

##Grammar of graphics and visual components
#Subtopic - Layers
#ORIGINAL
p1 <- ggplot(df,aes(x=Electricity_consumption_per_capita))
p2 <- p1+geom_histogram()
p2
p3 <- p1+geom_histogram(bins=15)
p3


#MODIFICADO1
ggplot(df, aes(x = Electricity_consumption_per_capita, fill = Country)) + 
  geom_histogram() 
#MODIFICADO2
ggplot(df, aes(x = Electricity_consumption_per_capita, fill = Country , colour = Country)) + 
  geom_histogram(position = "dodge")

#MODIFICADO3 el que mas me gusto
#Le modificamos poder mirar conjunto los paises y el consumo de electricidad per capita. 
ggplot(df, aes(x = Electricity_consumption_per_capita, fill = Country , colour = Country)) + 
  geom_histogram(colour = "black", lwd = 0.75, linetype = 1, alpha = 0.5, position = "identity")+
  labs(title='Histogram by country', 
     subtitle='Electricity consumption per capita',
     x='Electricity consumption per capita', y='Count')+ 
  theme(axis.title.x = element_text(size=10,color="black",face="bold",angle=0))

#MODIFICADO4prueba
ggplot(df, aes(x = Electricity_consumption_per_capita, fill = Country , colour = Country)) + 
  geom_histogram(colour = "black", lwd = 0.75, linetype = 1, position = "dodge")

#Exercise-Layers
p4 <- p3+xlab("Electricity consumption per capita")
p4

#Exercise- Scales
p1 <- ggplot(df,aes(x=gdp_per_capita))
p2 <- p1+geom_histogram()
p2
#Where does the maximum occur? We need to have a finer labelling to answer
#the question
p2 + scale_x_continuous(breaks=seq(0,40000,4000))


#Topic B: Facet
#Exercise: Using facets to split data
#ORIGINAL
p <- ggplot(df, aes(x=gdp_per_capita, y=Electricity_consumption_per_capita)) + 
  geom_point()
p + facet_grid(Country ~ .) #Horizontally Arranged
p + facet_grid(. ~ Country) #Vertically Arranged
p + facet_wrap(~Country)


#Topic B: Facet
#Exercise: Using facets to split data
#MODIFICADO
#Al grafico anterior le liberamos las escalas, modificamos los labels y le pusimos titulos y demas :).
p <- ggplot(df, aes(x=gdp_per_capita, y=Electricity_consumption_per_capita)) + 
  geom_point()
p + facet_wrap(~Country)
  ggplot(df,aes(x=gdp_per_capita)) + geom_density() + facet_wrap(~Country)
p + facet_wrap(~Country)+
  labs(title='Face charts by country', 
       subtitle='GDP per capita and Electricity consumption per capita', 
       x='GDP per capita', y='Electricity consumption per capita')+ 
  theme(axis.title.x = element_text(size=10,color="black",face="bold",angle=0))

#MODIFICADO
#Al grafico anterior le liberamos las escalas, modificamos los labels y le pusimos titulos y demas :).
p <- ggplot(df, aes( y=Electricity_consumption_per_capita)) + 
ggplot(df,aes(x=gdp_per_capita)) +
  labs(title='Face charts by country', 
       subtitle='GDP per capita and Electricity consumption per capita', 
       x='GDP per capita', y='Electricity consumption per capita')+ 
  theme(axis.title.x = element_text(size=10,color="black",face="bold",angle=0))

##
ggplot(df, aes(x =gdp_per_capita , y=Electricity_consumption_per_capita, color=Country)) +
  geom_line(linetype = 3,size=2,
             lwd = 2.1)+
labs(title='Line plot by country', 
     x='GDP per capita', y='Electricity consumption per capita')+ 
  theme(axis.title.x = element_text(size=10,color="black",face="bold",angle=0))


##MODIFICADO
p <- ggplot(df, aes(x=gdp_per_capita, y=Electricity_consumption_per_capita)) + 
  geom_point()
ggplot(df,aes(x=gdp_per_capita)) + geom_density(scales="free") + facet_wrap(~Country)
p + facet_wrap(~Country)+
  labs(title='Face charts by country', 
       subtitle='GDP per capita and Electricity consumption per capita', 
       caption='Note: The scale of the Electricity consumption per capita axis was released',
       x='GDP per capita', y='Electricity consumption per capita')+ 
  theme(axis.title.x = element_text(size=10,color="black",face="bold",angle=0))


  
#Activity B:Using faceting to understand data
#"Aquí quiere ver la distribución de las cantidades de los préstamos para diferentes grados de crédito.
# Objetivo: Trazar el monto del préstamo para diferentes grados de crédito usando el faceting.
df3s <- subset(df3,grade %in% c("A","B","C","D","E","F","G"))
pb1<-ggplot(df3s,aes(x=loan_amnt))
pb1
pb2<-pb1+geom_histogram(bins=10,fill="cadetblue4")
pb2
#Facet_wrap
pb3<-pb2+facet_wrap(~grade) 
pb3
#Free y coordinate for the subplots
pb4<-pb3+facet_wrap(~grade, scale="free_y")
pb4

#Activity B:Using faceting to understand data
#MODIFICADO
#Queremos ver la relacion entre el amount del loan y las categorias de credito.
ggplot(df3s, aes(x=grade,y=loan_amnt)) + 
  geom_jitter(aes(color = grade), size = 1, alpha = 0.7)+
  geom_boxplot(aes(color = grade), alpha = 0.5)+
  xlab('Grade') + 
  ylab('Loan amount') +
  ggtitle('Loan amount according to grade') + 
  theme_minimal()


#Activity B:Using faceting to understand data
#MODIFICADA
#Queremos ver la relacion entre el amount del loan y el proposito del credito, para compararlo con las categorias en el grafico anterior.
ggplot(df3s, aes(x = loan_amnt, fill = purpose , colour = purpose)) + 
  geom_histogram(colour = "black", lwd = 0.75, linetype = 1, alpha = 0.4, position = "identity")+
  labs(title='Histogram by purpose of credit', 
       subtitle='Loan amount',
       x='Loan amount', y='Count')+ 
  theme(axis.title.x = element_text(size=10,color="black",face="bold",angle=0), legend.key.height = unit (0.4, 'cm'),
        legend.key.width = unit (0.4, 'cm'))



#Topic C: Visual components - Color and shape Differentiated
#Topic C: Using and changing styles and colors
#Subtopic: using colors in plots

#Exercise - Using color to group points by variable
dfs <- subset(df,Country %in% c("Germany","India","China","United States"))
var1<-"Electricity_consumption_per_capita"
var2<-"gdp_per_capita"
name1<- "Electricity/capita"
name2<- "GDP/capita"
# Change color and shape of points
p1<- ggplot(dfs,aes_string(x=var1,y=var2))+
  geom_point(color=2,shape=2)+xlim(0,10000)+xlab(name1)+ylab(name2)
p1
#Grouping points by a variable mapped to colour and shape
p2 <- ggplot(dfs,aes_string(x=var1,y=var2))+
  geom_point(aes(color=Country,shape=Country))+xlim(0,10000)+xlab(name1)+ylab(name2)
grid.arrange(p1, p2, nrow = 2)

#Activity C:Using color differentiation in plots
#Supongamos que un banco ha concedido préstamos a personas con características diferentes (por ejemplo, situación laboral, propiedad de la vivienda, grado de crédito, etc.) y queremos ver las relaciones entre algunas de esas variables.
#Objetivo: Ver la distribución de la cantidad de préstamo frente a ser propietario de una casa usando diferentes colores según el nivel de crédito".

#color differentiate with credit grade.
dfn <- df3[,c("home_ownership","loan_amnt","grade")]
dfn <- na.omit(dfn) #remove NA y NONE
dfn <- subset(dfn, !dfn$home_ownership %in% c("NONE"))
ggplot(dfn,aes(x=home_ownership,y=loan_amnt))+geom_boxplot(aes(fill=grade))
#People with higher credit grades take smaller loans
#People with lower credit grades take small loans if they don't have a mortgage.

#Finer labelling in y 
ggplot(dfn,aes(x=home_ownership,y=loan_amnt))+geom_boxplot(aes(fill=grade))+
  scale_y_continuous(breaks=seq(0,40000,2000))

#Subtopic: Themes and changing the appearance of graphs

#Exercise:Using theme to customize a plot
#“The color palette can be found at: “http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf”
dfn <- subset(HollywoodMovies2013, Genre %in% c("Action","Adventure","Comedy","Drama","Romance")
              & LeadStudio %in% c("Fox","Sony","Columbia","Paramount","Disney"))
p1 <- ggplot(dfn,aes(Genre,WorldGross)) 
p1
p2 <- p1+geom_bar(stat="Identity",aes(fill=LeadStudio),position="dodge")
p2
p3 <- p2+theme(axis.title.x=element_text(size=15),
    axis.title.y=element_text(size=15),
    plot.background=element_rect(fill="gray87"),
    panel.background = element_rect(fill="beige"),
    panel.grid.major = element_line(color="Gray",linetype=1)
    )
p3

#Using predefined themes - Just show slide
p4 <- p2+theme_bw()+ggtitle("theme_bw()")
p5 <- p2+theme_classic()+ggtitle("theme_classic()")
p6 <- p2+theme_grey()+ggtitle("theme_grey()")
p7 <- p2+theme_minimal()+ggtitle("theme_minimal()")
grid.arrange(p4,p5,p6,p7,nrow=2,ncol=2)

library("ggthemes")
#install.packages("purrr")
library("purrr")

p7b <- p2+theme_economist()+ggtitle("theme_economist()")+scale_colour_economist()
p7b

q2 <- ggplot(dfs,aes_string(x=var1,y=var2))+
  geom_point(aes(color=Country,shape=Country))+xlim(0,10000)+xlab(name1)+ylab(name2)+theme_economist()+scale_colour_economist()
q2

#Exercise : Using or setting your own theme globally
mytheme <- theme(
  text = element_text(colour="Blue"),
  axis.text = element_text(size=12,color="Red"),
  axis.title = element_text(size = rel(1.5)))
p2 <- p2+ggtitle("Original Plot")
p8 <- p2+mytheme+ggtitle("Changed Plot with my theme")
grid.arrange(p2,p8,ncol=2)

#Exercise: Changing the color scheme of the given 
#Ver ?scale_fill_brewer
p4 + scale_fill_brewer(palette="Spectral")
p4 + scale_fill_brewer(palette="Pastel1")
p4 + scale_fill_brewer(palette="Oranges")

#Activity C: Using themes and color differentiation in a plot
# En ciertos casos puede surgir la necesidad de comparar dos variables y diferenciar por el color; por ejemplo, una empresa de comercialización digital podría desear comparar el número de visitas de su anuncio en diferentes sitios web, o comparar el número de clics frente al número de visitas de diferentes estados en el mismo sitio web.
# Objetivo: Trazar el IMC de hombres contra mujeres en diferentes países.
pd1 <- ggplot(df,aes(x=BMI_male,y=BMI_female))
pd2 <- pd1+geom_point()
pd2
pd3 <- pd1+geom_point(aes(color=Country),size=2)+
  scale_colour_brewer(palette="Dark2")
pd3
pd4 <- pd3+theme(axis.title=element_text(size=15,color="cadetblue4",
                                         face="bold"),
                 plot.title=element_text(color="cadetblue4",size=18,
                                         face="bold.italic"),
                 panel.background = element_rect(fill="azure",color="black"),
                 panel.grid=element_blank(),
                 legend.position="bottom",
                 legend.justification="left",
                 legend.title = element_blank(),
                 legend.key = element_rect(color=3,fill="gray97")
)+
  xlab("BMI Male")+
  ylab("BMI female")+
  ggtitle("BMI female vs BMI Male")
pd4

## Advanced Geoms and Statistics

# Create a bubble chart
# Dos de las técnicas avanzadas de trazado más comunes son los gráficos de dispersión (scatter) y los gráficos de burbujas (bubbles). Los gráficos de dispersión muestran la relación entre dos variables. Un gráfico de burbujas puede incluir una tercera variable. Cada punto (con sus valores (v1, v2, v3) de datos asociados) se traza como un disco, donde dos de los valores muestran las ubicaciones x e y, y el tercero representa el tamaño. Al igual que en un gráfico de dispersión, un gráfico de burbujas utiliza variables numéricas para sus ejes x e y. No puedes usar variables categóricas en un gráfico de burbujas".

#En este gráfico, trazaremos el consumo de electricidad per cápita para diferentes años y países. El tamaño del punto variará, según la población del país.

dfs <- subset(df,Country %in% c("Germany","India","China","United States","Japan"))

ggplot(dfs,aes(x=Year,y=Electricity_consumption_per_capita)) + geom_point(aes(size=population,color=Country))+
  coord_cartesian(xlim=c(1950,2020))+
  labs(subtitle="Electricity consumption vs Year",
       title="Bubble chart")+ylab("Electricity consumption")+
  scale_size(breaks=c(0,1e+8,0.3e+9,0.5e+9,1e+9,1.5e+9),range=c(1,5))

### Exercise: Creating density plots
df3s <- subset(df3,grade %in% c("A","B","C","D","E","F","G"))
#Let's do a histogram first and sub divide into the different grades.
ggplot(df3s,aes(x=loan_amnt)) + geom_histogram() + facet_wrap(~grade)

# We cannot see the shapes of the E,F,G grades very clearly. Also all the grades have different histogram counts. It would be better to use a density plot to compare.

ggplot(df3s,aes(x=loan_amnt)) + geom_density() + facet_wrap(~grade)

# Superimposing plots 

ggplot(df3,aes(x=loan_amnt)) + geom_density(aes(fill=grade),alpha=1/2) +
  scale_fill_brewer(palette="Dark2") + xlab("Loan Amount") + theme_light()

ggplot(df3,aes(x=loan_amnt))+ geom_density(aes(color=grade),alpha=0.2) +
  scale_fill_brewer(palette="Dark2") + xlab("Loan Amount") + theme_classic()

# Maps

states_map <- map_data("state")

glimpse(states_map)

#The map_data() function returns a data frame with the following columns: 
 #long - Longitude
 #lat - Latitude
 #group - This is a grouping variable for each polygon

#A region or subregion might have multiple polygons, for example, if it includes islands.

ggplot(states_map, aes(x=long, y=lat, group=group)) +    geom_polygon(fill="white", colour="black")

ggplot(states_map, aes(x=long, y=lat, group=group)) +    
  geom_path() + coord_map("mercator")

### World map data

# Get map data for world 
world_map <- map_data("world") 
ggplot(world_map, aes(x=long, y=lat, group=group)) +    geom_polygon(fill="white", colour="black")

### Map of Europe
europe <- map_data("world", region=c("Germany", "Spain", "Italy","France","UK","Ireland")) 
ggplot(europe, aes(x=long, y=lat, group=group, fill=region)) + geom_polygon(colour="black") + scale_fill_brewer(palette="Set3")

# Create a map with regions that are colored according to variable values
USStates$Statelower <- as.character(tolower(USStates$State))
glimpse(USStates)

us_data <- merge(USStates,states_map,by.x="Statelower",by.y="region")
head(us_data)

#Voter Chart for 2016 Elections

ggplot(us_data, aes(x=long, y=lat, group=group, fill=ClintonVote)) + geom_polygon(colour="black") +
  coord_map("mercator")+scale_fill_gradient(low="red",high="blue")

## Trends, correlations and statistical summaries

### Statistical summaries
#Read the data
df_fb <- read.csv("data/FB.csv")
df_fb$Date <- as.Date(df_fb$Date)
#Use strftime to get the month for each date
df_fb$Month <- strftime(df_fb$Date,"%m")
df_fb$Month <- as.numeric(df_fb$Month)
ggplot(df_fb, aes(Month,Close)) + 
  geom_point(color="red",alpha=1/2,position = position_jitter(h=0.0,w=0.0))+
  geom_line(stat='summary',fun.y=mean, color="blue",size=1)+
  scale_x_continuous(breaks=seq(0,13,1))+
  ggtitle("Monthly Closing Stock Prices: Facebook")+theme_classic()

### Trends and Scatterplots
#One can study trends in data by looking at scatter plots between two variables. This reveals if one variable is related to another variable. 

ggplot(dfs, aes(gdp_per_capita,Electricity_consumption_per_capita)) + geom_point(aes(color=Country))+xlim(0,30000)+ stat_smooth(method=lm)

ggplot(dfs, aes(gdp_per_capita,Electricity_consumption_per_capita,color=Country)) + geom_point() + stat_smooth(method=lm)
  
### Correlation plot
#Use only continuous variables columns. Drop "Year","Country"
dfs1 <- dfs[,colnames(dfs)[4:9]]
#Remove NA's or correlation won't work
dfs1 <- na.omit(dfs1)
M <- cor(dfs1)
corrplot(M,method="number")

#The plot looks messy because of the long names. Let's change the names to shorter names.
colnames(dfs1) <- c("gdp","electricity","mort","pov","bmi_m","bmi_f")
M <- cor(dfs1)
corrplot(M,method="number")

# One can see that the positively correlated variables (in Blue and Darkblue) are:
  #1. GDP and Electricity consumption
  #2. Electricity consumption and BMI's
  #3. BMI's of males and females
  #4. Poverty and under5mortality

#The one's which have negative corelation are:
  #1. mortality and electricity consumption
  #2. GDP and Poverty.
  #3. GDP and Mortality
  #4. Poverty and BMI

#One can also try other methods for the correlation plots:
corrplot(M,method="circle")
corrplot(M,method="pie")

#The fraction of the pie, gives an idea of how strong the correlation is and the color gives whether its positively or negatively correlated. 

#a) The "number" option gives us an exact number and there is no ambiguity. However, when one is presenting to an audience, it makes it difficult to read.

#b) The "circle" option is great visually as its color coded. But the 'pie' option is even better because one gets a feel for the size as well as type of correlation.

### Activity D
#Studying Correlations and making a scatter plot.
#Sometimes, two variables are highly interdependent, and you'd like to study their variations in greater detail, and then fit a model to it. For example, Facebook might be interested in studying the correlation between the number of Facebook friends and the age of a user, to find out which age group utilizes Facebook the most. They might also be interested in finding out whether the variation is linear.
# Aim: To make a scatter plot for the most correlated variables and then fit a linear regression model to it.”

t <- subset(df3,grade=="A")
z1 <- ggplot(t, aes(total_pymnt_inv,total_rec_prncp,color=grade)) + geom_point() + stat_smooth(method=lm)

z2 <- ggplot(t, aes(funded_amnt,total_pymnt_inv,color=grade)) + geom_point() + stat_smooth(method=lm,color=2)

grid.arrange(z1,z2,ncol=2)

#Both of these plots reveal an (approximate) linear relationship between the preceding pairs, confirming the numbers that we obtained with the cor command.”


