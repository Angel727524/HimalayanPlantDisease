from database import get_database_connection

plant_name = "Rhododendron"

connection = get_database_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT
        p.plant_name,
        d.disease_name,
        d.disease_type,
        d.description,
        d.cause,
        d.symptoms,
        d.treatment,
        d.prevention,
        d.severity
    FROM plants p
    JOIN plant_diseases pd
        ON p.plant_id = pd.plant_id
    JOIN diseases d
        ON pd.disease_id = d.disease_id
    WHERE p.plant_name = %s
""", (plant_name,))

diseases = cursor.fetchall()

print("\n==============================")
print("DISEASE INFORMATION")
print("==============================")

if diseases:
    for disease in diseases:
        print("\nDisease:", disease[1])
        print("Type:", disease[2])
        print("Description:", disease[3])
        print("Cause:", disease[4])
        print("Symptoms:", disease[5])
        print("Treatment:", disease[6])
        print("Prevention:", disease[7])
        print("Severity:", disease[8])
else:
    print("No diseases found for this plant.")

cursor.close()
connection.close()