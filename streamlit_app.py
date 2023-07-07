import pandas
import streamlit
import requests
import snowflake.connector
from urllib.error import URLError

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()


streamlit.title('My Mom\'s New Healthy Diner')


streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach, & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Advocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)



streamlit.header("Fruityvice Fruit Advice!")

def get_fruity_advice(this_fruit_choice): 
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruity_advice(fruit_choice)
    streamlit.dataframe(back_from_function)      
except URLError as e:
  streamlit.error()


# my_cur.execute("SELECT * FROM fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header("Fruit Load List Contains:")
# streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list VALUES ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_function)

# SF
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

streamlit.title("View Our Fruit List - Add Your Favorites!")
# add button to load fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)


#my_cur.execute("INSERT INTO fruit_load_list VALUES("+add_my_fruits+")")



