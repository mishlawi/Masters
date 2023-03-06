// Controlador para o modelo User

var User = require('../models/user')

// Devolve a lista de Users
module.exports.listar = () => {
    return User
        .find()
        .sort('username')
        .exec()
}

module.exports.consultar = id => {
    return User
        .findOne({_id: id})
        .exec()
}

module.exports.consultarByUsername = uname => {
    return User
        .findOne({username: uname})
        .exec()
}


module.exports.inserir = u => {
    var novo = new User(u)
    return novo.save()
}

module.exports.remover = function(id){
    return User.deleteOne({_id: id})
}


module.exports.update = async (id,usern,pass,nivel) => {
    //console.log("udate: ",id,usern,pass,nivel)
    
    user = await this.consultar(id)
    console.log(user)
    if(!user)
        throw new Error("Utilizador não encontrado!")
    
    if(!pass)
        pass = user.password
    
    if(!usern)
        usern = user.username

    await User.updateOne({_id: id},{$set: {password: pass, username: usern, level: nivel}})
            .exec()
}


module.exports.validatePassword = async (username, password) => {
    user = await this.consultarByUsername(username)
    //console.log(user)
    if(!user) erroFind("Utilizador não encontrado!")

    //var compare = await user.isValidPassword(password)

    if(!(password==user.password))
        return null

    return user
}
