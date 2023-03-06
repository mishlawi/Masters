const mongoose = require('mongoose')
var Para = require('../models/para')

module.exports.listar = () => {
    return Para
        .find() //devolve uma lista enquanto que findOne devolve um objeto só
        .exec()
}

module.exports.inserir = (p) => {
    var d = new Date()
    p.data = d.toISOString().substring(0,16)
    var novo = new Para(p)
    return novo.save()
}

module.exports.editar = function(id,data){
    var d = new Date().toISOString().substring(0,16)
    return Para
            .updateOne({_id:id},{data:d, para: data.para})
}

module.exports.delete = function(id){
    return Para.deleteOne({_id:id}).exec()
}