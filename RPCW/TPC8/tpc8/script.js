var id = -1



$(function(){
    $.get('http://localhost:4000/paras', function(data){
        data.forEach(function(data) {
            
            var remove = $("<button/>").css({"margin-left": "10px"}).text("remove")
            remove.click(function() {
                id = data._id
                $.ajax({
                    url: 'http://localhost:4000/paras/remove/' + id,
                    type: 'DELETE',
                    success: function(response) {
                        location.reload()
                    }
                });
                
            })
            
            var edit = $("<button/>").css({"margin-left": "20px"}).text("Editar")
            edit.click(function() {
                id = data._id
                $("#novoPar").val(data.para);
            })
            
            var element = $("<li style=\"margin-bottom: 10px;\" ><b>"+ data.data +":</b> " + data.para + "</li>")

                element.append(edit).append(remove)
                $("#paras").append(element);
        })
    })

    $("#botao").click(function(){
        if (id == -1){
          $.post('http://localhost:4000/paras',$("#novoPar").serialize())
          alert('Adicionado ' + ($("#novoPar").val()))
          $("#novoPar").val("")
          location.reload()
        }
        else{
          $.ajax({
            url: 'http://localhost:4000/paras/editar/'+id,
            type: 'PUT',
            data:$("#paraForm").serialize(),
            success: function(response) {
                alert('Editado: ' + ($("#novoPar").val()));
                $("#novoPar").val("");
                id = -1;
                location.reload();
            }
          });
        }
    })
});