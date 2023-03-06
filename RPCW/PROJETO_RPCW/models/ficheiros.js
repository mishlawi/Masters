const mongoose = require('mongoose')

var ficheiroSchema = new mongoose.Schema({
    creation_date: Date,
    submission_date: Date,
    producer: String, //nome de quem fez o ficheiro
    user: String, //nome de quem submeteu o ficheiro
    desc: String,
    type: Number, //0-slides 1-exame 2-manual  3-relatório 4-tese
    name: String,
    path: String,
    mimetype: String,
    size: Number,
    comments:[{
        from: String,
        date: Date,
        content: String,
        rating: Number
    }]
})


module.exports = mongoose.model('ficheiro',ficheiroSchema)