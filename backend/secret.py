database_name = "trivia"

path = "postgresql://{}:{}@{}/{}".format(
    "student", "student", "localhost:5432", database_name
)