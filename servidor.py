from flask import Flask, render_template, redirect, jsonify, request, session, url_for
from flask_cors import CORS, cross_origin
from usuarios import usuarios
app = Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS']='Content-type'

@app.route('/')
def prueba():
    return jsonify(
        mensaje='Todo bien',
        usuarios= usuarios, 
        status= 200
    )

@app.route('/login', methods=['POST'])
def login():

    banderauser=False
    banderapassword=False
    username= request.json['username']
    password= request.json['password']
    for user in usuarios:
        if user['username']==username:
            entrada={
                'name': user['name'],
                'gender': user['gender'],
                'username': user['username'],
                'email': user['email'],
                'password': user['password']
            }
            banderauser=True
        if user['password']== password:
            banderapassword=True  
    if banderapassword ==False and banderauser==True:

        return jsonify(
            status=404,
            mensaje='Contraseña incorrecta',
            persona=2
        )
    if banderapassword ==True and banderauser==True:
        
        if username=='admin':
            return jsonify(
            status=200,
            mensaje='Sesión iniciada',
            persona=1
        )

        return jsonify(
            status=200,
            mensaje='Sesión iniciada',
            persona=2, 
            usuario= entrada
        )


@app.route('/registro', methods=['POST'])
def registro():
    contra=False
    correcta=request.json['password']
    tamaño = len(correcta)
    entrada={
        'name': request.json['name'],
        'gender': request.json['gender'],
        'username': request.json['username'],
        'email': request.json['email'],
        'password': request.json['password']
    }
    if any(chr.isdigit() for chr in correcta) ==True and tamaño>=8:
        if any(v=='#' for v in correcta) ==True or any(v=='$' for v in correcta) ==True or any(v=='&' for v in correcta) ==True or any(v=='?' for v in correcta) ==True or any(v=='¿' for v in correcta) ==True or any(v=='!' for v in correcta) ==True or any(v=='¡' for v in correcta) ==True  or any(v=='@' for v in correcta) ==True:
            contra=True
        else:
            contra= False
            return jsonify(
                mensaje= 'La contraseña debe contener al menos un simbolo',
                status= 404
            )
    else:
        contra= False
        return jsonify(
            mensaje='La contraseña tiene que ser de al menos 8 digitos y contener un numero',
            status= 404
        )      
            
              
    if contra ==True:  
        usuarioencontrado = [usuario for usuario in usuarios if usuario['username']==entrada['username']]
        if len(usuarioencontrado)==0:
            usuarios.append(entrada)
            return jsonify(
                mensaje= 'Usuario agregado', 
                status=200
            )

        else:
            return jsonify(
                mensaje= 'no se puede agregar, ya hay un usuario con ese nombre',
                status= 404
            )
        
@app.route('/usuarios')
def mostrarUsuarios():
    return jsonify(
        usuario=usuarios
    )

@app.route('/editar/<string:usuario_username>', methods=['PUT'] )
def editarUsuarios(usuario_username):
    contra=False
    usuarioEncontrado=[usuario for usuario in usuarios if usuario['username'] ==usuario_username]
    if (len(usuarioEncontrado)>0):
        nuevousername=request.json['username']
        nuevacontraseña=request.json['password']
        tamaño = len(nuevacontraseña)
        if any(chr.isdigit() for chr in nuevacontraseña) ==True and tamaño>=8:
            if any(v=='#' for v in nuevacontraseña) ==True or any(v=='$' for v in nuevacontraseña) ==True or any(v=='&' for v in nuevacontraseña) ==True or any(v=='?' for v in nuevacontraseña) ==True or any(v=='¿' for v in nuevacontraseña) ==True or any(v=='!' for v in nuevacontraseña) ==True or any(v=='¡' for v in nuevacontraseña) ==True  or any(v=='@' for v in nuevacontraseña) ==True:
                contra=True
            else:
                contra= False
                return jsonify(
                    mensaje= 'La contraseña debe contener al menos un simbolo',
                    status= 404
                )
        else:
            contra= False
            return jsonify(
                mensaje='La contraseña tiene que ser de al menos 8 digitos y contener un numero',
                status= 404
            ) 
        usernamediferente = [usuario for usuario in usuarios if usuario['username']==nuevousername]
        
        if len(usernamediferente)==0 and contra==True:
            usuarioEncontrado[0]['name']=request.json['name']
            usuarioEncontrado[0]['gender']=request.json['gender']
            usuarioEncontrado[0]['username']=request.json['username']
            usuarioEncontrado[0]['email']=request.json['email']
            usuarioEncontrado[0]['password']=request.json['password']
            return jsonify(
                mensaje='Usuario actualizado',
                usuario=usuarios,
                status=200
            )
        else:
            if nuevousername==usuario_username:
                usuarioEncontrado[0]['name']=request.json['name']
                usuarioEncontrado[0]['gender']=request.json['gender']
                usuarioEncontrado[0]['username']=request.json['username']
                usuarioEncontrado[0]['email']=request.json['email']
                usuarioEncontrado[0]['password']=request.json['password']
                return jsonify(
                    mensaje='Usuario actualizado',
                    usuario=usuarios,
                    status=200
                )
            return jsonify(
                mensaje='Ese username ya esta siendo utilizado',
                usuario=usuarios,
                status=404
            )
    else:
         return jsonify(
            mensaje='No se encontro un usuario',
            status=404
        )       

@app.route('/borrar/<string:usuario_username>', methods=['DELETE'] )
def borrarUsuarios(usuario_username):
    usuarioEncontrado=[usuario for usuario in usuarios if usuario['username'] ==usuario_username]
    if (len(usuarioEncontrado)>0):
        usuarios.remove(usuarioEncontrado[0])
        return jsonify(
            mensaje='Usuario eliminado',
            usuario=usuarios,
            status=200
        )
    else:
         return jsonify(
            mensaje='No se encontro un usuario',
            status=404
        ) 
if __name__ =='__main__':
    app.run(host='localhost')
    app.run(debug=True)