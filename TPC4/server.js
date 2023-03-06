var http = require('http')
var axios = require('axios')
var fs = require('fs')



function notDone(tarefas){
    html = `<ul id="job">\n`

    tarefas.forEach(tarefa => {
        html+=`
        <li>
            <p>${tarefa.titulo}</p>
            <p>${tarefa.descricao}</p>
            <a href="/todos/${tarefa.nr}/editar">
            <a href="/tasks/${tarefa.id}/completada">
        </li>\n
        \n
            `
    })

    html+= `</ul>\n`

    return html
}


function done(tarefas){

    pagHTML=`<ul id="job">\n`

    tarefas.forEach(tarefa =>{
        html+=`
        <li>
            <p>${tarefa.titulo}</p>
            <a  href="/tasks/${tarefa.nr}/delete">   
        </li>\n
        `
    })
    html += `</ul>\n`

    return html
}


function edit(tarefas,index){
    
    pagHTML=`<ul id="job">\n`

    for (const tarefa in tarefas){
        //check input type
        if (tarefa.nr == index){
            html+=`
            <li>
            <form action="/tasks/${tarefa.id}/edit" method="POST">
            <input type="text" id="title" name="title" placeholder="Escreve uma tarefa" value="${task.title}"/>
        

            <input type="hidden" name="status" value="pending">
            <input type="submit" value="Submit" class="addBtn"/>

            <a href="/" class="addBtn">Cancel</a>
            </form>
            </li>`
        }
        else{
        html+=`
        <li>
    		        <p>${tarefa.titulo}</p> 
    		        <p>${tarefa.descricao}</p>
                        <a href="/tasks/${tarefa.nr}/edit">
                        <a href="/tasks/${tarefa.nr}/complete">
            </li>\n
        `
        }

    }

}
