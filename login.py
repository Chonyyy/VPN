import json

def get_register(file_name='data/usuarios.json'):
    try:
        with open(file_name, 'r') as file:
            dictionary = json.load(file)
        return dictionary 
    except FileNotFoundError:
        new_dictionary={'Sherlyn5425':'*Sher'}
        with open(file_name, 'w') as file:
            json.dump(new_dictionary, file)
            return get_register(file_name)

            
def login(user_name,password,file_name='data/usuarios.json'):
    if user_name == '' or password== '':
        return 0
    
    register=get_register(file_name)
    for user in register:
        if user["usuario"]==user_name:
            if password == user["contrasenna"]:
                return 1
    return 0        
   
                      
                            
                        
            
                   

