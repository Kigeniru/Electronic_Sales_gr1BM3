import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import altair as alt
from wordcloud import WordCloud
from mpl_toolkits.mplot3d import Axes3D

st.title('Data Visualization of an Electronic Store between September 2023 - September 2024')
st.markdown(' ')
st.markdown('by Group 1 BM3')
st.markdown('John Kenneth Alon')
st.markdown('Rob Eugene Dequinon')
st.markdown('Neil Mediavillo')
st.markdown('Emmanuel Villanosa')
st.markdown('Ezekiel Martin')
st.markdown(' ')

#Data Descriptions

st.markdown("""Listed below is the data provided by the dataset. It includes the 
            customer ID, age, gender, loyalty number, product type, SKU, rating, 
            order status, payment method, total price, unit price, quantity, 
            purchase date, shipping type, add-ons purchased, and add-on total""")
st.markdown(' ')

df = pd.read_csv('Electronic_sales_Sep2023-Sep2024.csv')
df.info()
df.isna().sum()
df.describe()


#Data Visualization 1

st.header('Correlation between the age of the customer and the number of units they purchase')
st.markdown(' ')
st.markdown('Records the amount of units each age group from 18 to 80 years old.')

bins = [18, 30, 40, 50, 60, 70, 80]
labels = ['18-30', '31-40', '41-50', '51-60', '61-70', '71-80']

df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)

x = df.groupby('AgeGroup')['Quantity'].sum()

print(x)

plt.figure(figsize=(10, 6))
x.plot(kind='bar', color='green')
plt.title('Correlation between the age of the customer and the number of units they purchase')
plt.xlabel('Age')
plt.xticks(rotation=45)
plt.ylabel('Quantity')
plt.legend()
plt.grid(True)

st.pyplot(plt)
plt.clf()

st.markdown(' ')
st.markdown("""This bar graph displays the correlation of the number of units that clients 
            of various ages purchase. The age ranges up from 18 to 30 years & 71 to 80 years 
            old. The average number of units purchased by each age group is shown by each 
            green bar. With about 9000 units, the youngest group (18–30) makes the most 
            purchases. The following age group (31–40) sees a significant decline in numbers, 
            whereas the middle-aged groups see rather stable levels. It's interesting to note 
            that the oldest group has a minor decline followed by a small gain for those aged 
            61 to 70. All things considered, the graph indicates that although young adults 
            purchase a great deal more, other age groups' spending patterns are largely unchanged, 
            with a few small exceptions.""")
st.markdown(' ')

#Data Visualization 2

st.header('Monthly Revenue')
st.markdown(' ')
st.markdown('Tracks the total sales of the store every month, from September 2023 - September 2024')
st.markdown(' ')

df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])

y = df.groupby(df['Purchase Date'].dt.to_period('M'))['Total Price'].sum().reset_index()

y['MonthYear'] = y['Purchase Date'].dt.strftime("%B %Y")

x= y['MonthYear']

print(y)

plt.figure(figsize=(10, 6))
plt.plot(x, y['Total Price'], marker='o', linestyle='-', color='b', label='Monthly Sales')
plt.title('Monthly Revenue')
plt.xlabel('Months')
plt.xticks(rotation=45)
plt.ylabel('Total Revenue')
plt.legend()
plt.grid(True)

st.pyplot(plt)
plt.clf()

st.markdown(' ')
st.markdown("""The monthly revenue from September 2023 to September 2024 is displayed in 
            this line graph. The monthly sales are shown by the blue line. September 
            2023 has a low level of revenue, which increases in October and remains rather 
            constant through December. January 2024 shows a significant increase in sales, 
            which peak during that month. After then, monthly revenue varies little but 
            stays high. In September 2024, the last month, there is a discernible decline. 
            The revenue pattern is generally upward, as seen by the graph, with a notable 
            increase at the beginning of 2024, high sales that are reasonably consistent 
            throughout the majority of the year, and a decline towards the end.""")
st.markdown(' ')


#Data Visualization 3

st.header('Sales according to Product Type')
st.markdown(' ')
st.markdown('Records the total price of each product type namely, headphones, laptops, smartphones, smartwatches, and tablets')
st.markdown(' ')

completed_orders = df[df['Order Status'] == 'Completed']

sales_by_product_type = completed_orders.groupby('Product Type')['Total Price'].sum().reset_index()


plt.figure(figsize=(10, 6))
colors = plt.cm.Paired(range(len(sales_by_product_type)))
bars = plt.bar(sales_by_product_type['Product Type'], sales_by_product_type['Total Price'], color=colors)

for bar, value in zip(bars, sales_by_product_type['Total Price']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')


plt.title('Sales by Product Type')
plt.xlabel('Product Type')
plt.ylabel('Total Sales (Sum of Total Price) in Ten Millions')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.9)

st.pyplot(plt)
plt.clf()
st.markdown(' ')

st.markdown("""This bar chart shows the overall sales generated by each product. 
            The graph portrays the dominant performance of Smartphones, 
            generating over 14.4 million in sales. Along with that, the second 
            highest generated sales are Smartwatches with a exceeding 9.3 million, 
            followed by Laptops generating 8.3 million, and Tablets generating 
            7.7 million. Lastly, Headphones are lagging behind with the lowest 
            sales, just over 2.7 million. Therefore, we can positivley conclude 
            the high demand and usage of Smartphones compare to other electronical 
            devices and gadgets.""")
st.markdown(' ')


#Data Visualization 4

st.header('Total Sales according to Shipping Type')
st.markdown(' ')
st.markdown('Keeps track of which Shipping Type is being used the most, namely between expedited, same day, standard, express, and overnight ')
st.markdown(' ')

completed_orders = df[df['Order Status'] == 'Completed']

sales_by_shipping_type = completed_orders.groupby('Shipping Type')['Total Price'].sum().reset_index()


categories = sales_by_shipping_type['Shipping Type']
values = sales_by_shipping_type['Total Price']

if len(categories) == 0 or len(values) == 0:
    print("No data available to plot.")
else:

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()


    values = np.concatenate((values, [values[0]]))
    angles += angles[:1]


    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='skyblue', alpha=0.5)
    ax.plot(angles, values, color='blue', linewidth=2)


    categories_with_values = [f'{category} ({value:.2f})' for category, value in zip(categories, sales_by_shipping_type['Total Price'])]


    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories_with_values, fontsize=10)

    plt.title('Total Sales by Shipping Type')

    st.pyplot(plt)
    plt.clf()
    st.markdown(' ')

st.markdown("""A radar chart is used to illustrate the total sales throughout all shipping 
            types. With sales of more than 14,3 million, standard shipping excels above 
            any other shipping types. In second place with almost 8.4 million in sales is 
            expedited shipping. Just behind with over 8.2 million is Same Day shipping. 
            Sales of overnight delivery are slightly higher than 5.8 million, while Express's 
            sales are little lower at 5.6 million. Express shipping has the lowest sales 
            compared to Standard shipping which performs best overall.""")
st.markdown(' ')

#Data Visualization 5

st.header('Add-ons Purchased Popularity')
st.markdown(' ')
st.markdown("""Showcases the most purchased add-on, between impulse item, warranty accessory, 
            extended warranty, warranty impulse, accessory,  item accessory, item extended, 
            accessory extended""")
st.markdown(' ')

text = ' '.join(df['Add-ons Purchased'].dropna().astype(str))

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Add-ons Purchased Popularity')

st.pyplot(plt)
plt.clf()
st.markdown(' ')


st.markdown("""Using word cloud visualization, the chart represents the frequency of different 
            add-ons purchased by customers from the data, the word cloud emphasizes more 
            frequent purchases with larger, bolder text. Less frequent purchases appear smaller 
            and less prominent. The chart highlights which add-ons are more popular among 
            customers, showcased in a way to easily understand purchasing trends without needing 
            to analyze raw data. It can be concluded that the "Impulse Item" add-on was favored 
            by many customers based on the data.""")
st.markdown(' ')

#Data Visualization 6

st.header('Ratings per Product Type')
st.markdown(' ')
st.markdown('Records the ratings for each product type, namely the headphones, tablet, smartphones, smartwatches, laptops')
st.markdown(' ')

sns.violinplot(x='Product Type', y='Rating', data=df, palette="Pastel1")
plt.title('Ratings per Product Type')
plt.xlabel('Product Type')
plt.ylabel('Rating')
plt.xticks(rotation=45)

st.pyplot(plt)
plt.clf()

st.markdown(' ')
st.markdown("""Using a violin plot, we are able to visualize the distribution of 
            product ratings across different product types. The width of the violin 
            represents the frequency of ratings at that value, with wider sections 
            indicating more common ratings. The plot highlights each product type 
            that is rated by customers, which helps identify trends such as which 
            products tend to receive higher or lower ratings. It can be concluded 
            that the "Headphones" product type seemed to obtain the most balanced 
            ratings out of all.""")
st.markdown(' ')


#Data Visualization 7

st.header('Percentage of Customers from the Two Sexes')
st.markdown(' ')
st.markdown('Shows how much of the customers are male and female')
st.markdown(' ')

pie = df['Gender'].value_counts()
colors = ['#75d2dd', '#f7adef']
exuplosion = [0.1, 0]

plt.pie(pie, labels = ['Male', 'Female'], autopct='%1.1f%%', colors = colors, shadow = True, explode = exuplosion, startangle = 90)
plt.title('Perecentage of Buyers from Two Sexes')

st.pyplot(plt)
plt.clf()

st.markdown(' ')
st.markdown("""Using a Pie Chart, we can see the total number of customers of each 
            sexes (Gender). There's really no need of a deep explanation here, 
            almost a 50-50 split between the two sexes, 50.8% of the customers are 
            Male, while the 49.2% are composed of Female customers. This comes no 
            suprise as the new modern world is now filled with diverse people with 
            iverse interest. Additionally, everyone has some tech device, not just 
            held by a majority set of people.""")
st.markdown(' ')

#Data Visualization 8

st.header('Total spendings by the Two Sexes')
st.markdown(' ')
st.markdown('Shows how much each of the two sexes, male and female, spend on the store')
st.markdown(' ')

x = df['Total Price'].sum()
y = df['Gender'].value_counts()
colors = ['#edff7b', '#b896ff']

plt.bar(y.index, y.values, color=colors)
plt.title('Total Spendings of Two Sexes')
plt.ylabel('Total Sum of Spendings (Total Price)')
plt.xlabel('Gender')

st.pyplot(plt)
plt.clf()

st.markdown(' ')
st.markdown("""In this graph, I used a Bar Chart to represent the total number 
            of spendings of each sexes (Gender). Getting the sum of the Total 
            Price from the data set, we come into a conclusion that the Male 
            customers slighlty spends higher, reaching above the 10,000s, than 
            the Female which reached just shy below the 10,000s.""")
st.markdown(' ')


#Data Visualization 9

st.header('Order Status')
st.markdown(' ')
st.markdown('Shows what percentage of orders were completed or cancelled')
st.markdown(' ')

status = df['Order Status'].value_counts()
colors = ['skyblue', 'Red']
exuplosion = [0.1, 0]

print(status)

plt.pie(status, labels = ['completed', 'cancelled'], autopct='%1.1f%%', colors = colors, explode = exuplosion, shadow = True)
plt.title('Order Status')

st.pyplot(plt)
plt.clf()

st.markdown(' ')
st.markdown("""The order status dictates whether a customer who has purchased or ordered a 
            product has cancelled their transaction. With 67.2%% completing their order, 
            it shows that the majority of customers successfully followed through with their 
            purchases, while the remaining 32.8%% cancelled. This means that a significant 
            portion of customers either changed their minds or encountered an issue that led 
            them to cancel their transactions. Understanding why this cancellation rate exists 
            could be key to improving customer experience, addressing potential barriers during 
            the purchasing process, and ultimately increasing the completion rate in future 
            transactions.""")
st.markdown(' ')


#Data Visualization 10

st.header('Distribution of Payment Methods')
st.markdown(' ')
st.markdown('Records which of the payment methods, credit card, paypal, bank transfer, cash, and debit card, are used the most')
st.markdown(' ')

df['Payment Method'] = df['Payment Method'].str.lower()

payment_method_counts = df['Payment Method'].value_counts()

print(payment_method_counts)

payment_method_counts.plot(kind='bar', color='skyblue')

plt.xlabel('Payment Method')
plt.ylabel('Number of Transactions')
plt.title('Distribution of Payment Methods')
plt.xticks(rotation=45)

st.pyplot(plt)
plt.clf()

st.markdown(' ')
st.markdown("""The data shows that customers primarily prefer using 
            credit card and PayPal for their transactions, with both 
            methods almost equally popular. Bank transfers are the third 
            most common payment method , followed by cash and debit card, 
            which are the least utilized. This suggests that digital and 
            secure payment options are favored by most customers, while 
            traditional methods like cash and debit cards are less 
            commonly used.""")
st.markdown(' ')
