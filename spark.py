# -*- coding: utf-8 -*-


from pyspark.sql import SparkSession
spark=SparkSession.builder.appName("Helllo").master("local[*]").getOrCreate()

from google.colab import files
uploaded=files.upload()

from pyspark.sql.functions import col
df=spark.read\
    .option("header","true")\
    .option("inferSchema","true")\
    .csv("BigMart Sales.csv")
df.show()
df.printSchema()
column1=df.Item_Identifier
column2=df['Item_Weight']
column3=col('Item_Fat_Content')
df.select(column1,column2,column3).show()
df.select("Item_Identifier","Item_Weight","Item_Fat_Content").show()

from pyspark.sql.types  import StringType
from pyspark.sql.types import *
col_Item_Weight_as_String=df['Item_Weight'].cast(StringType()).alias("Item")
df.select(col_Item_Weight_as_String,df['Item_Weight']).show()
col_iW=df['Item_weight'].cast(IntegerType()).alias("IntWeight")
df.select(col_iW).show()

from pyspark.sql.functions import*
def load_func(symbol:str):
   ddf=spark.read.option("header","true")\
   .option("inferSchema",'true')\
   .csv(symbol+".csv")

   return df.select(
       col("Item_Identifier").cast(StringType()).alias("II"),
       df["Item_weight"].cast(FloatType()).alias("WE"),
       df['Item_Fat_Content'].cast(StringType()).alias('Item_Fat')
   )

getDataFrame=load_func("BigMart Sales")
getDataFrame.show()
getDataFrame.printSchema()
concatDf=getDataFrame.select( concat(col("II"), lit(" hello")).alias("Concatenated_Column"))
concatDf.show()
getDataFrame.createOrReplaceTempView("getDataFrame")
spark.sql("select * from getDataFrame").show()
spark.sql("SELECT WE, CAST(WE AS INT) as WE_Integer FROM getDataFrame").show()

getDataFrame.show()
getDataFrame.sort(getDataFrame["WE"]).show()
getDataFrame.sort(getDataFrame['II'].desc()).show()

getDataFrame.groupBy("II").max("WE").show()
getDataFrame.groupBy("II").agg(
    sum("WE").alias("Total"),
    avg("WE").alias("Average")
).show()
from pyspark.sql.functions import row_number
from pyspark.sql.window import Window
window_spec = Window.partitionBy("Item_Fat").orderBy("WE")

df_with_rownum = getDataFrame.withColumn("row_num", row_number().over(window_spec))
df_with_rownum.show()
df_add=getDataFrame.withColumn("Country",lit("India"))
df_add.show()

from pyspark.sql import SparkSession
from pyspark.sql.functions import*
from pyspark.sql.window import Window
sparkk=SparkSession.builder.appName("window").getOrCreate()
data=[
    ("A","2024-01-01",100),
    ("A","2024-01-01",200),
    ("A","2024-01-03",300),
    ("B","2024-01-01",400),
    ("B","2024-01-02",1500),
]
dd=sparkk.createDataFrame(data,["user","date","sales"])
dd.show()
#convert date comun that in string to date format
dd=dd.withColumn("date",to_date("date"))
dd.show()
window_sp=Window.partitionBy("user").orderBy("date")
#in each group it start 1,2,3....
dd.withColumn("row_num",row_number().over(window_sp)).show()
#in each group if duplicate occur it will same 1 2 2 2 3,4 ,4
dd.withColumn("rank",rank().over(window_sp)).show()
#When you want ranking without gaps
dd.withColumn("dense_rank", dense_rank().over(window_sp)).show()
#Value from the previous row
dd.withColumn("prev_sales", lag("sales", 1).over(window_sp)).show()
# Value from the next row
dd.withColumn("next_sales", lead("sales", 1).over(window_sp)).show()
dd.withColumn("sum_sales",sum("sales").over(window_sp.rowsBetween(Window.unboundedPreceding,Window.currentRow))).show()
dd.withColumn("avg",avg("sales").over(window_sp.rowsBetween(-1,0))).show()
