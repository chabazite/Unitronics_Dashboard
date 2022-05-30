import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("Database")
# ADD SETTINGS TO SECTION
config_file.set("Database", "host", "***REMOVED***")
config_file.set("Database", "dbase", "***REMOVED***")
config_file.set("Database", "userName", "***REMOVED***")
config_file.set("Database", "password", "***REMOVED***")

# SAVE CONFIG FILE
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")

# PRINT FILE CONTENT
read_file = open("configurations.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()