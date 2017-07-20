$(document).ready(function () {
    var seguridad = $('input:hidden[name="csrfmiddlewaretoken"]').val();
    $("#id_uno_jefe_institucion").attr('class', 'active');
    $('input:text').val('');

    var entero = "0123456789";
    $('#cedula_jefe,#cedula,#telefono,#telefono_represe').validar(entero);
    $('#cedula_jefe').focus().attr('maxlength', '10');
    $('#h_ced_jefe').val('true');

    var TUbch = $('#tabla_ubch').dataTable({
        "iDisplayLength": 10,
        "iDisplayStart": 0,
        "sPaginationType": "full_numbers",
        "aLengthMenu": [10, 20, 30, 40, 50],
        "oLanguage": {"sUrl": "/static/js/es.txt"},
        "aoColumns": [
            {"sClass": "control", "sWidth": "4%"},
            {"sClass": "registro right", "sWidth": "4%"},
            {"sClass": "registro right", "sWidth": "5%"},
            {"sClass": "registro left", "sWidth": "25%"},
            {"sClass": "registro right", "sWidth": "8%"},
            {"sClass": "registro right", "sWidth": "11%"},
            {"sClass": "registro left"},
            {"sWidth": "3%", "bSortable": false, "sClass": "center sorting_false", "bSearchable": false},
            {"sClass": "none"}
        ]
    });

    $('#buscar_patru').click(function () {

        var este = $(this);
        var $cedula = $('#cedula_jefe');
        $('div#div_registro').slideUp(1000);
        $('div#div_lista').slideDown(1000);
        $('#restablecer').trigger('click');
        if (!$(".appriseInner").is(":visible") == true) {

            if ($cedula.val() === null || $cedula.val().length === 0 || /^\s+$/.test($cedula.val())) {
                apprise('<span style="color:#FF0000;font-weight:bold">Debe indicar el n&uacute;mero de  C&eacute;dula</span>', {'textOk': 'Aceptar'}, function () {
                    $cedula.parent('div').addClass('has-error');
                    $cedula.focus();
                });
            } else {
                TUbch.fnClearTable();
                $('#nombre_patru,#telefono_patru,#codigo,#centro').val('');
                $('#tipo').css('display', 'none').text('');
                $('div').removeClass('has-error');
                $.post('', {'cedula': $cedula.val(), 'csrfmiddlewaretoken': seguridad, 'accion': 'buscar_jefes'}, function (data) {
                    if (data['existe'] == 'no') {
                        apprise('<span style="color:#FF0000;font-weight:bold">Esta n&uacute;mero de C&eacute;dula no pertenece a un Jefe de CLP o Jefe de UBCH</span>', {'textOk': 'Aceptar'}, function () {
                            $('#cedula_jefe').parent('div').addClass('has-error');
                            $('#cedula_jefe').focus().select();
                            $('#div_nuevo').css('display', 'none');
                            $('div#div_registro').slideUp(1000);
                            $('div#div_lista').slideDown(1000);
                        });
                    } else if (data.cod_cargo > 1) {
                        apprise('<span style="color:#FF0000;font-weight:bold">Esta n&uacute;mero de C&eacute;dula es un Jefe de Patrulla <br/> Nombre:' + data.nombre + '</span>', {'textOk': 'Aceptar'}, function () {
                            $('#cedula_jefe').parent('div').addClass('has-error');
                            $('#cedula_jefe').focus().select();
                        });
                    } else {
                        var texto = 'Jefe de UBCH';
                        if (data.cod_cargo == 0) {
                            texto = 'Jefe de CLP';
                        }
                        $('#tipo').css('display', 'block').text(texto);
                        $('#nombre_patru').val(data.nombre);
                        $('#telefono_patru').val(data.telefono);
                        $('#codigo').val(data.codigo);
                        $('#centro').val(data.centro);
                        $('#div_nuevo').css('display', 'block');

                        $.post('/ubch/registro/', {'cedula': $cedula.val(), 'csrfmiddlewaretoken': seguridad, 'accion': 'buscar_uno'}, function (data) {
                            $.each(data, function (i, obj) {
                                var eli = '<img class="eliminar" id ="' + obj.id + '" style="width:24px;height:24px;cursor:pointer"  src="/static/img/eliminar.png" />';
                                var contador = i + 1;
                                TUbch.fnAddData(['', contador, obj.cedula, obj.nombres, obj.telefono, obj.cod_ubch, obj.nom_ubch, eli, obj.direcc_p]);
                            });
                        }, 'json');
                    }
                }, 'json');
            }
        }
    });

    $('#add').click(function () {
        $('#div_nuevo').css('display', 'none');
        $('div#div_lista').slideUp(1000);
        $('div#div_registro').slideDown(1000, function () {
            $('#cedula').focus();
        });
    });


    $('#buscar').click(function () {
        var este = $(this);
        var cedula = $('#cedula').val();
        $('#telefono,#twitter,#p_nombre,#s_nombre,#p_apellido,#s_apellido,#cod_ubch,#ubch,#id_direcc_p').val('')
        if (!$(".appriseInner").is(":visible") == true) {
            if (cedula === null || cedula.length === 0 || /^\s+$/.test(cedula)) {
                apprise('<span style="color:#FF0000;font-weight:bold">Debe indicar el n&uacute;mero de C&eacute;dula</span>', {'textOk': 'Aceptar'}, function () {
                    $('#cedula').parent('div').addClass('has-error');
                    $('#cedula').focus();
                });
            } else {
                $.get("http://consultaelectoral.bva.org.ve/cedula=" + cedula, function (data) {
                    $('#p_nombre').val(data[0].p_nombre);
                    $('#s_nombre').val(data[0].s_nombre);
                    $('#p_apellido').val(data[0].p_apellido);
                    $('#s_apellido').val(data[0].s_apellido);
                    $('#cod_ubch').val(data[0].cod_nuevo);
                    $('#ubch').val(data[0].c_votacion);
                    $('#id_estado').val(data[0].cod_estado);
                    $('#id_municipio').val(data[0].cod_municipio);
                    $('#id_parroquia').val(data[0].cod_parroquia);
                    $("#id_direcc_u").val(data[0].c_direccion);
                    $("#id_estado_p").val(data[0].nom_estado);
                    $("#id_municipio_p").val(data[0].nom_mun);
                    $("#id_parroquia_p").val(data[0].nom_parroquia);

                }, 'json').fail(function () {
                    apprise('<span style="color:#FF0000;font-weight:bold">Esta C&eacute;dula no se encuentra registrada en el CNE</span>', {'textOk': 'Aceptar'}, function () {
                        este.parent('div').addClass('has-error');
                        este.focus().select();
                        $('#p_nombre,#s_nombre,#p_apellido,#s_apellido,#cod_ubch,#ubch,#id_direcc_p').val('');
                    });
                });
            }
        }
    });


    $('#registrar').click(function () {
        var texto_jefe = $('#tipo').text();
        var jefe_text = '';
        if (/CLP/.test(texto_jefe)) {
            jefe_text = 'CLP';
        } else if (/UBCH/.test(texto_jefe)) {
            jefe_text = 'UBCH';
        }

        var $cedula = $('#cedula');
        var $telefono = $('#telefono');
        var $direccion = $('#id_direcc_p');
        if (!$(".appriseInner").is(":visible") == true) {
            if ($cedula.val() === null || $cedula.val().length === 0 || /^\s+$/.test($cedula.val())) {
                apprise('<span style="color:#FF0000;font-weight:bold">Debe indicar el n&uacute;mero de C&eacute;dula</span>', {'textOk': 'Aceptar'}, function () {
                    $cedula.parent('div').addClass('has-error');
                    $cedula.focus();
                });
            } else if ($telefono.val() == '') {
                apprise('<span style="color:#FF0000;font-weight:bold">Debe indicar el n&uacute;mero de Tel&eacute;fono</span>', {'textOk': 'Aceptar'}, function () {
                    $telefono.parent('div').addClass('has-error');
                    $telefono.focus();
                });
            } else if ($direccion.val() === null || $direccion.val().length === 0 || /^\s+$/.test($direccion.val())) {
                apprise('<span style="color:#FF0000;font-weight:bold">Debe indicar la direcci&oacute;n</span>', {'textOk': 'Aceptar'}, function () {
                    $direccion.parent('div').addClass('has-error');
                    $direccion.focus();
                });
            } else if ($cedula.val() == $('#cedula_jefe').val()) {
                apprise('<span style="color:#FF0000;font-weight:bold">No puede registrar la misma C&eacute;dula del jefe de ' + jefe_text + ' a las lista de 1X10</span>', {'textOk': 'Aceptar'}, function () {
                    $cedula.parent('div').addClass('has-error');
                    $cedula.focus();
                });
            } else {
                $('#p_nombre,#s_nombre,#p_apellido,#s_apellido,#cod_ubch,#ubch,#nombre_represe,telefono_represe#telefono_represe').prop('disabled', false)
                var tipo_registro = $('#tipo_registro').val();
                var data_send = $("#frmjefe,#frmregistro").serialize() + '&' + $.param({accion: 'guardar','csrfmiddlewaretoken': seguridad});
                if(tipo_registro == 'institucion'){
                    var cedula_jefe = $('#cedula_represe').val()
                    var data_send = $("#form_institucion,#frmregistro").serialize() + '&' + $.param({cedula_jefe:cedula_jefe,accion: 'guardar',tipo:'institucion','csrfmiddlewaretoken': seguridad,is_institucion:true});
                }
                $.post("/ubch/registro/", data_send, function (response) {
                    $('#p_nombre,#s_nombre,#p_apellido,#s_apellido,#cod_ubch,#ubch,#nombre_represe,telefono_represe#telefono_represe').prop('disabled', true)
                    if (response['cedula_clp'] == 'existe') {
                        apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula pertenece a un Jefe de Clp y no puede ser registrado</span>', {'textOk': 'Aceptar'}, function () {
                            $cedula.parent('div').addClass('has-error');
                            $cedula.focus().select();
                        });
                    } else if (response['cedula_ubch'] == 'existe') {
                        apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula pertenece a un Jefe de UBCH y no puede ser registrado</span>', {'textOk': 'Aceptar'}, function () {
                            $cedula.parent('div').addClass('has-error');
                            $cedula.focus().select();
                        });
                    } else if (response['cedula_patrullero'] == 'existe') {
                        apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula pertenece a un Patrullero de UBCH y no puede ser registrado</span>', {'textOk': 'Aceptar'}, function () {
                            $cedula.parent('div').addClass('has-error');
                            $cedula.focus().select();
                        });
                    } else if (response['cedula_inst'] == 'existe') {
                        apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula pertenece a un representante de Instituci&oacute;n</span>', {'textOk': 'Aceptar'}, function () {
                            $cedula.parent('div').addClass('has-error');
                            $cedula.focus().select();
                        });
                    } else if (response['cedula_patr'] == 'existe') {
                        apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula ya pertenece a su lista 1X10</span>', {'textOk': 'Aceptar'}, function () {
                            $cedula.parent('div').addClass('has-error');
                            $cedula.focus().select();
                        });
                    } else if (response['cedula'] == 'existe') {
                        var pertenece = response['pertenece'];
                        text_pertenece = 'Patrullero';
                        if (pertenece == 'clp') {
                            text_pertenece = 'jefe de CLP';
                        } else if (pertenece == 'ubch') {
                            text_pertenece = 'jefe de UBCH';
                        }
                        apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula ya pertenece a lista de 1X10 del ' + text_pertenece + ',<br/> "' + response['nombre'] + '"</span>', {'textOk': 'Aceptar'}, function () {
                            $cedula.parent('div').addClass('has-error');
                            $cedula.focus().select();
                        });
                    } else if (response['save'] == 'ok') {
                        var cedula = $('#cedula').val();
                        var nombres = $('#p_nombre').val() + ' ' + $('#s_nombre').val() + ' ' + $('#p_apellido').val() + ' ' + $('#s_apellido').val();
                        var telefono = $('#telefono').val();
                        var cod_ubch = $('#cod_ubch').val();
                        var ubch = $('#ubch').val();
                        var direccion = $('#id_direcc_p');
                        var id = response['id'];
                        var totalfilas = TUbch.fnGetData().length;
                        var ultimo = totalfilas + 1;
                        apprise('<span style="color:#059102;font-weight:bold">El registro se guardo sastifactoriamente', {'textOk': 'Aceptar'}, function () {
                            var eli = '<img class="eliminar" id ="' + id + '" style="width:24px;height:24px;cursor:pointer"  src="/static/img/eliminar.png" />';
                            TUbch.fnAddData(['', ultimo, cedula, nombres, telefono, cod_ubch, ubch, eli, direccion.val()]);
                            $('div#div_registro').slideUp(1000);
                            $('div#div_lista').slideDown(1000);
                            $('#cedula,#telefono,#twitter,#p_nombre,#s_nombre,#p_apellido,#s_apellido,#cod_ubch,#ubch,#id_direcc_p').val('')
                            $('#div_nuevo').fadeIn(1000);
                        });
                    }
                });
            }
        }
    });
    $('#add_institucion').click(function() {
        TUbch.fnClearTable();
        $('#frmjefe,#div_registro').find('input:text').val('')
        $('#tipo_registro').val('institucion')
        $('div#div_jefes').slideUp(3000);
        $('div#div_instituciones').slideDown(3000);
        $('div#div_registro').slideUp(1000);
        $('div#div_lista').slideDown(1000);
        $('#div_nuevo').fadeOut(1000);
    });
    $('#add_clpubch').click(function() {
        TUbch.fnClearTable();
        $('#form_institucion,#div_registro').find('input:text').val('')
        $('div#div_instituciones').slideUp(3000);
        $('div#div_jefes').slideDown(3000);
        $('div#div_registro').slideUp(1000);
        $('div#div_lista').slideDown(1000);
        $('#div_nuevo').fadeOut(1000);
    });
    
    $('#buscar_represe').click(function () {
        $('div#div_registro').slideUp(1000);
        $('div#div_lista').slideDown(1000);
        var cedula = $('#cedula_represe').val();
        TUbch.fnClearTable();
        $('#nombre_represe,#telefono_represe,#institucion').val('');
        $.post('/ubch/registro/', {'cedula': cedula, 'csrfmiddlewaretoken': seguridad, 'accion': 'buscar_represe'}, function (data) {
            if (data.existe_clp == 'si') {
                apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula pertenece a un Jefe de Clp y no puede ser registrado</span>', {'textOk': 'Aceptar'}, function () {
                    $('#cedula_represe').parent('div').addClass('has-error');
                    $('#cedula_represe').focus().select();
                });
            }else if (data.existe_ubch == 'si') {
                apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula pertenece a un Jefe de UBCH y no puede ser registrado</span>', {'textOk': 'Aceptar'}, function () {
                    $('#cedula_represe').parent('div').addClass('has-error');
                    $('#cedula_represe').focus().select();
                });
            }else if (data.existe_patru == 'si') {
                apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula pertenece a un Patrullero y no puede ser registrado</span>', {'textOk': 'Aceptar'}, function () {
                    $('#cedula_represe').parent('div').addClass('has-error');
                    $('#cedula_represe').focus().select();
                });
            }else if (data.existe_unodiez == 'si') {
                apprise('<span style="color:#FF0000;font-weight:bold">Este n&uacute;mero de C&eacute;dula pertenece a un UNO X 10 y no puede ser registrado</span>', {'textOk': 'Aceptar'}, function () {
                    $('#cedula_represe').parent('div').addClass('has-error');
                    $('#cedula_represe').focus().select();
                }); 
            }else if (data.existe == 'no') {
                $.get("http://consultaelectoral.bva.org.ve/cedula=" + cedula, function (data) {
                    var nombre = data[0].p_nombre;
                    if (data[0].s_nombre == '') {
                        nombre += '+' + data[0].s_nombre;
                    } else {
                        nombre += ' ' + data[0].s_nombre;
                    }
        
                    nombre += ' ' + data[0].p_apellido;
        
                    if (data[0].s_apellido == '') {
                        nombre += ' ' + data[0].s_apellido;
                    } else {
                        nombre += ' ' + data[0].s_apellido;
                    }
                    $('#div_nuevo').css('display', 'block');
                    $('#nombre_represe').val(nombre);
        
                    
                }, 'json').fail(function () {
                    apprise('<span style="color:#FF0000;font-weight:bold">Esta C&eacute;dula no se encuentra registrada en el CNE</span>', {'textOk': 'Aceptar'}, function () {
                        $('#cedula_represe').parent('div').addClass('has-error');
                        $('#cedula_represe').focus().select();
                        $('#nombre_represe,#telefono_represe,#codigo_represe,#centro_represe').val('');
                    });
                });
            }else{
                $('#div_nuevo').css('display', 'block');
                $('#nombre_represe').val(data.nombre);
                $('#telefono_represe').val(data.telefono);
                $('#institucion').val(data.institucion);
                
                $.post('/ubch/registro/', {'cedula': cedula, 'csrfmiddlewaretoken': seguridad, 'accion': 'buscar_uno'}, function (data) {
                    $.each(data, function (i, obj) {
                        var eli = '<img class="eliminar" id ="' + obj.id + '" style="width:24px;height:24px;cursor:pointer"  src="/static/img/eliminar.png" />';
                        var contador = i + 1;
                        TUbch.fnAddData(['', contador, obj.cedula, obj.nombres, obj.telefono, obj.cod_ubch, obj.nom_ubch, eli, obj.direcc_p]);
                    });
                }, 'json');
            }
        })
        
    });
});