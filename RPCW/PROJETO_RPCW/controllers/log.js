var Log = require('../models/log')

module.exports.list = async () => {
    return await Log
            .find()
            .sort({date: -1})
            .exec()
}

module.exports.insert = log => {
    return Log.create(log)
}