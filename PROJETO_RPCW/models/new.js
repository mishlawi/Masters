var mongoose = require('mongoose')

var newSchema = new mongoose.Schema({
    user:{type:String,required:true},
    date:{type:String,required:false},
    action:{type:Number,required:true},
    rec_name:{type:String,required:false},
    rec_id:{type:String,required:false},
    active:{type:Number,required:true},
    comment:{type:String,required:false},
    rating:{type:Number,required:false},
    free:{type:String,required:false}
})

newSchema.pre('save', async function(next) {
    var date = new Date()
    this.date = date.toISOString()
    next()
})

module.exports = mongoose.model('new', newSchema)