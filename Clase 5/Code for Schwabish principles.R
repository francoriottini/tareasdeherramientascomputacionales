#Prior to use, install the following packages:
  #install.packages("ggplot2")
  #install.packages("tibble")
  #install.packages("dplyr")
  #install.packages("gridExtra")
  #install.packages("Lock5Data")
  #install.packages("ggthemes")
  #install.packages("maps")
  #install.packages("mapproj")
  #install.packages("corrplot")
  #install.packages("fun")
  #install.packages("zoo")

#Used datafiles and sources:
#  a) gapminder.csv - Modified dataset from various datasets available at:
#  https://www.gapminder.org/data/
#  b) xAPI-Edu-Data.csv:
#  https://www.kaggle.com/aljarah/xAPI-Edu-Data/data
#c) LoanStats.csv:
#  Loan Data from Lending Tree - https://www.lendingclub.com/info/download-data.action
#d) Lock5Data

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
setwd("~/Desktop/UDESA/Herramientas computacionales/Clase 5/Applied-Data-Visualization-with-R-and-ggplot2-master/Applied-Data-Visualization-with-R-and-ggplot2-master")

#Check working directory
getwd()

#Note: Working directory should be "Beginning-Data-Visualization-with-ggplot2-and-R"

#Load the data files
df <- read.csv("data/gapminder-data.csv")
df2 <- read.csv("data/xAPI-Edu-Data.csv")
df3 <- read.csv("data/LoanStats.csv")

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

#Modificado3
p1mod <- ggplot(df, aes(y=Electricity_consumption_per_capita, x = Year, color = Country)) +
  geom_line(size=1.5) + theme_minimal() +
  labs(x="",
       y="",
       title="Consumo de electricidad per cápita",
       subtitle="(kWh anual)") +
  theme(legend.position="top") +
  scale_color_discrete(name="",
                       labels=c("Brasil","China","Alemania","India","Japón","Reino Unido","Estados Unidos"))
p1mod

#Veo que hay muchos NA's por lo tanto puedo seleccionar un tramo de la base de datos para poder graficar mas acorde.
dffiltered <- df %>% filter(Electricity_consumption_per_capita != 0)

p1mod <- ggplot(dffiltered, aes(y=Electricity_consumption_per_capita, x = Year, color = Country)) +
  geom_line(size=1.5) + theme_minimal() +
  labs(x="",
       y="",
       title="Consumo de electricidad per cápita",
       subtitle="(kWh anual)") +
  theme(legend.position="top") +
  scale_color_discrete(name="",
                       labels=c("Brasil","China","Alemania","India","Japón","Reino Unido","Estados Unidos"))
p1mod
  

#MODIFICADO3 el que mas me gusto
#Le modificamos poder mirar conjunto los paises y el consumo de electricidad per capita. 
ggplot(df, aes(x = Electricity_consumption_per_capita, fill = Country , colour = Country)) + 
  geom_histogram(colour = "black", lwd = 0.75, linetype = 1, alpha = 0.5, position = "identity")+
  labs(title='Histogram by country', 
     subtitle='Electricity consumption per capita',
     x='Electricity consumption per capita', y='Count')+ 
  theme(axis.title.x = element_text(size=10,color="black",face="bold",angle=0))


#ORIGINAL
p1 <- ggplot(df, aes(x=gdp_per_capita, y=Electricity_consumption_per_capita)) + 
  geom_point() + 
  facet_grid(Country ~ .) + #Horizontally Arranged 
  facet_grid(. ~ Country) + #Vertically Arranged
  facet_wrap(~Country)
p1

#Plot2 modificado
p2 <- ggplot(df, aes(x =gdp_per_capita , y=Electricity_consumption_per_capita, color=Country)) +
  geom_line(linetype = 1,size=0.9,
            lwd = 2.1)+
  labs(title='Line plot by country', 
       x='GDP per capita', y='Electricity consumption per capita')+ 
  theme(axis.title.x = element_text(size=9,color="black",face="bold",angle=0))

p2

#Plot 3 Original
df3s <- subset(df3,grade %in% c("A","B","C","D","E","F","G"))
pb1<-ggplot(df3s,aes(x=loan_amnt)) +
  geom_histogram(bins=10,fill="cadetblue4") +
  facet_wrap(~grade) +
  facet_wrap(~grade, scale="free_y")

pb1

#Queremos ver la relacion entre el amount del loan y las categorias de credito.
p3 <- ggplot(df3s, aes(x=grade,y=loan_amnt)) + 
  geom_jitter(aes(color = grade), size = 1, alpha = 0.7)+
  geom_boxplot(aes(color = grade), alpha = 0.5)+
  xlab('Grade') + 
  ylab('Loan amount') +
  ggtitle('Loan amount according to grade') + 
  theme_minimal()

p3


