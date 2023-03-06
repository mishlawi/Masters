var New = require('../models/new')
var File =  require('../controllers/ficheiros');

module.exports.list = async () => {
    return await New
            .find()
            .sort({date: -1})
            .exec()
}

module.exports.listActive = async () => {
    return await New
            .find({active:1})
            .sort({date: -1})
            .exec()
}

module.exports.listInactive = async () => {
    return await New
            .find({active:0})
            .sort({date: -1})
            .exec()
}

module.exports.insert = async n => {    
    return New.create(n)
}

module.exports.delete =  id =>{
    return New.deleteOne({_id: id})
}

module.exports.hide = async id =>{
    await New.updateOne({_id: id}, {active : 0})   
}

module.exports.show = async id =>{
    await New.updateOne({_id: id}, {active : 1})   
}

module.exports.update = async (id,content) =>{
    var d = new Date().toISOString()
    await New.updateOne({_id: id}, {date:d,free:content})   
}

