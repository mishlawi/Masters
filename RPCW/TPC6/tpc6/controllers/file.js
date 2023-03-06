const mongoose = require("mongoose")
var Ficheiro = require('../models/ficheiro')

module.exports.list = () => {
    return Ficheiro
        .find()
        .sort({ _id: 1 })
        .exec()
}

module.exports.insert = ficheiro => {
    if ((Ficheiro.find({ _id: ficheiro._id }).exec).length != 1) {
        var newFicheiro = new Ficheiro(ficheiro)
        return newFicheiro.save()
    }
}

module.exports.remove = id => {
    Ficheiro
        .find({ _id: id })
        .deleteOne()
        .exec()
}

module.exports.getById = id => {
    return Ficheiro
        .findOne({ __id: id })
        .exec()
}