import mysql.connector
new_medicines=[]
def create_medicine(name,quantity,price,expiry):
  new_medicines.append([name,quantity,price,expiry])
  try:
     conn=mysql.connector.connect (
        host="localhost",
        user="root",
        passwd="",
        database="medicines"
     )
     cursor=conn.cursor()
     sql = "INSERT INTO meddata  (Name,Quantity,Price,Expiry) VALUES (%s,%s,%s,%s)"
     values = (name,quantity,price,expiry)
     cursor.execute(sql,values)
     conn.commit()

     print(f"Successfully added medicine: {name}")
  except mysql.connector.Error as err:
     print(f"Something went wrong: {err}")
  finally:
     if conn.is_connected():
        conn.close()

name = input("Please enter your medicine name: ")
quantity = int(input("Please enter your quantity: "))
price = float(input("Please enter your price: "))
expiry = float(input("Please enter your expiry: "))

create_medicine(name, quantity, price, expiry)
