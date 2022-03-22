function edit_btn(id,url) {
    
    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: url,
        method: "GET",
        data:{
          'id':id,
        },

        dataType : "json",
        success:function(response){
         
           $('#DetailPlantingModal').html(response.templateStr)
            $('#DetailPlantingModal').modal('show')
           
        }
    });
}


function edit_monitoring(url) {
    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: url,
        method: "GET",

        dataType : "json",
        success:function(response){
         //console.log(response.templateStr);
           $('#MonitoringModal').html(response.templateStr)
           $('#MonitoringModal').modal('show')
           
        }
    });
}

function reload() {
    location.reload();
}



function edit_prod(url) {

    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: url,
        method: "GET",
        dataType : "json",
        success:function(response){

           $('#ProducteursModal').html(response.templateStr)
           $('#ProducteursModal').modal('show')
           
        }
    });

}

function edit_formatoin(url) {
    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: url,
        method: "GET",
        dataType : "json",
        success:function(response){
         //console.log(response.templateStr);
           $('#FormationModal').html(response.templateStr)
           $('#FormationModal').modal('show')
           
        }
    });
}



function edit_parcelle(url) {
    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: url,
        method: "GET",
        dataType : "json",
        success:function(response){
         
           $('#ParcelleModal').html(response.templateStr)
           $('#ParcelleModal').modal('show')
           
        }
    });
}


function edit_pepiniere(url) {
    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: url,
        method: "GET",
        dataType : "json",
        success:function(response){
         
           $('#PepinieresModal').html(response.templateStr)
           $('#PepinieresModal').modal('show')
           
        }
    });
}



///////////////////////UNIQUE POUR LES MODIFICATIONS///////////////////////////////////////////////////////////


function delete_semence(url) {
    event.preventDefault();
        swal({
				title: "Voulez vous vraiment supprimer cet enregistrement ?",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			})
				.then((willDelete) => {
				if (willDelete) {
					$.get(url , { });
					swal("supprimer avec succès", {
						icon: "success",
					})
                    .then((ok) => {
                        if(ok) {
                            location.reload();
                        }
                    });
                    
				} else {

		}
		});

}


function edit(url) {
    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: url,
        method: "GET",
        dataType : "json",
        success:function(response){
         
           $('#agroModal').html(response.templateStr)
           $('#agroModal').modal('show')
           
        }
    });
}

function update(url) {

        event.preventDefault()
        
        $.ajax({
            url:url,
            method:'POST',
            data:$('#form').serialize(),
            dataType:'json',
            success: function(data){
                
                if(data.status == 400){

                    swal({
                        title: data.msg,
                        icon: "error",
                        dangerMode: true,
                    })
    
                }
                
                if(data.status == 200){
                    swal({
                        title: data.msg,
                        icon: "success",
                    })
                    .then((ok) => {
                        if(ok) {
                            location.reload();
                        }
                    });
                }else{
                    $.each(data.errors, function(prefix, val){
                    
                    $(form).find('span.'+prefix+'_error').text(val[0]);
                });
                }
            }
    
      
        });
        
    
}

function SaveAndRest(url) {
    event.preventDefault();
  

    $.ajax({
        url:url,
        method:'POST',
        data:$('#form').serialize(),
        dataType:'json',
        success: function(data){
            if(data.status == 400){

                alertify.error(data.msg)

            }else{
                //console.log(data)

                if(data.status == 200){
                    swal({
                        title: data.msg,
                        icon: "success",
                    })
                    .then((ok) => {
                        if(ok) {
                            location.reload();
                        }
                    });
                }else{
                    $.each(data.errors, function(prefix, val){
                        
                        $(form).find('span.'+prefix+'_error').text(val[0]);
                    });
                }

            }

           

        }
    });
    
}

function SaveAndRedirect(url) {

    event.preventDefault();
    


    $.ajax({
        url:url,
        method:'POST',
        data:$('#form').serialize(),
        dataType:'json',
        success: function(data){
            if(data.status == 400){

                alertify.error(data.msg)

            }else{
                //console.log(data)

                if(data.status == 200){
                    swal({
                        title: data.msg,
                        icon: "success",
                    })
                    .then((ok) => {
                        if(ok) {
                            window.location.href = 'http://127.0.0.1:8000/cooperatives/formation/'+data.id;
                        }
                    });
                }else{
                    $.each(data.errors, function(prefix, val){
                        
                        $(form).find('span.'+prefix+'_error').text(val[0]);
                    });
                }

            }

           

        }
    });
    
}

function show_especemonitoring(url) {
    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: url,
        method: "GET",
        dataType : "json",
        success:function(response){

            //console.log(response.templateStr)
         
           $('#modalshow').html(response.templateStr)
           $('#modalshow').modal('show')
           
        }
    });
}


function show_formremplacement(url) {
    
    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: url,
        method: "GET",
        dataType : "json",
        success:function(response){

            //console.log(response.templateStr)
         
           $('#modalshow').html(response.templateStr)
           $('#modalshow').modal('show')
           
        }
    });
}

//function CalculplantMort() {
//    var ids = $(this).attr('id');
//    alert(ids);
//    var recus = $("#recus").val();
//    var mature = $("#mature").val();
//    var mort = 0;
//
//    mort = recus - mature;
//
//    $("#mort").val(parseInt(mort));
//
//
//    
//}

function save(url) {

    event.preventDefault();
  

    $.ajax({
        url:url,
        method:'POST',
        data:$('#form').serialize(),
        dataType:'json',
        success: function(data){

            if(data.status == 400){

                swal({
                    title: data.msg,
                    icon: "error",
                    dangerMode: true,
                })

            }else{
                //console.log(data)

                if(data.status == 200){
                    swal({
                        title: data.msg,
                        icon: "success",
                    })
                    .then((ok) => {
                        if(ok) {
                            location.reload();
                        }
                    });
                }else{
                    $.each(data.errors, function(prefix, val){
                        
                        $(form).find('span.'+prefix+'_error').text(val[0]);
                        //alertify.error(val[0])
                    });
                }

            }


        }

    })
    
}



$("#select_all").change(function(){
  
          $(".my_checkbox").prop('checked', $(this).prop("checked"));
      });

      $('.my_checkbox').change(function(){

          if(false == $(this).prop("checked")){
              $("#select_all").prop('checked', false);

          }

          if ($('.my_checkbox:checked').length == $('.my_checkbox').length ){
              $("#select_all").prop('checked', true);
          }
          });



function saveParticipant(url) {
    event.preventDefault();
    var nom = $("#id_nom").val().trim()
    //var localite = $("#id_localite").val().trim()

    if(nom !='' ){
        
        $.ajax({
            url:url,
            method:'POST',
            data:$('#addUser').serialize(),
            dataType:'json',
            success: function(data){

                if(data.status == 200){
                    location.reload()
                    alertify.success(data.msg)
                }else{
                    $.each(data.errors, function(prefix, val){
                        
                        $('#addUser').find('span.'+prefix+'_error').text(val[0]);
                        //alertify.error(val[0])
                    });
                }

            
                
            }
    
        });

        $('form#addUser').trigger("reset");
      

    }else{
        alertify.error("Le champs nom est obligatoire.");
    }   

    
    
}



        

//function appendToUsrTable(participant) {
//    $("#userTable > tbody:last-child").append(`
//          <tr id="user-${participant.id}">
//                <td><input class="my_checkbox" type="checkbox" name="check[]" id="${participant.id}" > </td>
//                <td id="col0"><input type="text" class="form-control" value="${participant.nom}" name="nom" readonly ></td> 
//                <td id="col1"><input type="text" class="form-control" value="${participant.contact}"  name="contact" readonly ></td> 
//                <td id="col2"><input type="text" class="form-control" value="${participant.localite}" name="localite" readonly ></td> 
//                <td id="col2 " class="text-center"> 
//                    <a href="#" onclick="" style="padding: 0px;" class="btn btn-danger">
//                        <i class="fa fa-trash fa-fw"></i>
//                    </a>
//                </td>
//          </tr>
//      `);
//}

function deleteItems(url)
{

   
    if ($('.my_checkbox:checked').length != 0 )
    {


        var donnees = new Array();
        $("input:checked").each(function () {
            donnees.push($(this).attr("value"));

        });

        console.log(JSON.stringify(donnees) )

        swal({
            title: "Voulez vous vraiment supprimer ces enregistrements ?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
            .then((willDelete) => {
            if (willDelete) {
                $.post(url , {d:JSON.stringify(donnees.toString().trim())},);
                swal("supprimer avec succès", {
                    icon: "success",
                })
                .then((ok) => {
                    if(ok) {
                        location.reload();
                    }
                });
                
            } else {
               

    }
    });
     
    }
}


function changeSection(id,url) {


    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: url,
        method: "POST",
        data:{
          'id':id,
        },

        dataType : "json",
        success:function(response){
         
           $('#sous_section').html(response.templateStr)
          
           
        }
    });
    
}


function globalproduct(url) {
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    var prod = $('#id_noms').val();

 

    if(prod != ""){
        $.ajax({
            url: url,
            method:"POST",
            data:{
              'nom':$('#id_nom').val().trim(),
            },
    
            dataType : "json",
            success:function(response){
             
              $('#contact').val(response.contact)
              
               
            }
        });
    }else{

    }
    
}


function show_form(url) {
    
    event.preventDefault();
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: url,
        method: "GET",
        dataType : "json",
        success:function(response){

            //console.log(response.templateStr)
         
           $('#modalshow').html(response.templateStr)
           $('#modalshow').modal('show')
           
        }
    });
}

