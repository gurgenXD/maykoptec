$(document).ready(function() {
    var activepane = $('#Passport-reg-pane');
    $(activepane).find('input, textarea').prop('required', true);


    $('.login-form .btn[type="submit"]').on('click', function(e) {
        $('#login-alert-r').addClass('d-none');
        e.preventDefault();

        var form = $(this)[0].form;

        csrf_token = form.elements['csrfmiddlewaretoken'].value;
        username = form.elements['username'].value.replace(/[^\d]/g, '');
        password = form.elements['password'].value;
        recaptcha = form.elements['g-recaptcha-response'].value;

        if(!recaptcha) {
            $('#login-alert').append(`
                <div class="alert alert-danger alert-dismissible small fade show" role="alert">
                    <strong>Произошла ошибка! </strong>Неправильная reCaptcha.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            `);
        } else {
            data = {
                'csrfmiddlewaretoken': csrf_token,
                username: username,
                password: password,
                'g-recaptcha-response': recaptcha,
            }

            $.ajax({
                type: 'POST',
                url: form.action,
                data: data,
                success: function(data) {
                    if (data.success) {
                        window.location.replace(`http://${data.domain}/users/profile/`);
                    } else {
                        $('#login-alert').append(`
                            <div class="alert alert-danger alert-dismissible small fade show" role="alert">
                                <strong>Произошла ошибка! </strong>Неправильный логин или пароль.
                                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                        `);
                    }
                }
            });
        }
    });
});
