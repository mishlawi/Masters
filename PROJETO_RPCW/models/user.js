const mongoose = require('mongoose')
var passportLocalMongoose = require("passport-local-mongoose");

var userSchema = new mongoose.Schema({
    username: { type: String, required: true },
    password: { type: String, required: true },
    level: Number
  });

userSchema.plugin(passportLocalMongoose);// assim metemos as 3 funções: serialize, desserialize e ...
module.exports = mongoose.model('user', userSchema)