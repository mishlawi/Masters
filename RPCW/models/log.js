var mongoose = require('mongoose')

var logSchema = new mongoose.Schema({
    user_id:{type:String,required:true},
    username:{type:String,required:true},
    action:{type:String,required:true},
    date:{type:String,required:false},
    recurso:{type:String,required:false}
})

logSchema.pre('save', async function(next) {
    var date = new Date()
    this.date = date.toISOString()
    next()
})

module.exports = mongoose.model('log', logSchema)